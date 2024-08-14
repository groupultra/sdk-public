# **The main Moobius module**
# Handles channel and database initialization.
# Wraps the two platform APIs (HTTP and Socket) together.
# Supports user mode which allows it to act like a user.
# And much, much more.
# Override the Moobius class to implement your service.

import json, os, pathlib

import dataclasses
from dataclasses import asdict
from dacite import from_dict

import asyncio
import json
import uuid
import aioprocessing

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from moobius.network.ws_client import WSClient
import moobius.network.ws_client as ws_client
from moobius.network.http_api_wrapper import HTTPAPIWrapper
from moobius.types import MessageContent, MessageBody, Button, ButtonClick, InputComponent, Payload, MenuItemClick, UpdateBody, UpdateItem, CopyBody, Character, ChannelInfo, CanvasItem, StyleItem, MenuItem, RefreshBody, JoinBody, LeaveBody
from moobius.database.storage import MoobiusStorage
from moobius import utils, types
from loguru import logger

utils.maybe_make_template_files({})
strict_kwargs = False # If True all functions (except __init__) with more than one non-self arg will require kwargs. If False a default ordering will be used.


class ServiceGroupLib():
    """
    (This class is for internal use)
    Converts a list of character_ids into a service or channel group id, creating one if need be.
       The lookup is O(n) so performance at extremly large list sizes may require optimizations.
    """

    def __init__(self):
        """Creates an empty ServiceGroupLib instance."""
        logger.info(f'Initialized new, empty ServiceGroupLib on process {os.getpid()}')
        self.id2ids_mdown = {} # Message down creates service group with /service/group/create
        self.ids2id_mdown = {}
        self.id2ids_mup = {}
        self.ids2id_mup = {}
        self.alock = asyncio.Lock()

    async def convert_list(self, http_api, character_ids, is_message_down, channel_id=None):
        """
        Converts a list to single group id, unless it is already a group id.

        Parameters:
          http_api: The http_api client in Moobius
          character_ids: List of ids. If a string, treated as a one element list.
          is_message_down: True = message_down (a message sent from the service), False = message_up (a message sent from a user).
          channel_id=None: If None and the conversion still needs to happen it will raise an Exception.

        Returns: The group id.
        """
        if is_message_down:
            ids2id = self.id2ids_mdown
            id2ids = self.id2ids_mdown
        else:
            ids2id = self.id2ids_mup
            id2ids = self.id2ids_mup
        async with self.alock: # Make sure the old list is stored before the new list is created.
            character_ids = utils.to_char_id_list(character_ids)
            if len(character_ids) == 0:
                return None
            else: # Convert list to a single group id in this mode.
                massive_str = '_'.join(character_ids)
                need_new_group = massive_str not in ids2id
                if need_new_group: # Call /service/group/create
                    character_ids = character_ids.copy()
                    if is_message_down:
                        group_id = (await http_api.create_service_group(character_ids)).group_id
                    else:
                        if not channel_id:
                            raise Exception('A channel_id must be specified when is_message_down is False')
                        group_id = (await http_api.create_channel_group(channel_id, 'A_message_up_group', character_ids)).group_id
                    ids2id[massive_str] = group_id
                    id2ids[group_id] = character_ids
                out = ids2id[massive_str]
                logger.info(f'Converted recipient list (is_mdown={is_message_down}) {character_ids} to group id {out} on process {os.getpid()}. {"Created new service group." if need_new_group else "Group already exists."}')
                return out


class Moobius:

    ############################ Startup functions ########################################

    def __init__(self, config_path, db_config_path=None, service_mode=True, **kwargs):
        """
        Initializes a service object, can do so in "user mode" where it acts like a user.

        Parameters:
          config_path: The path of the service config file.
            Can instead be a dict of the actual config, so that no file is loaded.
          db_config_path=None: The optional path of the database config file.
            Can also be a dict instead of a file.
          service_mode=True: True is the default for services. False is "user_mode" where we can simulate bieng an end-user.

        Example:
          >>> service = SDK(config_path="./config/service.json", db_config_path="./config/database.json", service_mode=True)
        """
        # Default logging settings:
        self.log_level = kwargs.get("terminal_log_level", "INFO")
        self.log_retention = kwargs.get('log_retention', {'rotation':"1 day", 'retention':"7 days"})
        self.log_file = kwargs.get('log_file')
        self.error_log_file = kwargs.get('error_log_file')
        self.error_log_level = kwargs.get('error_log_level', "WARNING")
        if 'log_settings' in kwargs: # Alternative option to specify a JSON.
            if type(kwargs['log_settings']) is str:
                with open(kwargs['log_settings'], 'r') as f:
                    kwargs['log_settings'] = json.load(f)
                logset = kwargs['log_settings']
                self.log_level = logset.get('log_level', self.log_level)
                self.log_retention = logset.get('log_retention', self.log_retention)
                self.log_file = logset.get('log_file', self.log_file)
                self.error_log_file = logset.get('error_log_file', self.error_log_file)
        if type(self.log_retention) is str:
            self.log_retention = {'retention':self.log_retention}
        self.log_level = self.log_level.upper()
        self.error_log_level = self.error_log_level.upper()

        utils.set_terminal_logger_level(self.log_level)

        self.config_path = config_path
        self.service_mode = service_mode

        if type(config_path) is dict:
            logger.info('Be careful to keep the secrets in your service config safe!')
            the_config = config_path
        elif type(config_path) is str:
            with open(config_path, "r", encoding='utf-8') as f:
                the_config = json.load(f)
        else:
            raise Exception('config_path not understood')
        self.config = the_config

        if type(db_config_path) is dict:
            self.db_config = db_config_path
        elif type(db_config_path) is str and db_config_path != "":
            with open(db_config_path, "r", encoding='utf-8') as f:
                self.db_config = json.load(f)
        elif not db_config_path:
            self.db_config = None
        else:
            raise Exception('db_config_path not understood')

        http_server_uri = self.config["http_server_uri"]
        ws_server_uri = self.config["ws_server_uri"]
        email = self.config["email"]
        password = self.config["password"]
        the_id = self.config.get("service_id", "")
        if the_id != '' and the_id and not self.service_mode:
            raise Exception('User-mode services cannot have a "service_id" in thier JSON config.')
        if self.service_mode:
            self.client_id = self.config.get("service_id", "")

        self._channels = [] # Generally filled up when initializing a channel.
        self.channel_storages = {} # MoobiusStorage objects.
        self.group_lib = ServiceGroupLib()

        self.http_api = HTTPAPIWrapper(http_server_uri, email, password)
        self.ws_client = WSClient(ws_server_uri, on_connect=self.send_service_login if self.service_mode else self.send_user_login, handle=self.handle_received_payload, report_str='' if self.service_mode else ' (user-mode)')

        self.queue = aioprocessing.AioQueue()

        self.refresh_interval = 6 * 60 * 60             # 24h expire, 6h refresh
        self.authenticate_interval = 7 * 24 * 60 * 60   # 30d expire, 7d refresh
        self.heartbeat_interval = 30                    # 30s heartbeat
        self.checkin_interval = 90

        self.scheduler = None

        self.init_all_channels = kwargs.get('initialize_all_bound_channels')

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
        utils.set_terminal_logger_level(self.log_level)

        logger.debug("Starting service..." if self.service_mode else "Starting user-mode client...")

        await self.authenticate()
        await self.ws_client.connect()
        logger.debug("Connected to websocket server.")

        if self.service_mode:
            if not self.client_id:
                logger.debug('No service_id in config file. Will create a new service.')
                self.client_id = await self.http_api.create_service(description="Generated by MoobiusService")

                logger.info(f"NEW SERVICE CREATED!!!")
                logger.info("=================================================")
                logger.info(f" Service ID: {self.client_id}")
                logger.info("=================================================")
                logger.info(f"Please wait for 5 seconds...")
                self.config["service_id"] = self.client_id
                await asyncio.sleep(5) # TODO: Sleeps "long enough" should be replaced with polling.
            if not self.client_id:
                raise Exception("Error creating a new service and getting its id.")

            if type(self.config_path) is str: # Save the newly created service if any.
                with open(self.config_path, "r", encoding='utf-8') as f:
                    old_config = json.load(f)
                s_id = self.config['service_id']
                if s_id != old_config.get('service_id'):
                    old_config['service_id'] = s_id
                    with open(self.config_path, "w", encoding='utf-8') as f:
                        json.dump(old_config, f, indent=4, ensure_ascii=False)
                        logger.info(f"Config file 'service_id' updated to {s_id}: {self.config_path}")

            if len(self.config["channels"]) == 0:
                logger.error('No channels specified in self.config')
                return

            channelid2serviceid = await self.fetch_service_id_each_channel() # Channels can only be bound to a SINGLE service.

            others = self.config["others"].lower().strip()
            for channel_id in set(self.config["channels"]):
                bound_to = channelid2serviceid.get(channel_id)
                if bound_to == self.client_id:
                    logger.info(f"Channel {channel_id} already bound to {self.client_id}, no need to bind it.")
                elif bound_to: # Conflict resolution.
                    if others == types.IGNORE: # Do not intefere with channels bound to other users.
                        logger.info(f"Channel {channel_id} bound to service {bound_to} and will not be re-bound.")
                    elif others == types.UNBIND: # Be spiteful: Unbind channels bound to other users but don't use them.
                        logger.info(f"Unbinding channel {channel_id} from service {bound_to} but this service will not use this channel.")
                        await self.http_api.unbind_service_from_channel(bound_to, channel_id)
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

                groupid2ids = await self.http_api.fetch_channel_group_dict(channel_id, self.client_id)
                logger.info(f'The channel {channel_id} has groups {groupid2ids}, adding these to self.group_lib.')
                self.group_lib.id2ids_mdown = {**self.group_lib.id2ids_mdown, **groupid2ids}
                await self.on_channel_init(channel_id)
                self._channels.append(channel_id)

            if len(self._channels) == 0:
                if len(self.config["channels"]) == 0:
                    logger.warning("No channels specified in the config. Channels will have to be created by your service in order to do anything.")
                else:
                    logger.warning("Channels were specified in the config, but they are all bound to other services and the 'others' option was not set to include")

            await self.send_service_login() # It is OK (somehow) to log in after all of this not before.

            channel_ids = await self.fetch_bound_channels()
            for c_id in channel_ids:
                if c_id not in self._channels:
                    if self.init_all_channels:
                        logger.info(f'Extra channel bound to this service on startup will be initialized  (self.init_all_channels is True): {c_id}')
                        await self.on_channel_init(c_id) # This channel was not initialized in the main "initialize channels" for loop because it is not in self._channels.
                    else:
                        logger.info(f'Extra channel bound to this service on startup will NOT be initialized (self.init_all_channels is False): {c_id}')
        else:
            async def _get_user_info():
                if self.service_mode:
                    raise Exception('Not in user mode.')
                user_info = await self.http_api.fetch_user_info()
                self.client_id = user_info.user_id
            await _get_user_info()
            await self.send_user_login()

        # Schedulers cannot be serialized so that you have to initialize it here
        self.scheduler = AsyncIOScheduler()

        # The details of access_token and refresh_token are managed by self.http_api
        self.scheduler.add_job(self.refresh_authentication, 'interval', seconds=self.refresh_interval)
        self.scheduler.add_job(self.authenticate, 'interval', seconds=self.authenticate_interval)
        self.scheduler.add_job(self.send_heartbeat, 'interval', seconds=self.heartbeat_interval)

        if self.log_file:
            logger.add(self.log_file, level=self.log_level, **self.log_retention)
        if self.error_log_file:
            logger.add(self.error_log_file, level=self.error_log_level, **self.log_retention)

        self.scheduler.start()
        logger.debug("Scheduler started.")

        await self.on_start()
        logger.debug("on_start() finished.")

        self.scheduler.add_job(self._on_checkin, 'interval', seconds=self.checkin_interval) # This check-in must be after on_start()

        await asyncio.gather(self.ws_client.receive(), self.listen_loop())

    async def user_join_service_channels(self, service_config_fname):
        """Joins service channels given a service config dict or JSON filename (use in user mode). Returns None"""
        if self.service_mode:
            logger.warning('Called user_join_service_channels when not in user mode.')
        if type(service_config_fname) is dict:
            s_config = service_config_fname
        else:
            with open(service_config_fname, 'r', encoding='utf-8') as f_obj:
                s_config = json.load(f_obj)
            channels = s_config.get('channels', [])
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
        Given a channel id, returns a list (of Character objects).

        This list includes:
          Real members (ids for a particular user-channel combination) who joined the channel with the given channel_id.
          Agent characters that have been created by this service; agent characters are not bound to any channel.
        """
        member_ids = await self.fetch_member_ids(channel_id, False)
        member_profiles = await self.fetch_character_profile(member_ids)
        agent_profiles = await self.fetch_agents()
        return member_profiles + agent_profiles

    ################################## Actuators #######################################

    def limit_len(self, txt, n):
        """Given the text and the maximum length, returns a string with a limited length.
        If the string is shortened "...<number of> chars" will be shown at the end."""
        if len(txt)>n:
            txt = txt[0:n]+'...'+str(len(txt))+' chars'
        return txt

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

    async def send_message(self, message, channel_id=None, sender=None, recipients=None, subtype=None, len_limit=None, file_display_name=None):
        """
        Sends a message down (or up if in user-mode). This function is very flexible. Returns None.

        Parameters:
          message: The message to send.
            If a string, the message will be a text message unless subtype is set.
              If not a text message, the string must either be a local filepath or an http(s) filepath.
            If a MessageBody or dict, the message sent will depend on it's fields/attributes as well as the overrides specified.
            If a pathlib.Path, will be a file/audio/image message by default.
          channel_id=None: The channel ids, if None message must be a MessageBody with the channel_id.
            Overrides message if not None
          sender=None: The character/user who's avatar appears to "speak" this message.
            Overrides message if not None
          recipients=None: List of character_ids.
            Overrides message if not None.
          subtype=None: Can be set to types.TEXT, types.IMAGE, types.AUDIO, types.FILE, or types.CARD
            If None, the subtype will be inferred.
          len_limit=None: Limit the length of large text messages.
          file_display_name: The name shown for downloadable files can be set to a value different than the filename.
            Sets the subtype to "types.FILE" if subtype is not specified.
        """

        async def _get_file_message_content(filepath, file_display_name=None, subtype=None):
            """Converts a filepath into a MessageContent object, uploading files if need be."""
            if type(filepath) is not str:
                filepath = filepath.as_posix() # For pathlib.paths.
            file_uri = await self.http_api.convert_to_url(filepath)
            size = None
            if file_uri != filepath:
                if os.path.exists(filepath):
                    size = os.stat(filepath).st_size
            ext = '.'+file_uri.lower().split('.')[-1]
            filename = file_display_name if file_display_name else filepath.replace('\\','/').split('/')[-1]
            if not subtype:
                subtype = types.IMAGE if ext in types.IMAGE_EXTS else (types.AUDIO if ext in types.AUDIO_EXTS else types.FILE)
            return MessageContent(filename=filename, size=size, path=file_uri), subtype

        if file_display_name:
            if not subtype:
                subtype = types.FILE
            if subtype != types.FILE:
                logger.warning(f'file_display_name is set, but the subtype is set to {subtype} not types.FILE')

        if type(message) is MessageBody:
            message = asdict(message)
        elif type(message) is str:
            if not subtype or subtype == types.TEXT:
                message = {'subtype':types.TEXT, 'content':MessageContent(text=message)}
            else:
                message = message.strip()
                mcontent, subtype = await _get_file_message_content(message, file_display_name=file_display_name, subtype=subtype)
                message = {'subtype':subtype, 'content':mcontent}
        elif type(message) in [pathlib.Path, pathlib.PosixPath, pathlib.PurePath, pathlib.PurePosixPath, pathlib.PureWindowsPath, pathlib.WindowsPath]:
            mcontent, subtype = await _get_file_message_content(message, file_display_name=file_display_name, subtype=subtype)
            message = {'subtype':subtype, 'content':mcontent}
        elif type(message) is dict:
            if 'link' in message and 'button' in message and 'text' in message:
                if not subtype:
                    subtype = types.CARD
                message = {'subtype':subtype, 'content': message} # Convert contents of a card into an actual card.
        if 'recipients' not in message and recipients is None:
            logger.error('None "recipients" (None as in not an empty list) but "recipients" not specified by the message. This may indicate that recipients was unfilled.')

        if 'content' not in message:
            raise Exception('Dict/MessageBody message with no "content" specified.')
        if type(message['content']) is dict:
            message['content'] = MessageContent(**message['content'])
        for xtra in ['timestamp', 'context', 'message_id']:
            if xtra in message:
                del message[xtra]
        if channel_id is not None:
            message['channel_id'] = channel_id
        if sender is not None:
            if type(sender) is Character:
                sender = sender.character_id
            message['sender'] = sender
        if recipients is not None:
            message['recipients'] = recipients

        if message.get('recipients'):
            message['recipients'] = await self._update_rec(message['recipients'], self.service_mode, message.get('channel_id'))
            if self.service_mode:
                message['sender'] = message['sender'] or 'no_sender'
            if len_limit and message['content'].text:
                message['content'].text = self.limit_len(message['content'].text, len_limit)

            if self.service_mode:
                return await self.ws_client.message_down(self.client_id, self.client_id,  **message)
            else:
                if 'sender' in message:
                    del message['sender'] # Message up messages have no sender, for some reason.
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
        if isinstance(payload_body, dict):
            payload_dict = {
                'type': payload_type,
                'request_id': str(uuid.uuid4()),
                'character_id': self.client_id,
                'body': payload_body
            }
        else: # Need to wrap non-dataclasses into a dataclass, in this case Payload, in order to use asdict() on them.
            payload_obj = Payload(
                type=payload_type,
                request_id=str(uuid.uuid4()),
                user_id=self.client_id,
                body=payload_body
            )
            try:
                payload_dict = asdict(payload_obj)
            except Exception as error_e: # Track down those pickle errors!
                _pr = logger.error
                print("asdict FAILURE on", payload_type, payload_body, error_e)
                try:
                    asdict(payload_body)
                    _pr('HUH? The payload body CAN be dictified?')
                except:
                    pass
                for k, v in payload_body.__dict__.items():
                    if type(v) in [str, int, bool, float]:
                        _pr('Elemetary type, no problem pickling:', k, v)
                    else:
                        try:
                            asdict(Payload(type=payload_type, request_id=str(uuid.uuid4()), user_id=self.client_id, body=v))
                            _pr('No problem pickling:', k, v)
                        except Exception as e:
                            _pr('UNDICTABLE part of __dict__ error:', k, 'Value is:', v, 'type is:', type(v), 'error is:', e)
                raise error_e
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
        if 'type' in payload_dict and payload_dict['type'] == types.MESSAGE_DOWN:
            payload_dict['service_id'] = self.client_id
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
        if self.service_mode: # 95% sure this extra line is just there because no one wanted to remove it.
            await self.ws_client.heartbeat()

    async def send_refresh(self, channel_id):
        """Sends a refresh given a channel_id. Returns the message sent. A user function."""
        if self.service_mode:
            logger.warning('This is a user function')
        return await self.ws_client.refresh_as_user(self.client_id, channel_id)

    async def do_channel_sync(self, channel_id):
        """Sends a refresh request "from" each user in this channel, which will refresh thier views.
        Accepts the channel id. returns None."""
        member_ids = await self.fetch_member_ids(channel_id)
        tasks = [self.ws_client.refresh_as_user(user_id, channel_id) for user_id in member_ids]
        await asyncio.gather(*tasks)

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
    async def update_agent(self, agent_id, avatar, description, name): """Calls self.http_api.update_agent using self.client_id."""; return await self.http_api.update_agent(self.client_id, agent_id, avatar, description, name)
    async def update_channel(self, channel_id, channel_name, channel_desc): """Calls self.http_api.update_channel."""; return await self.http_api.update_channel(channel_id, channel_name, channel_desc)
    async def bind_service_to_channel(self, channel_id): """Calls self.http_api.bind_service_to_channel"""; return await self.http_api.bind_service_to_channel(self.client_id, channel_id)
    async def unbind_service_from_channel(self, channel_id): """Calls self.http_api.unbind_service_from_channel"""; return await self.http_api.unbind_service_from_channel(self.client_id, channel_id)
    async def create_agent(self, name, avatar=None, description="No description"): """Calls self.http_api.create_agent using self.create_agent."""; return await self.http_api.create_agent(self.client_id, name, avatar, description)
    async def fetch_popular_channels(self): """Calls self.http_api.fetch_popular_channels."""; return await self.http_api.fetch_popular_channels()
    async def fetch_channel_list(self): """Calls self.http_api.fetch_channel_list."""; return await self.http_api.fetch_channel_list()
    async def fetch_member_ids(self, channel_id, raise_empty_list_err=False): """Calls self.http_api.fetch_member_ids using self.client_id."""; return await self.http_api.fetch_member_ids(channel_id, self.client_id, raise_empty_list_err=raise_empty_list_err)
    async def fetch_character_profile(self, character_id): """Calls self.http_api.fetch_character_profile"""; return await self.http_api.fetch_character_profile(character_id)
    async def fetch_service_id_list(self): """Calls self.http_api.fetch_service_id_list"""; return await self.http_api.fetch_service_id_list()
    async def fetch_agents(self): """Calls self.http_api.fetch_agents using self.client_id."""; return await self.http_api.fetch_agents(self.client_id)
    async def fetch_message_history(self, channel_id, limit=1024, before="null"): """Calls self.http_api.fetch_message_history."""; return await self.http_api.fetch_message_history(channel_id, limit, before)
    async def upload(self, filepath): """Calls self.http_api.upload. Note that uploads happen automatically for any function that accepts a filepath/url when given a local path."""; return await self.http_api.upload(filepath)
    async def download(self, source, full_path=None, auto_dir=None, overwrite=True, bytes=False, headers=None): """Calls self.http_api.download."""; return await self.http_api.download(source, full_path, auto_dir, overwrite, bytes, headers)

    async def create_channel_group(self, channel_id, group_name, members): """Calls self.http_api.create_channel_group."""; return await self.http_api.create_channel_group(channel_id, group_name, members)
    async def create_service_group(self, group_id, members): """Calls self.http_api.create_service_group."""; return await self.http_api.create_service_group(group_id, members)
    async def character_ids_of_channel_group(self, sender_id, channel_id, group_id): """Calls self.http_api.character_ids_of_channel_group"""; return await self.http_api.character_ids_of_channel_group(sender_id, channel_id, group_id)
    async def character_ids_of_service_group(self, group_id): """Calls self.http_api.character_ids_of_service_group"""; return await self.http_api.character_ids_of_service_group(group_id)
    async def update_channel_group(self, channel_id, group_id, members): """Calls self.http_api.update_channel_group."""; return await self.http_api.update_channel_group(channel_id, group_id, members)
    async def update_temp_channel_group(self, channel_id, members): """Calls self.http_api.update_temp_channel_group."""; return await self.http_api.update_temp_channel_group(channel_id, members)
    async def fetch_channel_temp_group(self, channel_id): """Calls self.http_api.fetch_channel_temp_group."""; return await self.http_api.fetch_channel_temp_group(channel_id, self.client_id)
    async def fetch_channel_group_list(self, channel_id): """Calls self.http_api.fetch_target_group."""; return await self.http_api.fetch_channel_group_list(channel_id, self.client_id)
    async def fetch_user_from_group(self, user_id, channel_id, group_id): """Calls self.http_api.fetch_user_from_group."""; return await self.http_api.fetch_user_from_group(user_id, channel_id, group_id)
    async def fetch_target_group(self, user_id, channel_id, group_id): """Calls self.http_api.fetch_target_group."""; return await self.http_api.fetch_target_group(user_id, channel_id, group_id)

    async def send_user_login(self): """Calls self.ws_client.user_login using self.http_api.access_token; Use for user mode."""; return await self.ws_client.user_login(self.http_api.access_token)
    async def send_service_login(self): """Calls self.ws_client.service_login using self.client_id and self.http_api.access_token."""; return await self.ws_client.service_login(self.client_id, self.http_api.access_token)
    async def send_update(self, data, target_client_id): """Calls self.ws_client.update"""; return await self.ws_client.update(data, self.client_id, target_client_id)
    async def send_characters(self, character_ids, channel_id, recipients): """Calls self.ws_client.update_character_list using self.client_id. Converts recipients to a group_id if a list."""; return await self.ws_client.update_character_list(await self._update_rec(character_ids, True), self.client_id, channel_id, await self._update_rec(recipients, True))
    async def send_buttons(self, buttons, channel_id, recipients): """Calls self.ws_client.update_buttons using self.client_id. Converts recipients to a group_id if a list."""; return await self.ws_client.update_buttons(buttons, self.client_id, channel_id, await self._update_rec(recipients, True))
    async def send_menu(self, menu_items, channel_id, recipients): """Calls self.ws_client.update_menu using self.client_id. Converts recipients to a group_id if a list."""; return await self.ws_client.update_menu(menu_items, self.client_id, channel_id, await self._update_rec(recipients, True))
    async def send_style(self, style_items, channel_id, recipients): """Calls self.ws_client.update_style using self.client_id. Converts recipients to a group_id if a list."""; return await self.ws_client.update_style(style_items, self.client_id, channel_id, await self._update_rec(recipients, True))

    async def send_join_channel(self, channel_id): """Calls self.ws_client.join_channel using self.client_id. Use for user mode."""; return await self.ws_client.join_channel(self.client_id, channel_id)
    async def send_leave_channel(self, channel_id): """Calls self.ws_client.leave_channel using self.client_id. Used for user mode."""; return await self.ws_client.leave_channel(self.client_id, channel_id)
    async def send_button_click(self, button_id, bottom_button_id, button_args, channel_id): """Calls self.ws_client.send_button_click using self.client_id. Used for user mode."""; await self.ws_client.send_button_click(button_id, bottom_button_id, button_args, channel_id, self.client_id, dry_run=False)
    async def send_menu_item_click(self, menu_item_id, bottom_button_id, button_args, the_message, channel_id): """Calls self.ws_client.send_menu_item_click using self.client_id. Used for user mode."""; await self.ws_client.send_menu_item_click(menu_item_id, bottom_button_id, button_args, the_message, channel_id, self.client_id, dry_run=False)

    ################################## Callback switchyards #######################################

    async def _on_checkin(self):
        """Called as a rate task, used to resync users, etc. Only called after on_start(). Returns None."""
        for channel_id in self._channels:
            await self.do_channel_sync(channel_id)

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
                raise Exception('Received an internal server error from the Websocket.')

        payload_body = payload_data['body']
        async def _group2ids(g_id):
            if g_id==types.SERVICE:
                return []
            if type(g_id) is not str:
                raise Exception('Group id not a string.')

            channel_id = payload_body['channel_id']
            use_sgroup = False
            use_cgroup = True
            try:
                if use_sgroup:
                    out_sgroup = await self.http_api.character_ids_of_service_group(g_id)
                else:
                    out_sgroup = []
                sgroup_err = None
            except Exception as e:
                out_sgroup = []
                sgroup_err = e
            try:
                if use_cgroup:
                    use_sender_when_possible = True
                    the_id = self.client_id
                    if 'sender' in payload_body and use_sender_when_possible:
                        the_id = payload_body['sender']
                    out_cgroup = await self.http_api.character_ids_of_channel_group(the_id, channel_id, g_id)
                else:
                    out_cgroup = []
                cgroup_err = None
            except Exception as e:
                out_cgroup = []
                cgroup_err = e
            out = out_sgroup+out_cgroup
            logger.info(f'Extract character_ids from group: {g_id} service_group {"error "+str(sgroup_err) if sgroup_err else "no error"}, channel_group {"error "+str(cgroup_err) if cgroup_err else "no error"}. Id list: {out}')
            if len(out)==0:
                logger.warning('Neither the channel nor service group queries were able to find any members in the group.')
            return out

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
                await self.on_message_down(payload.body)
            elif payload.type == types.UPDATE:
                # First convert the content into an UpdateItem:
                subty = payload.body['subtype']
                content0 = payload.body['content'] # This dict needs to be converted into a list of UpdateItem's
                empty_elem_dict = {'character':None, 'button':None, 'channel_info':None, 'canvas_item':None, 'style_item':None, 'menu_item':None}
                def _make_elem(d):
                    return UpdateItem(**{**empty_elem_dict, **d})
                content = []
                if subty == types.UPDATE_CHARACTERS:
                    content = [_make_elem({'character':Character({**c, **c['character_context']})}) for c in content0['characters']]
                elif subty == types.UPDATE_CHANNEL_INFO:
                    content = [_make_elem({'channel_info':ChannelInfo(content0)})]
                elif subty == types.UPDATE_CANVAS:
                    content = [_make_elem({'canvas_item':CanvasItem(**ce)}) for ce in content0]
                elif subty == types.UPDATE_MENU:
                    content = [_make_elem({'menu_item':MenuItem(**ce)}) for ce in content0]
                elif subty == types.UPDATE_BUTTONS:
                    buttons = []
                    for b in content0:
                        if b.get('arguments'): # For some reason this wasn't bieng converted to a InputComponent data.
                            b['arguments'] = [InputComponent(**a) for a in b['arguments']]
                        buttons.append(Button(**b))
                    content = [_make_elem({'button':b}) for b in buttons]
                elif subty == types.UPDATE_STYLE:
                    content = [_make_elem({'style_item':StyleItem(**b)}) for b in content0]
                else:
                    logger.error(f'Unknown recieved update subtype, cannot encode: {subty}')
                    content = [] # Unknown.

                # Then make an update and call the update switchyard:
                recipients = []
                if 'recipients' in payload.body and payload.body['recipients'] not in [types.SERVICE, 'null', '', None, False]:
                    r_group = payload.body['recipients']
                    if type(r_group) in [list, tuple]:
                        recipients = r_group
                    else:
                        try:
                            recipients = await self.character_ids_of_service_group(r_group) # Convert to list.
                            if not recipients:
                                recipients = f'WARNING: empty list for group_id {r_group}'
                        except Exception as e:
                            recipients = [f"ERROR getting character_ids for group_id: {r_group}"]
                update = UpdateBody(**{**payload.body, **{'content':content, 'recipients':recipients}})
                await self.on_update(update)
            elif payload.type == types.MESSAGE_UP:
                await self.on_message_up(payload.body)
            elif payload.type == types.ACTION:
                await self.on_action(payload_body)
            elif payload.type == types.COPY:
                await self.on_copy_client(payload.body)
            elif payload.type == types.REFRESH: # TODO: Not used, actions actions with refresh. But will direct refresh be the future in the platform?
                await self.on_refresh(payload.body)
            else:
                logger.warning(f"Unknown payload received: {payload}; DATA: {payload_data}")
                await self.on_unknown_payload(payload)
        else:
            logger.error(f"Unknown payload without type: {payload_data}")

    async def on_action(self, action_data):
        """
        Accepts an action object, as a dict, from a user. Returns None.
        Calls the corresponding method to handle different subtypes of action.
        Example methods called:
          on_button_click(), on_join_channel()
        """
        # Note: putting dataclass constructors here, instead of attempting to do it all at once, makes it much easier to debug.
        subtype = action_data['subtype']
        if subtype == types.JOIN_CHANNEL:
            await self.on_join_channel(JoinBody(**action_data))
        elif subtype == types.LEAVE_CHANNEL:
            await self.on_leave_channel(LeaveBody(**action_data))
        elif subtype == types.BUTTON_CLICK:
            action_data = types._recv_tmp_convert('on_button_click', action_data)
            await self.on_button_click(ButtonClick(**action_data))
        elif subtype == types.MENU_ITEM_CLICK:
            action_data = types._recv_tmp_convert('on_menu_item_click', action_data)
            await self.on_menu_item_click(MenuItemClick(**action_data))
        elif subtype == types.REFRESH:
            await self.on_refresh(RefreshBody(**action_data))
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
        By default, if self.db_config has been set, a MoobiusStorage is created in self.channel_storages.
        Also does a channel sync by default.
        """
        if self.db_config: # Optional storage.
            self.channel_storages[channel_id] = MoobiusStorage(self.client_id, channel_id, self.db_config)
        await self.do_channel_sync(channel_id)
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

    async def on_refresh(self, refresh: RefreshBody):
        """
        This callback accepts a "Copy" request from the user. Returns None.
        Example RefreshObject object:
        >>> moobius.RefreshBody(channel_id=<channel_id>, context={})"""
        logger.debug("on_refresh")

    async def on_join_channel(self, action):
        """
        This callback happens when the user joins a channel. Accepts an Action object. Returns None.
        Commonly used to inform everyone about this new user and update everyone's character list.
        Example Action object:
        >>> moobius.Action(subtype="join_channel", channel_id=<channel id>, sender=<user id>, context={})"""
        logger.debug("on_action join_channel")

    async def on_leave_channel(self, action):
        """
        Called when the user leaves a channel. Accepts an Action object. Returns None.
        Commonly used to update everyone's character list.
        Example Action object:
        >>> moobius.Action(subtype="leave_channel", channel_id=<channel id>, sender=<user id>, context={})"""
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

    async def on_unknown_payload(self, payload: Payload):
        """A catch-all for handling unknown Payloads. Accepts a Payload that has not been recognized by the other handlers. Returns None."""
        pass

    ############################## User mode-specific simple callbacks (also commonly overridden) #######################################

    async def on_message_down(self, message: MessageBody):
        """Callback when the user recieves a message. Accepts the service's MessageBody.
           Use for user mode. Returns None."""
        logger.debug(f"MessageDown received: {message}")

    async def on_update_characters(self, update: UpdateBody):
        """Callback when the user recieves the character list. Accepts the service's Update. One of the multiple update callbacks. Returns None.
           Use for user mode."""
        logger.debug("on_update_character_list")

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
        http_server_uri = self.config["http_server_uri"]
        ws_server_uri = self.config["ws_server_uri"]
        email = self.config["email"]
        num_channels = len(self._channels)
        agsv = 'Service' if self.service_mode else 'User-mode'
        return f'moobius.SDK({agsv}; config=config={fname}, http_server_uri={http_server_uri}, ws_server_uri={ws_server_uri}, ws={ws_server_uri}, email={email}, password=****, num_channels={num_channels})'
    def __repr__(self):
        return self.__str__()

###################################################### Deprecated functions ###########################################
deprecated_functions = {'create_character':'create_agent',
                        'fetch_real_character_ids':'fetch_member_ids',
                        'update_character':'update_agent',
                        'fetch_member_profile':'fetch_character_profile',
                        'fetch_service_characters':'fetch_agents',
                        'send_character_list':'send_characters',
                        'upload_file':'upload', 'download_file':'download'}

def _deprecated_wrap(f, old_name, new_name):
    """Accepts a function, a deprecated old name, and a new name. Returns the function with a deprecation logger warning."""
    def out(*args, **kwargs):
        logger.warning(f'Deprecated function {old_name}, use {new_name} instead.')
        return f(*args, **kwargs)
    return out

for old_name, new_name in deprecated_functions.items():
    new_f = getattr(Moobius, new_name)
    setattr(Moobius, old_name, _deprecated_wrap(old_name, new_name, new_f))
