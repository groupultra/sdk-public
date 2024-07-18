# SDK interface, agent or service. Automatically wraps the two platform APIs (HTTP and Socket)

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
from moobius.types import MessageContent, MessageBody, Action, Button, ButtonClick, ButtonArgument, ButtonClickArgument, Payload, MenuClick, Update, UpdateElement, Character, ChannelInfo, CanvasElement, StyleElement, ContextMenuElement
from moobius.database.storage import MoobiusStorage
from moobius import utils, types
from loguru import logger

utils.maybe_make_template_files({})
strict_kwargs = False # If True all functions (except __init__) with more than one non-self arg will require kwargs. If False a default ordering will be used.


class ServiceGroupLib():
    """Converts a list of character_ids into a service or channel group id, creating one if need be.
       The lookup is O(n) so performance issues at extremly large list sizes are a theoretical possibility."""

    def __init__(self):
        logger.info(f'Initialized new, empty ServiceGroupLib on process {os.getpid()}')
        self.id2ids_mdown = {} # Message down creates service group with /service/group/create
        self.ids2id_mdown = {}
        self.id2ids_mup = {}
        self.ids2id_mup = {}
        self.alock = asyncio.Lock()

    async def convert_list(self, http_api, character_ids, is_message_down, channel_id=None):
        """
        Converts a list to single group id unless it is already a group id.

        Parameters:
          http_api: The http_api client in Moobius
          character_ids: List of ids. If a string, treated as a one element list.
          is_message_down: True = message_down (Service sends message), False = message_up (Agent sends message).
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

    def __init__(self, config_path, db_config_path, is_agent=False, **kwargs):
        """
        Initialize a service or agent object.

        Parameters:
          config_path: The path of the agent or service config file. Can also be a dict.
          db_config_path: The path of the database config file.
            Can also be a dict in which case no file will be loaded.
          is_agent=False: True for an agent, False for a service.
            Agents and services have slight differences in auth and how the platform reacts to them, etc.

        No return value.

        Example:
          >>> service = SDK(config_path="./config/service.json", db_config_path="./config/database.json", is_agent=False)
        """
        self._log_level = kwargs.get("terminal_log_level", "INFO")
        utils.set_terminal_logger_level(self._log_level)

        self.config_path = config_path
        self.is_agent = is_agent

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
        else:
            raise Exception('db_config_path not understood')

        http_server_uri = self.config["http_server_uri"]
        ws_server_uri = self.config["ws_server_uri"]
        email = self.config["email"]
        password = self.config["password"]
        the_id = self.config.get("service_id", "")
        if the_id != '' and the_id and self.is_agent:
            raise Exception('Agents cannot have a "service_id" in there JSON config.')
        if not self.is_agent:
            self.client_id = self.config.get("service_id", "")

        self.channels = {} # Generally filled up by self.initialize_channel().
        self.group_lib = ServiceGroupLib()

        self.http_api = HTTPAPIWrapper(http_server_uri, email, password)
        # TODO: Is it easier just to pass in the socket.send_agent_login function rather than self.send_agent_login?
        self.ws_client = WSClient(ws_server_uri, on_connect=self.send_agent_login if self.is_agent else self.send_service_login, handle=self.handle_received_payload)

        self.queue = aioprocessing.AioQueue()

        self.refresh_interval = 6 * 60 * 60             # 24h expire, 6h refresh
        self.authenticate_interval = 7 * 24 * 60 * 60   # 30d expire, 7d refresh
        self.heartbeat_interval = 30                    # 30s heartbeat
        self.checkin_interval = 90
        self.log_retention = kwargs.get('log_retention', {'rotation':"1 day", 'retention':"7 days"})

        self.scheduler = None

        self.log_file = kwargs.get('log_file')
        self.error_log_file = kwargs.get('error_log_file')
        self.init_all_channels = kwargs.get('initialize_all_bound_channels')

    async def start(self):
        """
        Start the Service/Agent. start() fns are called with wand.run. There are 6 steps:
          1. Authenticate.
          2. Connect to the websocket server.
          3. (if a Service) Bind the Service to the channels. If there is no service_id in the config file, create a new service and update the config file.
          4. Start the scheduler, run refresh(), authenticate(), send_heartbeat() periodically.
          5. Call the on_start() callback (override this method to perform your own initialization tasks).
          6. Start listening to the websocket and the Wand.

        No parameters or return value.
        """
        utils.set_terminal_logger_level(self._log_level)

        logger.debug("Starting agent..." if self.is_agent else "Starting service...")

        await self.authenticate()
        await self.ws_client.connect()
        logger.debug("Connected to websocket server.")

        if self.is_agent:
            async def _get_agent_info():
                if not self.is_agent:
                    raise Exception('Not an agent.')
                agent_info = await self.http_api.fetch_user_info()
                self.client_id = agent_info.user_id
            await _get_agent_info()
            await self.send_agent_login()
        else:
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
                await self.initialize_channel(channel_id)

            if not self.channels:
                logger.error("All channels are used up by other services and the 'others' option is not set to 'include' to steal them back.")
                return

            await self.send_service_login() # It is OK (somehow) to log in after all of this not before.

        # Schedulers cannot be serialized so that you have to initialize it here
        self.scheduler = AsyncIOScheduler()

        # The details of access_token and refresh_token are managed by self.http_api
        self.scheduler.add_job(self.refresh, 'interval', seconds=self.refresh_interval)
        self.scheduler.add_job(self.authenticate, 'interval', seconds=self.authenticate_interval)
        self.scheduler.add_job(self.send_heartbeat, 'interval', seconds=self.heartbeat_interval)

        if self.log_file:
            logger.add(self.log_file, level="DEBUG", **self.log_retention)
        if self.error_log_file:
            logger.add(self.error_log_file, level="ERROR", **self.log_retention)

        self.scheduler.start()
        logger.debug("Scheduler started.")

        if not self.is_agent:
            channel_ids = await self.fetch_bound_channels()
            for c_id in channel_ids:
                if c_id not in self.channels:
                    if self.init_all_channels:
                        logger.info(f'Extra channel bound to this service on startup will be initialized  (self.init_all_channels is True): {c_id}')
                        await self.initialize_channel(c_id) # This channel was not initialized in the main "initialize channels" for loop because it is not in self.channels.
                    else:
                        logger.info(f'Extra channel bound to this service on startup will NOT be initialized (self.init_all_channels is False): {c_id}')

        await self.on_start()
        logger.debug("on_start() finished.")

        self.scheduler.add_job(self.checkin, 'interval', seconds=self.checkin_interval) # This check-in must be after on_start()

        await asyncio.gather(self.ws_client.receive(), self.listen_loop())

    async def agent_join_service_channels(self, service_config_fname):
        """Joins service channels given by service config filename."""
        if not self.is_agent:
            logger.warning('Called agent_join_service_channels when not an agent.')
        if type(service_config_fname) is dict:
            s_config = service_config_fname
        else:
            with open(service_config_fname, 'r', encoding='utf-8') as f_obj:
                s_config = json.load(f_obj)
            channels = s_config.get('channels', [])
        if len(channels)==0:
            logger.warning('No channels for Agent to join.')
        else:
            logger.info(f'Agent joining Service default channels (if not already joined). Will not join to any extra channels: {channels}')

        try:
            ch1 = await self.http_api.this_user_channels()
        except Exception as e:
            logger.warning(f'Error fetching channels this user is in: {e}')
            ch1 = []
        for channel_id in channels:
            if channel_id not in ch1:
                try:
                    chars = await self.fetch_real_character_ids(channel_id, raise_empty_list_err=False)
                except Exception as e:
                    logger.warning(f'fetch_real_character_ids failed: {e}. Channel will be joined')
                    chars = []
                try:
                    if type(chars) is not list or self.client_id not in chars:
                        await self.send_join_channel(channel_id)
                    else:
                        logger.info(f'Agent already in channel {channel_id}, no need to join.')
                except Exception as e:
                    logger.warning(f'Agent error joining channel: {e}')

    ################################## Query functions #######################################

    async def fetch_service_id_each_channel(self):
        """Returns a dict of which service_id is each channel_id bound to. Channels can only be bound to a single service.
           Channels not bound to any service will not be in the dict."""
        service_list = await self.http_api.fetch_service_id_list()
        channelid2serviceid = {} # Channels can only be bound to a SINGLE service.
        for service in service_list:
            for channel_id in service["channel_ids"]:
                channelid2serviceid[channel_id] = service['service_id']
        return channelid2serviceid

    async def fetch_bound_channels(self):
        """Returns a list of channels this Service is bound to."""
        ch_id2s_id = await self.fetch_service_id_each_channel()
        channel_ids = []
        for channel_id, service_id in ch_id2s_id.items():
            if service_id == self.client_id:
                channel_ids.append(channel_id)
        return channel_ids

    async def fetch_characters(self, channel_id):
        """Returns a list (or Character objects) with both the real characters bound to channel_id
        as well as fake virtual characters bound to, not a channel, but to service self.client_id."""
        real_character_ids = await self.fetch_real_character_ids(channel_id, False)
        real_characters = await self.fetch_character_profile(real_character_ids)
        service_characters = await self.fetch_service_characters()
        return real_characters + service_characters

    ################################## Actuators #######################################

    def _convert_message_content(self, subtype, content):
        """Converts message content, which can be a string (for text messages), to a MessageContent object."""
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

    async def initialize_channel(self, channel_id):
        """Creates a MoobiusStorage object for a channel given by channel_id. Commonly overridden. Returns None."""
        the_channel = MoobiusStorage(self.client_id, channel_id, db_config=self.db_config)
        self.channels[channel_id] = the_channel

    async def checkin(self):
        """Called as a rate task, used to resync users, etc. Only called after on_start()"""
        for channel_id in self.channels.keys():
            await self.checkin_channel(channel_id)

    async def checkin_channel(self, channel_id):
        """This is called on startup and on reconnect"""
        if channel_id == list(self.channels.keys())[0]:
            logger.info('checkin_channel not overriden, occasional desyncs are possible.')

    def limit_len(self, txt, n):
        if len(txt)>n:
            txt = txt[0:n]+'...'+str(len(txt))+' chars'
        return txt

    async def send_message(self, the_message, channel_id=None, sender=None, recipients=None, subtype=None, len_limit=None, file_display_name=None):
        """
        Sends a message. Commonly used by both Services and Agents.

        Parameters:
          the_message:
            If a string, the message will be a text message unless subtype is set.
              If not a text message, the string must either be a local filepath or an http(s) filepath.
            If a MessageBody or dict, the message sent will depend on it's fields/attributes as well as the overrides specified.
            If a pathlib.Path, will be a file/audio/image message by default.
          channel_id=None: The channel ids, if None the_message must be a MessageBody with the channel_id.
            Overrides the_message if not None
          sender=None: The character/user who's avatar appears to "speak" this message.
            Overrides the_message if not None
          recipients=None: List of character_ids.
            Overrides the_message if not None.
          subtype=None: Can be set to types.TEXT, types.IMAGE, types.AUDIO, types.FILE, or types.CARD
            If None, the subtype will be inferred.
          len_limit=None: Limit the length of large text messages.
          file_display_name: The name shown for downloadable files can be set to a value different than the filename.
            Sets the subtype to "types.FILE" if subtype is not specified.
        """

        async def _get_file_message_content(filepath, file_display_name=None, subtype=None):
            """Converts filepath into a MessageContent object, uploading files if need be."""
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

        if type(the_message) is MessageBody:
            the_message = asdict(the_message)
        elif type(the_message) is str:
            if not subtype or subtype == types.TEXT:
                the_message = {'subtype':types.TEXT, 'content':MessageContent(text=the_message)}
            else:
                the_message = the_message.strip()
                mcontent, subtype = await _get_file_message_content(the_message, file_display_name=file_display_name, subtype=subtype)
                the_message = {'subtype':subtype, 'content':mcontent}
        elif type(the_message) in [pathlib.Path, pathlib.PosixPath, pathlib.PurePath, pathlib.PurePosixPath, pathlib.PureWindowsPath, pathlib.WindowsPath]:
            mcontent, subtype = await _get_file_message_content(the_message, file_display_name=file_display_name, subtype=subtype)
            the_message = {'subtype':subtype, 'content':mcontent}
        elif type(the_message) is dict:
            if 'link' in the_message and 'button' in the_message and 'text' in the_message:
                if not subtype:
                    subtype = types.CARD
                the_message = {'subtype':subtype, 'content': the_message} # Convert contents of a card into an actual card.
        if 'recipients' not in the_message and recipients is None:
            logger.error('None "recipients" (None as in not an empty list) but "recipients" not specified by the_message. This may indicate that recipients was unfilled.')

        if 'content' not in the_message:
            raise Exception('Dict/MessageBody message with no "content" specified.')
        if type(the_message['content']) is dict:
            the_message['content'] = MessageContent(**the_message['content'])
        for xtra in ['timestamp', 'context', 'message_id']:
            if xtra in the_message:
                del the_message[xtra]
        if channel_id is not None:
            the_message['channel_id'] = channel_id
        if sender is not None:
            the_message['sender'] = sender
        if recipients is not None:
            the_message['recipients'] = recipients

        if the_message.get('recipients'):
            the_message['recipients'] = await self._update_rec(the_message['recipients'], not self.is_agent, the_message.get('channel_id'))
            if not self.is_agent:
                the_message['sender'] = the_message['sender'] or 'no_sender'
            if len_limit and the_message['content'].text:
                the_message['content'].text = self.limit_len(the_message['content'].text, len_limit)

            if self.is_agent:
                if 'sender' in the_message:
                    del the_message['sender'] # Message up messages have no sender, for some reason.
                return await self.ws_client.message_up(self.client_id, self.client_id, **the_message)
            else:
                return await self.ws_client.message_down(self.client_id, self.client_id,  **the_message)
        else:
            logger.warning('Empty or None recipients, no message will be sent.')

    async def send(self, payload_type, payload_body):
        """
        Send any kind of payload, including message_down, update, update_characters, update_channel_info, update_canvas, update_buttons, update_style, and heartbeat.
        Rarely used except internally, but provides the most flexibility for those special occasions.

        Parameters:
          payload_type (str): The type of the payload.
          payload_body (dict or str): The body of the payload.
            Strings will be converted into a Payload object.

        No return value.
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
        #logger.info('SELF>SEND:', payload_dict) # This can be useful but also gets a bit lengthy.
        if 'type' in payload_dict and payload_dict['type'] == types.MESSAGE_DOWN:
            payload_dict['service_id'] = self.client_id
        if 'type' in payload_dict and (payload_dict['type'] == types.MESSAGE_UP or payload_dict['type'] == types.MESSAGE_DOWN):
            ws_client.send_tweak(payload_dict) # TODO: what is this line for?
        await self.ws_client.send(payload_dict)

    async def send_button_click(self, channel_id, button_id, button_args):
        """
        Use to send a request to ask for a button call.

        Parameters:
          channel_id (str): Which channel.
          button_id (str): Which button.
          button_args (list of k-v pairs, not a dict): What about said button should be fetched?

        No return value.
        """
        button_click_instance = ButtonClick(
            button_id=button_id,
            channel_id=channel_id,
            sender=self.client_id,
            arguments=[ButtonClickArgument(name=arg[0], value=arg[1]) for arg in button_args],
            context={}
        )
        await self.send("button_click", button_click_instance)

    async def send_heartbeat(self):
        """Sends a heartbeat to the server. Return None"""
        await self.ws_client.heartbeat()
        if not self.is_agent: # 95% sure this extra line is just there because no one wanted to remove it.
            await self.ws_client.heartbeat()

    async def create_channel(self, channel_name, channel_desc, bind=True):
        """Create a channel with the provided name and description and binds self.client_id (the service_id) to it.
           By default bind is True, which means the service connects itself to the channel.
           A Service function. Returns the channel id."""
        channel_id = await self.http_api.create_channel(channel_name, channel_desc)
        if bind:
            await self.http_api.bind_service_to_channel(self.client_id, channel_id)  # may already be binded to the service itself
        return channel_id

    async def send_update_canvas(self, channel_id, canvas_elements, recipients):
        """Updates the canvas given a channel_id, a list of CanvasElements (which have text and/or images), and recipients."""
        if type(canvas_elements) is dict or type (canvas_elements) is CanvasElement:
            canvas_elements = [canvas_elements]
        canvas_elements = [dataclasses.replace(elem) for elem in canvas_elements]
        for elem in canvas_elements:
            if elem.path:
                elem.path = await self.http_api.convert_to_url(elem.path)
        return await self.ws_client.update_canvas(self.client_id, channel_id, canvas_elements, await self._update_rec(recipients, True))


    ################################## Single-line functions #######################################
    async def _update_rec(self, recipients, is_m_down, channel_id=None):
        """Pass in await self._update_rec(recipients) into "recipients".
           Converts lists into group_id strings, creating a group if need be."""
        return await self.group_lib.convert_list(self.http_api, recipients, is_m_down, channel_id)

    async def refresh(self): """Calls self.http_api.refresh."""; return await self.http_api.refresh()
    async def authenticate(self): """Calls self.http_api.authenticate."""; return await self.http_api.authenticate()
    async def sign_up(self): """Calls self.http_api.sign_up."""; return await self.http_api.sign_up()
    async def sign_out(self): """Calls self.http_api.sign_out."""; return await self.http_api.sign_out()
    async def update_current_user(self, avatar, description, name): """Calls self.http_api.update_current_user."""; return await self.http_api.update_current_user(avatar, description, name)
    async def update_character(self, character_id, avatar, description, name): """Calls self.http_api.update_character using self.client_id."""; return await self.http_api.update_character(self.client_id, character_id, avatar, description, name)
    async def update_channel(self, channel_id, channel_name, channel_desc): """Calls self.http_api.update_channel."""; return await self.http_api.update_channel(channel_id, channel_name, channel_desc)
    async def bind_service_to_channel(self, channel_id): """Calls self.http_api.bind_service_to_channel"""; return await self.http_api.bind_service_to_channel(self.client_id, channel_id)
    async def unbind_service_from_channel(self, channel_id): """Calls self.http_api.unbind_service_from_channel"""; return await self.http_api.unbind_service_from_channel(self.client_id, channel_id)
    async def create_character(self, name, avatar=None, description="No description"): """Calls self.http_api.create_character using self.create_character."""; return await self.http_api.create_character(self.client_id, name, avatar, description)
    async def fetch_popular_channels(self): """Calls self.http_api.fetch_popular_channels."""; return await self.http_api.fetch_popular_channels()
    async def fetch_channel_list(self): """Calls self.http_api.fetch_channel_list."""; return await self.http_api.fetch_channel_list()
    async def fetch_real_character_ids(self, channel_id, raise_empty_list_err=True): """Calls self.http_api.fetch_real_character_ids using self.client_id."""; return await self.http_api.fetch_real_character_ids(channel_id, self.client_id, raise_empty_list_err=raise_empty_list_err)
    async def fetch_character_profile(self, character_id): """Calls self.http_api.fetch_character_profile"""; return await self.http_api.fetch_character_profile(character_id)
    async def fetch_service_id_list(self): """Calls self.http_api.fetch_service_id_list"""; return await self.http_api.fetch_service_id_list()
    async def fetch_service_characters(self): """Calls self.http_api.fetch_service_characters using self.client_id."""; return await self.http_api.fetch_service_characters(self.client_id)
    async def upload_file(self, filepath): """Calls self.http_api.upload_file. Note that uploads happen automatically for any function that accepts a filepath/url when given a local path."""; return await self.http_api.upload_file(filepath)
    async def download_file(self, url, filepath, assert_no_overwrite=False, headers=None): """Calls self.http_api.download_file"""; return await self.http_api.download_file(url, filepath, assert_no_overwrite=assert_no_overwrite, headers=headers)
    async def fetch_message_history(self, channel_id, limit=1024, before="null"): """Calls self.http_api.fetch_message_history."""; return await self.http_api.fetch_message_history(channel_id, limit, before)
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

    async def send_agent_login(self): """Calls self.ws_client.agent_login using self.http_api.access_token; one of the agent vs service differences."""; return await self.ws_client.agent_login(self.http_api.access_token)
    async def send_service_login(self): """Calls self.ws_client.service_login using self.client_id and self.http_api.access_token; one of the agent vs service differences."""; return await self.ws_client.service_login(self.client_id, self.http_api.access_token)
    async def send_update(self, target_client_id, data): """Calls self.ws_client.update"""; return await self.ws_client.update(self.client_id, target_client_id, data)
    async def send_update_character_list(self, channel_id, character_list, recipients): """Calls self.ws_client.update_character_list using self.client_id. Converts recipients to a group_id if a list."""; return await self.ws_client.update_character_list(self.client_id, channel_id, await self._update_rec(character_list, True), await self._update_rec(recipients, True))
    async def send_update_channel_info(self, channel_id, channel_info): """Calls self.ws_client.update_channel_info using self.client_id."""; return await self.ws_client.update_channel_info(self.client_id, channel_id, channel_info)
    async def send_update_buttons(self, channel_id, buttons, recipients): """Calls self.ws_client.update_buttons using self.client_id. Converts recipients to a group_id if a list."""; return await self.ws_client.update_buttons(self.client_id, channel_id, buttons, await self._update_rec(recipients, True))
    async def send_update_context_menu(self, channel_id, menu_elements, recipients): """Calls self.ws_client.update_context_menu using self.client_id. Converts recipients to a group_id if a list."""; return await self.ws_client.update_context_menu(self.client_id, channel_id, menu_elements, await self._update_rec(recipients, True))
    async def send_update_style(self, channel_id, style_content, recipients): """Calls self.ws_client.update_style using self.client_id. Converts recipients to a group_id if a list."""; return await self.ws_client.update_style(self.client_id, channel_id, style_content, await self._update_rec(recipients, True))
    async def send_fetch_characters(self, channel_id): """Calls self.ws_client.fetch_characters using self.client_id."""; return await self.ws_client.fetch_characters(self.client_id, channel_id)
    async def send_fetch_buttons(self, channel_id): """Calls self.ws_client.fetch_buttons using self.client_id."""; return await self.ws_client.fetch_buttons(self.client_id, channel_id)
    async def send_fetch_style(self, channel_id): """Calls self.ws_client.fetch_style using self.client_id."""; return await self.ws_client.fetch_style(self.client_id, channel_id)
    async def send_fetch_canvas(self, channel_id): """Calls self.ws_client.fetch_canvas using self.client_id."""; return await self.ws_client.fetch_canvas(self.client_id, channel_id)
    async def send_fetch_channel_info(self, channel_id): """Calls self.ws_client.fetch_channel_info using self.client_id."""; return await self.ws_client.fetch_channel_info(self.client_id, channel_id)
    async def send_join_channel(self, channel_id): """Calls self.ws_client.join_channel using self.client_id."""; return await self.ws_client.join_channel(self.client_id, channel_id)
    async def send_leave_channel(self, channel_id): """Calls self.ws_client.leave_channel using self.client_id. The Agent version of self.unbind_service_from_channel."""; return await self.ws_client.leave_channel(self.client_id, channel_id)

    ################################## Callback switchyards #######################################

    @logger.catch
    async def listen_loop(self):
        """Listens to the wand (in an infinite loop so) that the wand could send spells to the service at any time (not only before the service is started).
           Uses asyncio.Queue."""
        while True:
            obj = await self.queue.coro_get()
            await self.on_spell(obj)

    @logger.catch
    async def handle_received_payload(self, payload):
        """
        Decode the received (websocket) payload, a JSON string, and call the handler based on p['type']. Returns None.
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

        if 'recipients' not in payload_body:
            payload_body['recipients'] = []
        else:
            rec_group = payload_body['recipients']
            payload_body['recipients'] = await _group2ids(rec_group)

        if 'type' in payload_data:
            if 'sender' not in payload_body and payload_body.get('context',{}).get('sender'):
                payload_body['sender'] = payload_body['context']['sender'] # Need a 'sender' key to make it a MessageBody or ButtonClick dataclass.
            if payload_data['type'] == types.MENU_CLICK:
                if 'message_id' not in payload_data['body']: # Need a 'message_id' key to make it a MenuClick.
                    payload_data['body']['message_id'] = ""
            payload = from_dict(data_class=Payload, data=payload_data) # Brittle type inference.
            if payload.type == types.MESSAGE_DOWN:
                await self.on_message_down(payload.body)
            elif payload.type == types.UPDATE:
                # First convert the content into an UpdateElement:
                subty = payload.body['subtype']
                content0 = payload.body['content'] # This dict needs to be converted into a list of UpdateElement's
                empty_elem_dict = {'character':None, 'button':None, 'channel_info':None, 'canvas_element':None, 'style_element':None, 'context_menu_element':None}
                def _make_elem(d):
                    return UpdateElement(**{**empty_elem_dict, **d})
                content = []
                if subty == types.UPDATE_CHARACTERS:
                    content = [_make_elem({'character':Character({**c, **c['character_context']})}) for c in content0['characters']]
                elif subty == types.UPDATE_CHANNEL_INFO:
                    content = [_make_elem({'channel_info':ChannelInfo(content0)})]
                elif subty == types.UPDATE_CANVAS:
                    content = [_make_elem({'canvas_element':CanvasElement(**ce)}) for ce in content0]
                elif subty == types.UPDATE_CONTEXT_MENU:
                    content = [_make_elem({'context_menu_element':ContextMenuElement(**ce)}) for ce in content0]
                elif subty == types.UPDATE_BUTTONS:
                    buttons = []
                    for b in content0:
                        if b.get('arguments'): # For some reason this wasn't bieng converted to a ButtonArgument data.
                            b['arguments'] = [ButtonArgument(**a) for a in b['arguments']]
                        buttons.append(Button(**b))
                    content = [_make_elem({'button':Button(**b)}) for b in content0]
                elif subty == types.UPDATE_STYLE:
                    content = [_make_elem({'style_element':StyleElement(**b)}) for b in content0]
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
                update = Update(**{**payload.body, **{'content':content, 'recipients':recipients}})
                await self.on_update(update)
            elif payload.type == types.MESSAGE_UP:
                await self.on_message_up(payload.body)
            elif payload.type == types.ACTION:
                await self.on_action(payload.body)
            elif payload.type == types.BUTTON_CLICK:
                await self.on_button_click(payload.body)
            elif payload.type == types.MENU_CLICK:
                await self.on_context_menu_click(payload.body)
            elif payload.type == types.COPY:
                await self.on_copy_client(payload.body)
            else:
                logger.warning(f"Unknown payload received: {payload}; DATA: {payload_data}")
                await self.on_unknown_payload(payload)
        else:
            logger.error(f"Unknown payload without type: {payload_data}")

    async def on_action(self, action: Action):
        """
        Handles an action (Action object) from a user. Returns None.
        Calls the corresponding method to handle different subtypes of action.
        Example methods called:
          on_fetch_service_characters(), on_fetch_buttons(), on_fetch_canvas(), on_join_channel(), on_leave_channel(), on_fetch_channel_info()
        Service function.
        """
        if action.subtype == types.FETCH_CHARACTERS:
            await self.on_fetch_service_characters(action)
        elif action.subtype == types.FETCH_BUTTONS:
            await self.on_fetch_buttons(action)
        elif action.subtype == types.FETCH_CANVAS:
            await self.on_fetch_canvas(action)
        elif action.subtype == types.JOIN_CHANNEL:
            await self.on_join_channel(action)
        elif action.subtype == types.LEAVE_CHANNEL:
            await self.on_leave_channel(action)
        elif action.subtype == types.FETCH_CONTEXT_MENU:
            await self.on_fetch_context_menu(action)
        elif action.subtype == types.FETCH_CHANNEL_INFO:
            await self.on_fetch_channel_info(action)
        else:
            logger.error(f"Unknown action subtype: {action.subtype}")

    async def on_update(self, update):
        """Dispatches an Update instance to one of various callbacks. Agent function.
           It is recommended to overload the invididual callbacks instead of this function."""
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
        elif update.subtype == types.UPDATE_CONTEXT_MENU:
            await self.on_update_context_menu(update)
        else:
            logger.error(f"Unknown update subtype: {update.subtype}")

    ################################## Individual callbacks #######################################

    async def on_spell(self, obj):
        """Called when a spell is received, which can be any object but is often a string. Returns None."""
        logger.debug(f'Spell Received {obj}')

    async def on_start(self):
        """Called when the service is initialized. Returns None"""
        logger.debug("Service started. Override this method to perform initialization tasks.")

    async def on_message_up(self, message_up: MessageBody):
        """
        Handles a payload from a user. Service function. Returns None.
        Example MessageBody object:
          moobius.MessageBody(subtype=text, channel_id=<channel id>, content=MessageContent(...), timestamp=1707254706635,
                              recipients=[<user id 1>, <user id 2>], sender=<user id>, message_id=<message-id>,
                              context={'group_id': <group-id>, 'channel_type': 'ccs'})
        """
        logger.debug(f"MessageUp received: {message_up}")

    async def on_message_down(self, message_down):
        """Callback when a message is recieved (a MessageBody object similar to what on_message_up gets).
           Agent function. Returns None."""
        logger.debug(f"MessageDown received: {message_down}")

    async def on_update_characters(self, update):
        """Handles changes to the character list. One of the multiple update callbacks. Returns None.
           Agent function. Update is an Update instance."""
        logger.debug("on_update_character_list")

    async def on_update_channel_info(self, update):
        """Handles changes to the channel info. One of the multiple update callbacks. Returns None.
           Agent function. Update is an Update instance."""
        logger.debug("on_update_channel_info")

    async def on_update_canvas(self, update):
        """Handles changes to the canvas. One of the multiple update callbacks. Returns None.
           Agent function. Update is an Update instance."""
        logger.debug("on_update_canvas")

    async def on_update_buttons(self, update):
        """Handles changes to the buttons. One of the multiple update callbacks. Returns None.
           Agent function. Update is an Update instance."""
        logger.debug("on_update_buttons")

    async def on_update_style(self, update):
        """Handles changes to the style (look and feel). One of the multiple update callbacks. Returns None.
           Agent function. Update is an Update instance."""
        logger.debug("on_update_style")

    async def on_update_context_menu(self, update):
        """Handles changes to the context menu. One of the multiple update callbacks. Returns None.
           Agent function. Update is an Update instance."""
        logger.debug("update_context_menu")

    async def on_fetch_service_characters(self, action):
        """Handles the received action of fetching a character_list. One of the multiple Action object callbacks. Returns None.
           Example Action object: moobius.Action(subtype="fetch_characters", channel_id=<channel id>, sender=<user id>, context={})."""
        logger.debug("on_action fetch_service_characters")

    async def on_fetch_buttons(self, action): # TODO: This doesn't seem to have the buttons?
        """Handles the received action of fetching buttons. One of the multiple Action object callbacks. Returns None.
           Example Action object: moobius.Action(subtype="fetch_buttons", channel_id=<channel id>, sender=<user id>, context={})"""
        logger.debug("on_action fetch_buttons")

    async def on_fetch_canvas(self, action):
        """Handles the received action (Action object) of fetching canvas. One of the multiple Action object callbacks. Returns None."""
        logger.debug("on_action fetch_canvas")

    async def on_fetch_context_menu(self, action):
        """Handles the received action (Action object) of fetching the right-click context menu. One of the multiple Action object callbacks. Returns None."""
        logger.debug("on_action fetch_context_menu")

    async def on_fetch_channel_info(self, action):
        """Handle the received action of fetching channel info. One of the multiple Action object callbacks. Returns None.
           Example Action object: moobius.Action(subtype="fetch_channel_info", channel_id=<channel id>, sender=<user id>, context={})."""
        logger.debug("on_action fetch_channel_info")

    async def on_join_channel(self, action):
        """Handles the received action of joining a channel. One of the multiple Action object callbacks. Returns None.
           Example Action object: moobius.Action(subtype="join_channel", channel_id=<channel id>, sender=<user id>, context={})."""
        logger.debug("on_action join_channel")

    async def on_leave_channel(self, action):
        """Handles the received action of leaving a channel. One of the multiple Action object callbacks. Returns None.
           Example Action object: moobius.Action(subtype="leave_channel", channel_id=<channel id>, sender=<user id>, context={})."""
        logger.debug("on_action leave_channel")

    async def on_button_click(self, button_click: ButtonClick):
        """Handles a button call from a user. Returns None.
           Example ButtonClick object: moobius.ButtonClick(button_id="the_big_red_button", channel_id=<channel id>, sender=<user id>, arguments=[], context={})"""
        logger.debug(f"Button call received: {button_click}")

    async def on_context_menu_click(self, context_click: MenuClick):
        """Handles a context menu right click from a user. Returns None. Example MenuClick object:
        MenuClick(item_id=1, message_id=<id>, message_subtype=text, message_content={'text': 'Click on this message.'}, channel_id=<channel_id>, context={}, recipients=[])"""
        logger.debug(f"Right-click call received: {context_click}")

    async def on_copy_client(self, copy):
        """Handles a "Copy" of a message. Returns None.
           Example Copy object: moobius.Copy(request_id=<id>, origin_type=message_down, status=True, context={'message': 'Message received'})"""
        if not self.is_agent and not copy.status:
            await self.send_service_login()
        logger.debug("on_copy_client")

    async def on_unknown_payload(self, payload: Payload):
        """Catch-all for handling unknown Payload objects. Returns None."""
        pass

    def __str__(self):
        fname = self.config_path
        http_server_uri = self.config["http_server_uri"]
        ws_server_uri = self.config["ws_server_uri"]
        email = self.config["email"]
        num_channels = len(self.channels)
        agsv = 'Agent' if self.is_agent else 'Service'
        return f'moobius.SDK({agsv}; config=config={fname}, http_server_uri={http_server_uri}, ws_server_uri={ws_server_uri}, ws={ws_server_uri}, email={email}, password=****, num_channels={num_channels})'
    def __repr__(self):
        return self.__str__()
