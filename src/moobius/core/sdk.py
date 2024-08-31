# **The main Moobius module**
# Handles channel and database initialization.
# Wraps the two platform APIs (HTTP and Socket) together.
# Supports user mode which allows it to act like a user.
# And much, much more.
# Override the Moobius class to implement your service.

import json, os, sys, asyncio, json, uuid, aioprocessing
from typing import Optional
import dataclasses
from dataclasses import asdict

from dacite import from_dict
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from loguru import logger

from moobius import types, json_utils, quickstart
from moobius.core import groups
from moobius.network.ws_client import WSClient
from moobius.network.http_api_wrapper import HTTPAPIWrapper
from moobius.types import MessageContent, MessageBody, Button, ButtonClick, InputComponent, Payload, MenuItemClick, UpdateBody, UpdateItem, CopyBody, Character, ChannelInfo, CanvasItem, StyleItem, MenuItem, ClickArgument, SimpleAction
from moobius.database.storage import MoobiusStorage


quickstart.maybe_make_template_files({})


class Moobius:
    """
    This is the main core class of Moobius. CCS services inherit this class.
    This is a big switchyard for handling HTTP, the Websocket, and sending callbacks back to the CCS app.
    This has a complex lifecycle with server initialization steps, etc.
    """
    ############################ Startup functions ########################################

    def __init__(self, config: Optional[str|dict]=None, account_config: Optional[str|dict]=None, service_config: Optional[str|dict]=None, db_config: Optional[str|dict]=None, log_config: Optional[str|dict]=None):
        """
        Initializes a service object, can do so in "user mode" where it acts like a user.

        Parameters:
          config=None: All the configs. Can be a dict or a JSON filename.
          account_config=None: Config specific to the account. Can be a dict or a JSON filename. Overrides config.
          service_config=None: Config specific to launching the service. Can be a dict or a JSON filename. Overrides config.
          db_config=None: Config that sepecifies a per-channel MoobiusStorage object stored in self.channels. Can be a dict or a JSON filename. Overrides config.
          log_config=None: Config that is log-related.

        Example:
          >>> service = SDK(account_config={}, log_config={})
        """
        # Where to save the service id if a service is created?
        self.config, self._where_save_new_service_id = json_utils.get_config(config, account_config, service_config, db_config, log_config)
        self.service_mode = self.config['service_config'].get('service_mode', True)
        if self.service_mode and self.config['service_config'].get("service_id"):
            self.client_id = self.config['service_config']["service_id"]
        else:
            self.client_id = None # Will be initialized later by creating a new service.
        self._set_loguru()

        if not self.config['account_config']['email'] or not self.config['account_config']['password']:
            logger.error("Email and password must be specified in account_config or config['account_config'].")

        self.channels = {} # Generally filled up when initializing a channel.
        self.group_lib = groups.ServiceGroupLib()

        self.http_api = HTTPAPIWrapper(self.config['service_config']['http_server_uri'], self.config['account_config']['email'], self.config['account_config']['password'])
        self.ws_client = WSClient(self.config['service_config']['ws_server_uri'], on_connect=self.send_service_login if self.service_mode else self.send_user_login, handle=self.handle_received_payload, report_str='' if self.service_mode else ' (user-mode)')

        self.queue = aioprocessing.AioQueue()

        self.refresh_interval = 6 * 60 * 60             # 24h expire, 6h refresh
        self.authenticate_interval = 7 * 24 * 60 * 60   # 30d expire, 7d refresh
        self.heartbeat_interval = 30                    # 30s heartbeat
        self.checkin_interval = self.config['service_config'].get('checkin_interval', 60 * 60)

        self.scheduler = None

    def _set_loguru(self):
        """Sets the log levels etc. Returns None. Set after setting self._config"""
        logger.remove() # Remove the default one.

        logger.add(sys.stdout, level=self.config['log_config']['terminal_log_level'])
        if self.config['log_config'].get('log_file'):
            logger.add(self.config['log_config']['log_file'], level=self.config['log_config']['log_level'], **self.config['log_config']['log_retention'])
        if self.config['log_config']['error_log_file']:
            logger.add(self.config['log_config']['error_log_file'], level=self.config['log_config']['error_log_level'], **self.config['log_config']['log_retention'])

    async def true_channel_list(self):
        """Gets the list of channels the self will end up bound to. Only used if self.service_mode. Returns the channel id list."""
        channelid2serviceid = await self.fetch_service_id_each_channel() # Channels can only be bound to a SINGLE service.

        out = []
        others = self.config['service_config'].get("others", types.INCLUDE).lower().strip()
        all_channels = self.config['service_config'].get("channels", [])
        for channel_id in all_channels:
            bound_to = channelid2serviceid.get(channel_id)
            if bound_to == self.client_id:
                logger.info(f"Channel {channel_id} already bound to {self.client_id}, no need to bind it.")
            elif bound_to: # Conflict resolution.
                if others == types.IGNORE: # Do not intefere with channels bound to other users.
                    logger.info(f"Channel {channel_id} bound to service {bound_to} and will not be re-bound.")
                    continue
                elif others == types.UNBIND: # Be spiteful: Unbind channels bound to other users but don't use them.
                    logger.info(f"Unbinding channel {channel_id} from service {bound_to} but this service will not use this channel.")
                    await self.http_api.unbind_service_from_channel(bound_to, channel_id)
                    continue
                elif others == types.INCLUDE: # Steal channels from other services. Hopefully they won't mind.
                    logger.info(f"Unbinding channel {channel_id} from service {bound_to} so it can be used by this service instead.")
                    await self.http_api.unbind_service_from_channel(bound_to, channel_id)
                    bind_info = await self.http_api.bind_service_to_channel(self.client_id, channel_id) # may already be binded to the service itself
                    logger.info(f"Re-bound service to channel {channel_id}: {bind_info}")
                else:
                    raise Exception(f'Unknown others (other channels) option for handling channels already bound to other services: {others}')
            else:
                bind_info = await self.http_api.bind_service_to_channel(self.client_id, channel_id) # may already be binded to the service itself
                if bind_info:
                    logger.info(f"Bound service to channel {channel_id}: {bind_info}")
            out.append(channel_id)
        if len(out) == 0:
            if len(all_channels) == 0:
                logger.warning("No channel ids specified in the config['service_config']['channels']. Creating channels manually or using create_channel is necessary to do anything.")
            else:
                logger.warning("Channels were specified in the config, but they are all bound to other services and the 'others' option was not set to 'include'")
        return out

    async def create_new_service(self, description="Generated by MoobiusService"):
        """Creates a new service and sets self.client_id to it. Accepts an optional description. Returns the service_id."""
        self.client_id = await self.http_api.create_service(description=description)
        logger.info(f"NEW SERVICE CREATED!!!")
        logger.info("=================================================")
        logger.info(f" Service ID: {self.client_id}")
        logger.info("=================================================")
        logger.info(f"Please wait for 5 seconds...")
        if not self.client_id:
            raise Exception("Create new service gave None client_id.")
        if self._where_save_new_service_id: # None if no config json file given.
            json_utils.update_jsonfile(*(self._where_save_new_service_id+[self.client_id]))
        return self.client_id

    @logger.catch
    async def start(self):
        """
        Starts the service and calls start() fns are called with wand.run. There are 6 steps:
          1. Authenticate.
          2. Connect to the websocket server.
          3. Bind the service to the channels, if a service. If there is no service_id in the config file, create a new service and update the config file.
          4. Start the scheduler and run refresh(), authenticate(), and send_heartbeat() periodically.
          5. Call the on_start() callback (override this method to perform your own initialization tasks).
          6. Start listening to the websocket and the Wand.

        Returns None.
        """
        self._set_loguru() # Set it again, since it may be running on the child process.

        logger.debug("Starting service..." if self.service_mode else "Starting user-mode client...")

        await self.authenticate()
        await self.ws_client.connect()
        logger.debug("Connected to websocket server.")

        if self.service_mode:
            if not self.client_id:
                logger.debug('No service_id in config file. Will create a new service.')
                self.client_id = await self.create_new_service()
                await asyncio.sleep(5) # TODO: Sleeps "long enough" should be replaced with polling.
            if not self.client_id:
                raise Exception("Error creating a new service and getting its id.")
            await self.send_service_login()
            await asyncio.sleep(1)

            await self.before_channel_init()
            true_channel_ids = await self.true_channel_list()
            for channel_id in true_channel_ids:
                groupid2ids = await self.http_api.fetch_channel_group_dict(channel_id, self.client_id)
                logger.info(f'The channel {channel_id} has {len(groupid2ids)} groups, adding these to self.group_lib.')
                self.group_lib.id2ids_mdown = {**self.group_lib.id2ids_mdown, **groupid2ids}
                self.channels[channel_id] = None
                await self.on_channel_init(channel_id)
        else:
            user_info = await self.http_api.fetch_user_info()
            self.client_id = user_info.user_id
            await self.send_user_login()
            await self.user_join_service_channels()

        # Schedulers cannot be serialized so that you have to initialize it here
        self.scheduler = AsyncIOScheduler()

        # The details of access_token and refresh_token are managed by self.http_api
        self.scheduler.add_job(self.refresh_authentication, 'interval', seconds=self.refresh_interval)
        self.scheduler.add_job(self.authenticate, 'interval', seconds=self.authenticate_interval)
        self.scheduler.add_job(self.send_heartbeat, 'interval', seconds=self.heartbeat_interval)

        if self.checkin_interval > 0:
            self.scheduler.add_job(logger.catch(self._checkin), 'interval', seconds=self.checkin_interval) # This check-in must be after on_start()

        self.scheduler.start()
        logger.debug("Scheduler started.")

        await self.on_start()
        logger.debug("on_start() finished.")

        await asyncio.gather(self.ws_client.receive(), self.listen_loop())

    async def user_join_service_channels(self):
        """Joins service channels given a service config dict or JSON filename (use in user mode). Returns None"""
        channels = self.config['service_config'].get('channels', [])
        if len(channels)==0:
            logger.warning('No channels for the user mode service to join.')
        else:
            logger.info(f'User mode joining Service default channels (if not already joined). Will not join to any extra channels: {channels}')

        try:
            ch1 = await self.http_api.this_user_channels()
        except Exception as e:
            logger.warning(f'Error fetching channels this user is in: {e}')
            ch1 = []
        for channel_id in channels:
            if channel_id not in ch1:
                try:
                    chars = await self.fetch_member_ids(channel_id, raise_empty_list_err=False)
                except Exception as e:
                    logger.warning(f'fetch_member_ids failed: {e}. Channel will be joined')
                    chars = []
                try:
                    if type(chars) is not list or self.client_id not in chars:
                        await self.send_join_channel(channel_id)
                    else:
                        logger.info(f'User-mode service already in channel {channel_id}, no need to join.')
                except Exception as e:
                    logger.warning(f'User-mode service error joining channel: {e}')

    ################################## Query functions #######################################

    async def fetch_service_id_each_channel(self):
        """
        Returns a dict describing which service_id each channel_id is bound to. 
        Channels can only be bound to a single service.
        Channels not bound to any service will not be in the dict.
        """
        service_list = await self.http_api.fetch_service_id_list()
        channelid2serviceid = {} # Channels can only be bound to a SINGLE service.
        for service in service_list:
            for channel_id in service["channel_ids"]:
                channelid2serviceid[channel_id] = service['service_id']
        return channelid2serviceid

    async def fetch_bound_channels(self):
        """Returns a list of channels that are bound to this service."""
        ch_id2s_id = await self.fetch_service_id_each_channel()
        channel_ids = []
        for channel_id, service_id in ch_id2s_id.items():
            if service_id == self.client_id:
                channel_ids.append(channel_id)
        return channel_ids

    async def fetch_characters(self, channel_id):
        """
        Given a channel id, returns a list of Character objects.

        This list includes:
          Real members (ids for a particular user-channel combination) who joined the channel with the given channel_id.
          Agent characters that have been created by this service; agent characters are not bound to any channel.
        """
        member_ids = await self.fetch_member_ids(channel_id, False)
        member_profiles = await self.fetch_character_profile(member_ids)
        agent_profiles = await self.fetch_agents()
        return member_profiles + agent_profiles

    ################################## Actuators #######################################

    def _convert_message_content(self, subtype, content):
        """Given the subtype and the string or dict-valued content, returns a MessageContent object."""
        if type(content) is str:
            if subtype == types.TEXT:
                content = MessageContent(text=content)
            else:
                content = MessageContent(path=content)
        elif type(content) is dict:
            if 'size' in content:
                content = content.copy(); content['size'] = int(content['size'])
            content = MessageContent(**content)
        return content

    async def send_message(self, message, channel_id=None, sender=None, recipients=None, subtype=None, text=None, path=None, image=None, audio=None, link=None, title=None, button=None, len_limit=None, file_display_name=None, context=None):
        """
        Sends a message down (or up if in user-mode). This function is very flexible. Returns None.

        Parameters:
          message: The message to send.
            If a string, the message will be a text message unless subtype is set.
              If not a text message, the string must either be a local file_path or an http(s) file_path.
            If a MessageBody or dict, the message sent will depend on it's fields/attributes as well as the overrides specified.
            If a pathlib.Path, will be a file/audio/image message by default.
          channel_id=None: The channel ids, if None message must be a MessageBody with the channel_id.
            Overrides message if not None
          sender=None: The character/user who's avatar appears to "speak" this message.
            Overrides message if not None
          recipients=None: List of characters or character_ids.
            Overrides message if not None.
          subtype=None: Can be set to types.TEXT, types.IMAGE, types.AUDIO, types.FILE, or types.CARD
            If None, the subtype will be inferred.
          text=None: Text which will override message.
          path=None: The filepath or URL of the message's content. Not needed for text messages.
          image=None: Equivalent to path except for also setting the subtype to types.IMAGE.
          audio=None: Equivalent to path except for also setting the subtype to types.AUDIO.
          link=None: For card messages, the URL that the link links to.
          title=None: For card messages, the card title.
          button=None: For card messages, the text that appears in the button.
          len_limit=None: Limit the length of large text messages.
          file_display_name: The name shown for downloadable files can be set to a value different than the filename.
            Sets the subtype to "types.FILE" if subtype is not specified.
          context=None: Optional metadata.

        Example:
          TODO many examples!
        """
        if image:
            path=image
            subtype = types.IMAGE
        if audio:
            path=audio
            subtype = types.AUDIO
        message = types.normalize_message(message=message, channel_id=channel_id, sender=sender, recipients=recipients, subtype=subtype, len_limit=len_limit, file_display_name=file_display_name, path=path, text=text, link=link, title=title, button=button, context=context)

        # URL handling:
        if message['content'].path:
            message['content'].path = await self.http_api.convert_to_url(message['content'].path) # If already a URL will not change it or upload anything.
            if message['subtype'] == types.FILE and not message['content'].size:
                message['content'].size = await self.http_api.download_size(message['content'].path)

        if message.get('recipients'):
            message['recipients'] = await self._update_rec(message['recipients'], self.service_mode, message.get('channel_id'))
            if self.service_mode:
                message['sender'] = message['sender'] or 'no_sender'

            if self.service_mode:
                return await self.ws_client.message_down(self.client_id, self.client_id,  **message)
            else:
                for ky in ['sender', 'timestamp']: # Message up messages have no sender, it is just the user id.
                    if ky in message:
                        del message[ky]
                return await self.ws_client.message_up(self.client_id, self.client_id, **message)
        else:
            logger.warning('Empty or None recipients, no message will be sent.')

    async def send(self, payload_type, payload_body):
        """
        Sends any kind of payload to the websocket. Example payload types:
          message_down, update, update_characters, update_canvas, update_buttons, update_style, and heartbeat.
        Rarely used except internally, but provides the most flexibility for those special occasions.

        Parameters:
          payload_type (str): The type of the payload.
          payload_body (dict or str): The body of the payload.
            Strings will be converted into a Payload object.

        Returns None.
        """
        payload_dict = types.payload_as_dict(payload_type, payload_body, self.client_id, str(uuid.uuid4()))
        if 'body' in payload_dict:
            if 'recipients' in payload_dict['body']:
                if type(payload_dict['body']['recipients']) is not str:
                    if payload_dict['type'] == types.MESSAGE_UP:
                        is_mdown = False
                    elif payload_dict['type'] == types.MESSAGE_DOWN:
                        is_mdown = True
                    else:
                        raise Exception('Payload_dict type is neither message_up or message_down.')
                    channel_id = payload_dict['body']['channel_id']
                    payload_dict['body']['recipients'] = await self._update_rec(payload_dict['body']['recipients'], is_mdown, channel_id) # Convert list to group id.
        await self.ws_client.send(payload_dict)

    async def create_channel(self, channel_name, channel_desc, bind=True):
        """Creates a channel given the channel name, the channel description, and whether to bind to the new channel.
           By default bind is True, which means the service connects itself to the channel.
           Returns the channel id."""
        channel_id = await self.http_api.create_channel(channel_name, channel_desc)
        if bind:
            await self.http_api.bind_service_to_channel(self.client_id, channel_id)  # may already be binded to the service itself
        return channel_id

    async def send_canvas(self, canvas_items, channel_id, recipients):
        """Updates the canvas given a list of CanvasItems (which have text and/or images), a channel_id, and the recipients.
        Returns the message."""
        if type(canvas_items) is dict or type (canvas_items) is CanvasItem:
            canvas_items = [canvas_items]
        canvas_items = [dataclasses.replace(elem) for elem in canvas_items]
        for elem in canvas_items:
            if elem.path:
                elem.path = await self.http_api.convert_to_url(elem.path)
        return await self.ws_client.update_canvas(self.client_id, channel_id, canvas_items, await self._update_rec(recipients, True))

    async def send_heartbeat(self):
        """Sends a heartbeat to the server. Returns None."""
        await self.ws_client.heartbeat()

    async def send_refresh(self, channel_id):
        """Sends a refresh given a channel_id. Returns the message sent. A user function."""
        if self.service_mode:
            logger.warning('Send-refresh is a user function')
        return await self.ws_client.refresh_as_user(self.client_id, channel_id)

    async def do_member_sync(self, channel_id, character):
        """Syncs a member. Accepts a channel_id and character/character_id. Returns None. This is the most common way to send buttons, etc."""
        pass

    async def before_channel_init(self):
        """A global init called right before the channels are initialized. Returns None."""
        pass

    async def on_channel_checkin(self, channel_id):
        """CCS apps often override this, syncing members, etc.
        Accepts the channel id. Returns None."""
        pass

    async def send_service_login(self):
        """Calls self.ws_client.service_login using self.client_id and self.http_api.access_token."""
        if not self.client_id:
            self.client_id = await self.create_new_service()
        return await self.ws_client.service_login(self.client_id, self.http_api.access_token)


    ################################## Single-line functions #######################################
    async def _update_rec(self, recipients, is_m_down, channel_id=None):
        """
        Use this function in the in the "recipients" fields of the websocket.
        Converts lists into group_id strings, creating a group if need be, when given the recipients, True if a message down, and the channel_id.
        Returns the converted list.
        """
        return await self.group_lib.convert_list(self.http_api, recipients, is_m_down, channel_id)

    async def refresh_authentication(self): """Calls self.http_api.refresh."""; return await self.http_api.refresh()
    async def authenticate(self): """Calls self.http_api.authenticate."""; return await self.http_api.authenticate()
    async def sign_up(self): """Calls self.http_api.sign_up."""; return await self.http_api.sign_up()
    async def sign_out(self): """Calls self.http_api.sign_out."""; return await self.http_api.sign_out()
    async def update_current_user(self, avatar, description, name): """Calls self.http_api.update_current_user."""; return await self.http_api.update_current_user(avatar, description, name)
    async def update_agent(self, character, avatar, description, name): """Calls self.http_api.update_agent using self.client_id."""; return await self.http_api.update_agent(self.client_id, character, avatar, description, name)
    async def update_channel(self, channel_id, channel_name, channel_desc): """Calls self.http_api.update_channel."""; return await self.http_api.update_channel(channel_id, channel_name, channel_desc)
    async def bind_service_to_channel(self, channel_id): """Calls self.http_api.bind_service_to_channel"""; return await self.http_api.bind_service_to_channel(self.client_id, channel_id)
    async def unbind_service_from_channel(self, channel_id): """Calls self.http_api.unbind_service_from_channel"""; return await self.http_api.unbind_service_from_channel(self.client_id, channel_id)
    async def create_agent(self, name, avatar=None, description="No description"): """Calls self.http_api.create_agent using self.create_agent."""; return await self.http_api.create_agent(self.client_id, name, avatar, description)
    async def fetch_popular_channels(self): """Calls self.http_api.fetch_popular_channels."""; return await self.http_api.fetch_popular_channels()
    async def fetch_channel_list(self): """Calls self.http_api.fetch_channel_list."""; return await self.http_api.fetch_channel_list()
    async def fetch_member_ids(self, channel_id, raise_empty_list_err=False): """Calls self.http_api.fetch_member_ids using self.client_id."""; return await self.http_api.fetch_member_ids(channel_id, self.client_id, raise_empty_list_err=raise_empty_list_err)
    async def fetch_character_profile(self, character): """Calls self.http_api.fetch_character_profile"""; return await self.http_api.fetch_character_profile(character)
    async def fetch_service_id_list(self): """Calls self.http_api.fetch_service_id_list"""; return await self.http_api.fetch_service_id_list()
    async def fetch_agents(self): """Calls self.http_api.fetch_agents using self.client_id."""; return await self.http_api.fetch_agents(self.client_id)
    async def fetch_message_history(self, channel_id, limit=1024, before="null"): """Calls self.http_api.fetch_message_history."""; return await self.http_api.fetch_message_history(channel_id, limit, before)
    async def upload(self, file_path): """Calls self.http_api.upload. Note that uploads happen automatically for any function that accepts a file_path/url when given a local path."""; return await self.http_api.upload(file_path)
    async def download(self, source, file_path=None, auto_dir=None, overwrite=True, bytes=False, headers=None): """Calls self.http_api.download."""; return await self.http_api.download(source, file_path, auto_dir, overwrite, bytes, headers)

    async def create_channel_group(self, channel_id, group_name, characters): """Calls self.http_api.create_channel_group, mainly for internal use."""; return await self.http_api.create_channel_group(channel_id, group_name, characters)
    async def create_service_group(self, characters): """Calls self.http_api.create_service_group, mainly for internal use."""; return await self.http_api.create_service_group(characters)
    async def character_ids_of_channel_group(self, sender_id, channel_id, group_id): """Calls self.http_api.character_ids_of_channel_group, mainly for internal use."""; return await self.http_api.character_ids_of_channel_group(sender_id, channel_id, group_id)
    async def character_ids_of_service_group(self, group_id): """Calls self.http_api.character_ids_of_service_group, mainly for internal use."""; return await self.http_api.character_ids_of_service_group(group_id)
    async def update_channel_group(self, channel_id, group_id, characters): """Calls self.http_api.update_channel_group, mainly for internal use."""; return await self.http_api.update_channel_group(channel_id, group_id, characters)
    async def update_temp_channel_group(self, channel_id, characters): """Calls self.http_api.update_temp_channel_group, mainly for internal use."""; return await self.http_api.update_temp_channel_group(channel_id, characters)
    async def fetch_channel_temp_group(self, channel_id): """Calls self.http_api.fetch_channel_temp_group, mainly for internal use."""; return await self.http_api.fetch_channel_temp_group(channel_id, self.client_id)
    async def fetch_channel_group_list(self, channel_id): """Calls self.http_api.fetch_channel_group_list, mainly for internal use."""; return await self.http_api.fetch_channel_group_list(channel_id, self.client_id)
    async def fetch_user_from_group(self, user_id, channel_id, group_id): """Calls self.http_api.fetch_user_from_group, mainly for internal use."""; return await self.http_api.fetch_user_from_group(user_id, channel_id, group_id)
    async def fetch_target_group(self, user_id, channel_id, group_id): """Calls self.http_api.fetch_target_group, mainly for internal use."""; return await self.http_api.fetch_target_group(user_id, channel_id, group_id)

    async def send_user_login(self): """Calls self.ws_client.user_login using self.http_api.access_token; Use for user mode."""; return await self.ws_client.user_login(self.http_api.access_token)
    async def send_update(self, data, target_client_id): """Calls self.ws_client.update"""; return await self.ws_client.update(data, self.client_id, target_client_id)
    async def send_characters(self, characters, channel_id, recipients): """Calls self.ws_client.send_characters using self.client_id. Converts recipients to a group_id if a list."""; return await self.ws_client.send_characters(await self._update_rec(characters, True), self.client_id, channel_id, await self._update_rec(recipients, True))
    async def send_buttons(self, buttons, channel_id, recipients): """Calls self.ws_client.send_buttons using self.client_id. Converts recipients to a group_id if a list."""; return await self.ws_client.send_buttons(buttons, self.client_id, channel_id, await self._update_rec(recipients, True))
    async def send_menu(self, menu_items, channel_id, recipients): """Calls self.ws_client.send_menu using self.client_id. Converts recipients to a group_id if a list."""; return await self.ws_client.send_menu(menu_items, self.client_id, channel_id, await self._update_rec(recipients, True))
    async def send_style(self, style_items, channel_id, recipients): """Calls self.ws_client.send_style using self.client_id. Converts recipients to a group_id if a list."""; return await self.ws_client.send_style(style_items, self.client_id, channel_id, await self._update_rec(recipients, True))

    async def send_join_channel(self, channel_id): """Calls self.ws_client.join_channel using self.client_id. Use for user mode."""; return await self.ws_client.join_channel(self.client_id, channel_id)
    async def send_leave_channel(self, channel_id): """Calls self.ws_client.leave_channel using self.client_id. Used for user mode."""; return await self.ws_client.leave_channel(self.client_id, channel_id)
    async def send_button_click(self, button_id, bottom_button_id, button_args, channel_id): """Calls self.ws_client.send_button_click using self.client_id. Used for user mode."""; await self.ws_client.send_button_click(button_id, bottom_button_id, button_args, channel_id, self.client_id, dry_run=False)
    async def send_menu_item_click(self, menu_item_id, bottom_button_id, button_args, the_message, channel_id): """Calls self.ws_client.send_menu_item_click using self.client_id. Used for user mode."""; await self.ws_client.send_menu_item_click(menu_item_id, bottom_button_id, button_args, the_message, channel_id, self.client_id, dry_run=False)

    ################################## Callback switchyards #######################################

    async def _checkin(self):
        """Called as a rate task, used to resync users, etc. Only called after on_start(). Returns None."""
        for channel_id in self.channels.keys():
            await self.on_channel_checkin(channel_id)

    @logger.catch
    async def listen_loop(self):
        """Listens to the wand in an infinite loop, polling self.queue (which is an aioprocessing.AioQueue).
        This allows the wand to send "spells" (messages) to the services at any time. Returns Never."""
        while True:
            obj = await self.queue.coro_get()
            await self.on_spell(obj)

    @logger.catch
    async def handle_received_payload(self, payload):
        """
        Decodes the received websocket payload JSON and calls the handler based on p['type'], given the payload string. Returns None.
        Example methods called:
          on_message_up(), on_action(), on_button_click(), on_copy_client(), on_unknown_payload()

        Example use-case:
          >>> self.ws_client = WSClient(ws_server_uri, on_connect=self.send_service_login, handle=self.handle_received_payload)
        """

        payload_data = json.loads(payload)
        if 'message' in payload_data:
            if payload_data['message'].lower().strip() == 'Internal server error'.lower():
                logger.error('Received an internal server error from the Websocket.')
                return

        payload_body = payload_data['body']
        async def _group2ids(g_id):
            """Accepts a gorup id. Returns a list of character id strings."""
            return await groups.group2ids(g_id, payload_body, self.http_api, self.client_id)

        if 'subtype' in payload_body and payload_body['subtype'] == types.UPDATE_CHARACTERS:
            if 'content' not in payload_body:
                raise Exception("Must have content.")
            payload_body['content']['characters'] = await _group2ids(payload_body['content']['characters'])

        if 'recipients' in payload_body:
            rec_group = payload_body['recipients']
            payload_body['recipients'] = await _group2ids(rec_group)

        if 'type' in payload_data:
            payload = from_dict(data_class=Payload, data=payload_data) # Brittle type inference.
            if payload.type == types.MESSAGE_DOWN:
                payload_body = types.recv_tmp_convert('on_message_down', payload_body)
                payload_body['content'] = MessageContent(**payload_body['content'])
                await self.on_message_down(MessageBody(**payload_body))
            elif payload.type == types.UPDATE:
                # First convert the content into an UpdateItem:
                update = types.as_update_body(payload_body)
                if update.recipients not in [types.SERVICE, 'null', '', None, False]:
                    r_group = payload_body['recipients']
                    if type(r_group) not in [list, tuple]:
                        try:
                            update.recipients = await self.character_ids_of_service_group(r_group) # Convert to list.
                            if not update.recipients:
                                update.recipients = f'WARNING: empty list for group_id {r_group}'
                        except Exception as e:
                            update.recipients = [f"ERROR getting character_ids for group_id: {r_group}"]
                await self.on_update(update)
            elif payload.type == types.MESSAGE_UP:
                payload_body['content'] = MessageContent(**payload_body['content'])
                await self.on_message_up(MessageBody(**payload_body))
            elif payload.type == types.ACTION:
                await self.on_action(payload_body)
            elif payload.type == types.COPY:
                await self.on_copy_client(CopyBody(**payload_body))
            elif payload.type == types.REFRESH:
                payload_body['subtype'] = types.REFRESH
                await self.on_refresh(SimpleAction(**payload_body))
            else:
                logger.warning(f"Unknown payload received: {payload}; DATA: {payload_data}")
                await self.on_unknown_payload(payload_data)
        else:
            logger.error(f"Unknown payload without type: {payload_data}")

    async def on_action(self, action_data: dict):
        """
        Accepts the action data (as a dict) from a user. Returns None.
        Calls the corresponding method to handle different subtypes of action.
        This callback is rarely overriden; it is more common to override the other callbacks that the calls.
        Example methods called:
          on_button_click(), on_join()
        """
        # Note: putting dataclass constructors here, instead of attempting to do it all at once, makes it much easier to debug.
        subtype = action_data['subtype']
        if subtype == types.JOIN:
            await self.on_join(SimpleAction(**action_data))
        elif subtype == types.LEAVE_CHANNEL:
            await self.on_leave(SimpleAction(**action_data))
        elif subtype == types.BUTTON_CLICK:
            if action_data.get('arguments'):
                action_data['arguments'] = [ClickArgument(**a) for a in action_data['arguments']]
            await self.on_button_click(ButtonClick(**action_data))
        elif subtype == types.MENU_ITEM_CLICK:
            if action_data.get('arguments'):
                action_data['arguments'] = [ClickArgument(**a) for a in action_data['arguments']]
            action_data['message_content'] = MessageContent(**action_data['message_content'])
            await self.on_menu_item_click(MenuItemClick(**action_data))
        elif subtype == types.REFRESH: # Is this used?
            await self.on_refresh(SimpleAction(**action_data))
        else:
            logger.error(f"Unknown action subtype: {subtype}")

    async def on_update(self, update: UpdateBody):
        """Accepts an Update object from the socket. Dispatches it to one of various callbacks. Use for user mode.
           It is recommended to overload the invididual callbacks instead of this function. Returns None."""
        if update.subtype == types.UPDATE_CHARACTERS:
            await self.on_update_characters(update)
        elif update.subtype == types.UPDATE_CHANNEL_INFO:
            await self.on_update_channel_info(update)
        elif update.subtype == types.UPDATE_CANVAS:
            await self.on_update_canvas(update)
        elif update.subtype == types.UPDATE_BUTTONS:
            await self.on_update_buttons(update)
        elif update.subtype == types.UPDATE_STYLE:
            await self.on_update_style(update)
        elif update.subtype == types.UPDATE_MENU:
            await self.on_update_menu(update)
        else:
            logger.error(f"Unknown update subtype: {update.subtype}")

    ############################## Simple callbacks (these are commonly overridden) #######################################

    async def on_start(self):
        """Called when the service is initialized. Returns None"""
        logger.debug("Service started. Override this method to perform initialization tasks.")

    async def on_channel_init(self, channel_id):
        """
        Called once per channel on startup. Accepts the channel ID. Returns None.
        By default, if the db has been set, a MoobiusStorage is created in self.channels, otherwise it is set to None.
        Also does a channel sync by default.
        """
        if self.config['db_config']: # Optional storage.
            self.channels[channel_id] = MoobiusStorage(self.client_id, channel_id, self.config['db_config'])
        await self.on_channel_checkin(channel_id)
        logger.debug('Initalized channel.')

    async def on_spell(self, obj):
        """Called when a "spell" from the wand is received, which can be any object but is often a string. Accepts whatever the wand sent this process. Returns None."""
        logger.debug(f'Spell Received {obj}')

    async def on_message_up(self, message: MessageBody):
        """
        This callback accepts a message from a user. Returns None.
        Example MessageBody object:
        >>>  moobius.MessageBody(subtype="text", channel_id=<channel id>, content=MessageContent(...), timestamp=1707254706635,
        >>>                      recipients=[<user id 1>, <user id 2>], sender=<user id>, message_id=<message-id>,
        >>>                      context={'group_id': <group-id>, 'channel_type': 'ccs'})
        """
        logger.debug(f"MessageUp received: {message}")

    async def on_copy_client(self, copy: CopyBody):
        """
        This callback accepts a "Copy" request from the user. Returns None.
        Example Copy object:
        >>> moobius.Copy(request_id=<id>, origin_type=message_down, status=True, context={'message': 'Message received'})"""
        if self.service_mode and not copy.status:
            await self.send_service_login()
        logger.debug("on_copy_client")

    async def on_refresh(self, action: SimpleAction):
        """
        This callback accepts a "Copy" request from the user. Returns None."""
        await self.do_member_sync(action.channel_id, action.sender)

    async def on_join(self, action: SimpleAction):
        """
        This callback happens when the user joins a channel. Accepts the channel and member id. Returns None.
        Commonly used to inform everyone about this new user and update everyone's character list."""
        await self.do_member_sync(action.channel_id, action.sender)

    async def on_leave(self, action: SimpleAction):
        """
        Called when the user leaves a channel. Accepts the channel and member id. Returns None.
        Commonly used to update everyone's character list."""
        logger.debug("on_action leave_channel")

    async def on_button_click(self, action: ButtonClick):
        """
        Handles a button click from a user. Accepts the user's ButtonClick. Returns None.
        Example ButtonClick object:
        >>> moobius.ButtonClick(button_id="the_big_red_button", channel_id=<channel id>, sender=<user id>, components=[], context={})
        """
        logger.debug(f"Button call received: {action}")

    async def on_menu_item_click(self, action: MenuItemClick):
        """Handles a context menu right click from a user. Accepts the user's MenuItemClick. Returns None.
        Example MenuItemClick object:
        >>> MenuItemClick(item_id=1, message_id=<id>, message_subtypes=text, message_content={'text': 'Click on this message.'}, channel_id=<channel_id>, context={}, recipients=[])
        """
        logger.debug(f"Right-click call received: {action}")

    async def on_unknown_payload(self, payload_data: dict):
        """A catch-all for handling unknown payloads. Accepts a payload-as-dict that has not been recognized by the other handlers and may not have a format listed in types. Returns None."""
        logger.warning("Unknown payload recieved from the websocket: "+str(payload_data))

    ############################## User mode-specific simple callbacks (also commonly overridden) #######################################

    async def on_message_down(self, message: MessageBody):
        """Callback when the user recieves a message. Accepts the service's MessageBody.
           Use for user mode. Returns None."""
        logger.debug(f"MessageDown received: {message}")

    async def on_update_characters(self, update: UpdateBody):
        """Callback when the user recieves the character list. Accepts the service's Update. One of the multiple update callbacks. Returns None.
           Use for user mode."""
        logger.debug("on_update_character")

    async def on_update_channel_info(self, update: UpdateBody):
        """Callback when the user recieves the channel info. Accepts the service's Update. One of the multiple update callbacks. Returns None.
           Use for user mode."""
        logger.debug("on_update_channel_info")

    async def on_update_canvas(self, update: UpdateBody):
        """Callback when the user recieves the canvas content. Accepts the service's Update. One of the multiple update callbacks. Returns None.
           Use for user mode."""
        logger.debug("on_update_canvas")

    async def on_update_buttons(self, update: UpdateBody):
        """Callback when the user recieves the buttons. Accepts the service's Update. One of the multiple update callbacks. Returns None.
           Use for user mode."""
        logger.debug("on_update_buttons")

    async def on_update_style(self, update: UpdateBody):
        """Callback when the user recieves the style info (look and feel). Accepts the service's Update. One of the multiple update callbacks. Returns None.
           Use for user mode."""
        logger.debug("on_update_style")

    async def on_update_menu(self, update: UpdateBody):
        """Callback when the user recieves the context menu info. Accepts the service's Update. One of the multiple update callbacks. Returns None.
           Use for user mode."""
        logger.debug("update_menu")

    #######################################################################################################################

    def __str__(self):
        fname = self.config_path
        http_server_uri = self.config['service_config'].get("http_server_uri")
        ws_server_uri = self.config['service_config'].get("ws_server_uri")
        email = self.config['account_config'].get("email")
        num_channels = len(self.channels)
        agsv = 'Service' if self.service_mode else 'User-mode'
        return f'moobius.SDK({agsv}; config=config={fname}, http_server_uri={http_server_uri}, ws_server_uri={ws_server_uri}, ws={ws_server_uri}, email={email}, password=****, num_channels={num_channels})'
    def __repr__(self):
        return self.__str__()
