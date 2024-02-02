# SDK interface, agent or service. Automatically wraps the two platform APIs (HTTP and Socket)

import json
import time

from dataclasses import asdict
from dacite import from_dict

from moobius.types import MessageBody

import asyncio
import json
import uuid
import aioprocessing

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from moobius.network.ws_client import WSClient
from moobius.network.http_api_wrapper import HTTPAPIWrapper
from moobius.types import MessageBody, Action, FeatureCall, FeatureCallArgument, Copy, Payload
from loguru import logger

strict_kwargs = False # If True all functions (except __init__) with more than one non-self arg will require kwargs. If False a default ordering will be used.


class SDK:

    ############################ Startup functions ########################################

    def __init__(self, config_path, db_config_path="", is_agent=False, **kwargs):
        '''
        Initialize a service or agent object.

        Parameters:
            config_path: str
                The path of the agent or service config file. Can also be a dict.
            db_config_path="": str
                The path of the database config file. Can also be a dict. No file will be loaded nor attribute set if an empty string.
            is_agent=False:
                True for an agent, False for a service. Agents and services have slight differences.

        Returns:
            None

        Example:
            >>> service = SDK(service_config_path="config/service.json", db_config_path="config/database.json", is_agent=False)
        '''
        self.config_path = config_path
        self.is_agent = is_agent

        if type(config_path) is dict:
            logger.info('Be careful to keep the secrets in your service config safe!')
            self.config = config_path
        elif type(config_path) is str:
            with open(config_path, "r") as f:
                self.config = json.load(f)
        else:
            raise Exception('config_path not understood')

        if type(db_config_path) is dict:
            self.db_config = db_config_path
        elif type(db_config_path) is str and db_config_path != "":
            with open(db_config_path, "r") as f:
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
            self.service_id = self.client_id # TODO deprecated feature so older apps can run.

        self.channels = []  # real channel ids. Not necessarily the same as self.config["channels"]

        self.http_api = HTTPAPIWrapper(http_server_uri, email, password)
        self.ws_client = WSClient(ws_server_uri, on_connect=self.send_agent_login if self.is_agent else self.send_service_login, handle=self.handle_received_payload)

        self.queue = aioprocessing.AioQueue()

        self.refresh_interval = 6 * 60 * 60             # 24h expire, 6h refresh
        self.authenticate_interval = 7 * 24 * 60 * 60   # 30d expire, 7d refresh
        self.heartbeat_interval = 30                    # 30s heartbeat

        self.scheduler = None

        self.bands = {}

    async def start(self):
        '''
        Start the service/agent. start() fns are called with wand.run. There are 6 steps:

            1. Authenticate the service.
            2. Connect to the websocket server.
            3. Bind the service to the channels. If there is no service_id in the config file, create a new service and update the config file.
            4. Start the scheduler, run refresh(), authenticate(), send_heartbeat() periodically.
            5. Call on_start() to perform initialization tasks (override this method to do your own initialization tasks).
            6. Start listening to the websocket and the wand.

        Parameters:
            None

        Returns:
            None

        Example:
            >>> service = SDK(config_path="config.json")
            >>> await service.start()
        '''

        logger.debug("Starting agent..." if self.is_agent else "Starting service...")

        await self.authenticate()
        await self.ws_client.connect()
        logger.debug("Connected to websocket server.")

        if self.is_agent:
            async def _get_agent_info():
                if not self.is_agent:
                    raise Exception('Not an agent.')
                self.agent_info = self.http_api.fetch_user_info()
                self.client_id = self.agent_info["sub"]
            await _get_agent_info()
            await self.send_agent_login()
        else:
            if not self.client_id:
                logger.debug('No service_id in config file. Will create a new service.')
                self.client_id = self.http_api.create_service(description="Generated by MoobiusService")

                logger.info(f"NEW SERVICE CREATED!!!")
                logger.info("=================================================")
                logger.info(f" Service ID: {self.client_id}")
                logger.info("=================================================")
                logger.info(f"Please wait for 5 seconds...")
                self.config["service_id"] = self.client_id
                await asyncio.sleep(5) # TODO: Sleeps "long enough" should be replaced with polling.

            if len(self.config["channels"]) == 0:
                logger.error('No channels specified in self.config')
                return

            channelid2serviceid = await self.fetch_bound_channels() # Channels can only be bound to a SINGLE service.

            others = self.config["others"].lower().strip()
            for channel_id in set(self.config["channels"]):
                bound_to = channelid2serviceid.get(channel_id)
                if bound_to == self.client_id:
                    logger.info(f"Channel {channel_id} already bound to {self.client_id}, no need to bind it.")
                    self.channels.append(channel_id)
                    continue
                elif bound_to: # Conflict resolution.
                    if others=='ignore': # Do not intefere with channels bound to other users.
                        logger.info(f"Channel {channel_id} bound to service {bound_to} and will not be re-bound.")
                        continue
                    elif others=='unbind': # Be spiteful: Unbind channels bound to other users but don't use them.
                        logger.info(f"Unbinding channel {channel_id} from service {bound_to} but this service will not use this channel.")
                        self.http_api.unbind_service_from_channel(bound_to, channel_id)
                        continue
                    elif others=='include': # Steal channels from other services. Hopefully they won't mind.
                        logger.info(f"Unbinding channel {channel_id} from service {bound_to} so it can be used by this service instead.")
                        self.http_api.unbind_service_from_channel(bound_to, channel_id)
                    else:
                        raise Exception(f'Unknown others (other bands) option for handling channels already bound to other services: {others}')
                bind_info = self.http_api.bind_service_to_channel(self.client_id, channel_id) # may already be binded to the service itself
                logger.info(f"Bound service to channel {channel_id}: {bind_info}")
                self.channels.append(channel_id)

            if not self.channels:
                logger.error("All channels are used up by other services and the 'others' option is not set to 'include' to steal them back.")
                return

            if type(self.config_path) is str:
                with open(self.config_path, "w") as f:
                    json.dump(self.config, f, indent=4)
                logger.info(f"Config file updated: {self.config_path}")

            await self.send_service_login() # It is OK (somehow) to log in after all of this not before.

        # Schedulers cannot be serialized so that you have to initialize it here
        self.scheduler = AsyncIOScheduler()

        # The details of access_token and refresh_token are managed by self.http_api
        self.scheduler.add_job(self.refresh, 'interval', seconds=self.refresh_interval)
        self.scheduler.add_job(self.authenticate, 'interval', seconds=self.authenticate_interval)
        self.scheduler.add_job(self.send_heartbeat, 'interval', seconds=self.heartbeat_interval)

        self.scheduler.start()
        logger.debug("Scheduler started.")

        await self.on_start()
        logger.debug("on_start() finished.")

        await asyncio.gather(self.ws_client.receive(), self.listen_loop())

    ################################## Query functions #######################################

    async def fetch_bound_channels(self):
        '''Which service is each channel bound to?'''
        service_list = self.http_api.fetch_service_list()
        #logger.debug(f"Service list: {service_list}")
        #logger.info(f"Service ID: {self.client_id}")
        channelid2serviceid = {} # Channels can only be bound to a SINGLE service.
        for service in service_list:
            for channel_id in service["channel_ids"]:
                channelid2serviceid[channel_id] = service['service_id']
        return channelid2serviceid

    async def fetch_real_characters(self, channel_id): return self.http_api.fetch_real_characters(channel_id, self.client_id)

    ################################## Actuators #######################################

    async def upload_avatar_and_create_character(self, service_id, username, nickname, image_path, description):
        '''
        Upload an avatar image and create a character.
        Service function not Agent function.

        Parameters:
            service_id: str
                The id of the service.
            username: str
                The username of the character.
            nickname: str
                The nickname of the character.
            image_path: str
                The path of the avatar image. This should be the local path of the image.
            description: str
                The description of the character.

        Returns:
            The Character object of the created character.

        Example:
            >>> character = await self.upload_avatar_and_create_character(service_id, username, nickname, image_path, description)
        '''
        avatar = self.http_api.upload_file(image_path)
        return self.http_api.create_service_user(service_id, username, nickname, avatar, description)

    async def create_message(self, channel_id, content, recipients, subtype='text', sender=None):
        '''
        Create a MessageDown (for service) or MessageUp (for agent) request and send it to the channel.

        Parameters:
            channel_id: str
                The id of the channel.
            content: str
                The content of the message.
            recipients: list
                The recipients of the message.
            subtype: str='text'
                The subtype of the message.
            sender: str=None
                The sender of the message. None for Agents.

        Returns:
            None

        Example:
            >>> await self.create_message(channel_id, content, recipients, subtype='text', sender=None)
        '''
        kwargs = {'channel_id':channel_id, 'recipients':recipients, 'subtype':subtype, 'message_content':content}
        if self.is_agent:
            await self.send_msg_up(**kwargs)
        else:
            kwargs['sender'] = sender or 'no_sender'
            await self.send_msg_down(**kwargs)

    async def send(self, payload_type, payload_body):
        '''
        Send any kind of payload, including msg_down, update, update_userlist, update_channel_info, update_playground, update_features, update_style, and heartbeat.

        Parameters:
            payload_type: str
                The type of the payload.
            payload_body: dict or str
                The body of the payload.

        Returns:
            None

        Example:
            >>> await self.send(payload_type='msg_down', payload_body=msg_up)
        '''
        if isinstance(payload_body, dict):
            payload_dict = {
                'type': payload_type,
                'request_id': str(uuid.uuid4()),
                'client_id': self.client_id,
                'body': payload_body
            }
        else: # Need to wrap non-dataclasses into a dataclass, in this case Payload, in order to use asdict() on them.
            payload_obj = Payload(
                type=payload_type,
                request_id=str(uuid.uuid4()),
                client_id=self.client_id,
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
                            asdict(Payload(type=payload_type, request_id=str(uuid.uuid4()), client_id=self.client_id, body=v))
                            _pr('No problem pickling:', k, v)
                        except Exception as e:
                            _pr('UNDICTABLE part of __dict__ error:', k, 'Value is:', v, 'type is:', type(v), 'error is:', e)
                raise error_e
        await self.ws_client.send(payload_dict)

    async def send_feature_call(self, channel_id, feature_id, feature_args):
        '''
        Use to send a request to ask for a feature call.

        Parameters:
            channel_id: Which channel.
            feature_id: Which feature.
            feature_args: What about said feature should be fetched?
        Returns:
            None
        '''
        feature_call_instance = FeatureCall(
            feature_id=feature_id,
            channel_id=channel_id,
            sender=self.client_id,
            arguments=[FeatureCallArgument(name=arg[0], value=arg[1]) for arg in feature_args],
            context={}
        )
        await self.send("feature_call", feature_call_instance)

    async def send_heartbeat(self):
        '''
        Send heartbeat to the server.

        Parameters:
            None

        Returns:
            None

        Example:
            >>> await self.send_heartbeat()
        '''
        await self.ws_client.ping()
        if not self.is_agent: # 95% sure this extra line is just there because no one wanted to remove it.
            await self.ws_client.ping()

    async def create_and_bind_channel(self, channel_name, channel_desc):
        '''
        Create a channel (band) and binds self.client_id (the service_id) to it.
        (I think) a Service function not an Agent function.

        Returns: The channel id.
        '''
        channel_id = self.http_api.create_channel(channel_name, channel_desc)
        self.http_api.bind_service_to_channel(self.client_id, channel_id)  # may already be binded to the service itself
        return channel_id

    ################################## Single-line actuators #######################################

    async def refresh(self): return self.http_api.refresh()
    async def authenticate(self): return self.http_api.authenticate()
    async def create_channel(self, channel_name, channel_desc): return self.http_api.create_channel(channel_name, channel_desc)
    async def send_agent_login(self): return await self.ws_client.agent_login(self.http_api.access_token)
    async def send_service_login(self): return await self.ws_client.service_login(self.client_id, self.http_api.access_token)
    async def send_msg_up(self, channel_id, recipients, subtype, message_content): return await self.ws_client.msg_up(self.client_id, channel_id, recipients, subtype, message_content)
    async def send_msg_down(self, channel_id, recipients, subtype, message_content, sender): return await self.ws_client.msg_down(self.client_id, channel_id, recipients, subtype, message_content, sender)
    async def send_update(self, target_client_id, data): return await self.ws_client.update(self.client_id, target_client_id, data)
    async def send_update_user_list(self, channel_id, user_list, recipients): return await self.ws_client.update_userlist(self.client_id, channel_id, user_list, recipients)
    async def send_update_channel_info(self, channel_id, channel_data): return await self.ws_client.update_channel_info(self.client_id, channel_id, channel_data)
    async def send_update_playground(self, channel_id, content, recipients): return await self.ws_client.update_playground(self.client_id, channel_id, content, recipients)
    async def send_update_features(self, channel_id, feature_data, recipients): return await self.ws_client.update_features(self.client_id, channel_id, feature_data, recipients)
    async def send_update_style(self, channel_id, style_content, recipients): return await self.ws_client.update_style(self.client_id, channel_id, style_content, recipients)
    async def send_fetch_userlist(self, channel_id): return await self.ws_client.fetch_userlist(self.client_id, channel_id)
    async def send_fetch_features(self, channel_id): return await self.ws_client.fetch_features(self.client_id, channel_id)
    async def send_fetch_style(self, channel_id): return await self.ws_client.fetch_style(self.client_id, channel_id)
    async def send_fetch_playground(self, channel_id): return await self.ws_client.fetch_playground(self.client_id, channel_id)
    async def send_fetch_channel_info(self, channel_id): return await self.ws_client.fetch_channel_info(self.client_id, channel_id)
    async def send_join_channel(self, channel_id): return await self.ws_client.join_channel(self.client_id, channel_id)
    async def send_leave_channel(self, channel_id): return await self.ws_client.leave_channel(self.client_id, channel_id)

    ################################## Callback switchyards #######################################

    @logger.catch
    async def listen_loop(self):
        '''
        Listen to the wand (in an infinite loop so) that the wand could send spells to the service at any time (not only before the service is started).
        We use asyncio.Queue to do this.

        Parameters:
            None

        Returns:
            None

        Example:
            Note: You don't need to call it directly.
            >>> await self.listen_loop()
        '''
        while True:
            obj = await self.queue.coro_get()
            await self.on_spell(obj)

    @logger.catch
    async def handle_received_payload(self, payload):
        """
        Decode the received payload and handle based on its type.
        Call the corresponding method (on_msg_up(), on_action(), on_feature_call(), on_copy_client(), on_unknown_payload()) to handle the payload.

        Parameters:
            payload: str

        Returns:
            None

        Example:
            >>> await self.handle_received_payload(payload)
            >>> # also we can initialize the ws_client like this:
            >>> self.ws_client = WSClient(ws_server_uri, on_connect=self.send_service_login, handle=self.handle_received_payload)
        """
        payload_data = json.loads(payload)
        if payload_data['type'] == 'msg_down' and 'recipients' not in payload_data['body']:
            payload_data['body']['recipients'] = [] # The conversion to a MessageBody needs all keys to be present! But msg_down doesn't have "recipients".
        if 'type' in payload_data:
            payload = from_dict(data_class=Payload, data=payload_data)
            if payload.type == "msg_down":
                await self.on_msg_down(payload.body)
            elif payload.type == "update":
                await self.on_update(payload.body)
            elif payload.type == "msg_up":
                await self.on_msg_up(payload.body)
            elif payload.type == "action":
                await self.on_action(payload.body)
            elif payload.type == "feature_call":
                await self.on_feature_call(payload.body)
            elif payload.type == "copy_client":     # TODO: legacy, at least for service.
                await self.on_copy_client(payload.body)
            else:   # TODO?: add types?
                await self.on_unknown_payload(payload)
        else:
            logger.error(f"Unknown payload without type: {payload_data}")

    async def on_action(self, action: Action):
        """
        Handle an action from a user.
        Call the corresponding method (on_fetch_user_list(), on_fetch_features(), on_fetch_playground(), on_join_channel(), on_leave_channel(), on_fetch_channel_info()) to handle different subtypes of action.
        Service function not Agent function.

        Parameters:
            action: Action

        Returns:
            None

        Example:
            Note: Override this method to customize the behavior when an action is received, or override the corresponding method to customize the behavior when a specific subtype of action is received.
            >>> await self.on_action(action)
        """
        if action.subtype == "fetch_userlist":
            await self.on_fetch_user_list(action)
        elif action.subtype == "fetch_features":
            await self.on_fetch_features(action)
        elif action.subtype == "fetch_playground":
            await self.on_fetch_playground(action)
        elif action.subtype == "join_channel":
            await self.on_join_channel(action)
        elif action.subtype == "leave_channel":
            await self.on_leave_channel(action)
        elif action.subtype == "fetch_channel_info":
            await self.on_fetch_channel_info(action)
        else:
            logger.error(f"Unknown action subtype: {action.action_subtype}")

    async def on_update(self, update):
        '''
        Dispatches an update to one of various callbacks. Agent function not Service function.
        It is recommended to overload the invididual callbacks instead of this function.

        Parameters:
            update: dict
                The structure varies depending on the 'subtype'

        Returns:
            None
        '''
        if update['subtype'] == "update_userlist":
            await self.on_update_userlist(update)
        elif update['subtype'] == "update_channel_info":
            await self.on_update_channel_info(update)
        elif update['subtype'] == "update_playground":
            await self.on_update_playground(update)
        elif update['subtype'] == "update_features":
            await self.on_update_features(update)
        elif update['subtype'] == "update_style":
            await self.on_update_style(update)
        else:
            logger.error(f"Unknown update subtype: {update['subtype']}")

    ################################## Individual callbacks #######################################

    async def on_spell(self, obj):
        """
        Called when a spell is received.

        Parameters:
            obj: any

        Returns:
            None

        Example:
            >>> await self.on_spell(obj)
        """
        logger.debug(f'Spell Received {obj}')

    async def on_start(self):
        """
        Called when the service is initialized.

        Parameters:
            None

        Returns:
            None

        Example:
            >>> await self.on_start()
        """
        logger.debug("Service started. Override this method to perform initialization tasks.")

    async def on_msg_up(self, msg_up: MessageBody):
        """
        Handle a payload from a user. Service function not Agent function.

        Parameters:
            msg_up: MessageUp

        Returns:
            None

        Example:
            Note: Override this method to customize the behavior when a message is received.
            >>> await self.on_msg_up(msg_up)
        """
        logger.debug(f"MessageUp received: {msg_up}")

    async def on_msg_down(self, msg_down):
        '''Callback when a message is recieved. Agent function not Service function.
           msg_down, the only paramter, is a dict with the same structure as MessageBody'''
        logger.debug(f"MessageDown received: {msg_down}")

    async def on_update_userlist(self, update):
        '''
        One of the multible update callbacks, overload to handle changes to the users.
        Agent function not Service function.

        Parameters:
            update: dict
              Example:
                {"subtype": "update_userlist",
                 "channel_id": "abc...",
                 "recipients": [recipient0_userid, recipient1_userid, recipient2_userid...],
                  "userlist": [user_id0, user_id1, ...],
                    "context": {}}

        Returns:
            None
        '''
        logger.debug("on_update_user_list")

    async def on_update_channel_info(self, update):
        '''
        One of the multible update callbacks, overload to handle changes to the channel.
        Agent function not Service function.

        Parameters:
            update: dict
                Example:    {"subtype": "channel_info",
                             "channel_id": "abc...",
                             "request_id": "abc...", "client_id": "abc...",
                             "body": <dict of channel data>}
        Returns:
            None
        '''
        logger.debug("on_update_channel_info")

    async def on_update_playground(self, update):
        '''
        One of the multible update callbacks, overload to handle changes to the playground.
        Agent function not Service function.

        Parameters:
            update: dict
                Example: {"subtype": "update_playground", "channel_id": "8c2...", "group_id": "temp", "context": {},
                          "content": {"path": "https://...png", "text": "This appears on the Stage"}}
                update['content'] gives the content.
        Returns:
            None
        '''
        logger.debug("on_update_playground")

    async def on_update_features(self, update):
        '''
        One of the multible update callbacks, overload to handle changes to the features.
        Agent function not Service function.

        Parameters:
            update: dict
                Example: {"subtype": "update_features", "channel_id": "8c23...",
                          "features": [{"feature_id": "key1", "feature_name": "name1",
                                        "button_text": "Meet Tubbs or Hermeowne", "new_window": true,
                                        "arguments": [{"name": "arg1", "type": "enum", "optional": false,
                                                       "values": ["Meet Tubbs", "Meet Hermeowne"],
                                                       "placeholder": "placeholder"}]},
                                                       {"feature_id": "key2", "feature_name": "name2", "button_text": "Meet Ms Fortune", "new_window": false, "arguments": null}],
                                        "group_id": "temp", "context": {}}
        Returns:
            None
        '''
        logger.debug("on_update_features")

    async def on_update_style(self, update):
        '''
        One of the multible update callbacks, overload to handle changes to the style.
        Agent function not Service function.

        Parameters:
            update: dict
              Example:
                {"subtype": "update_style",
                "channel_id": "abc...",
                "recipients": [user_id0, user_id1, user_id2],
                "content": [{"widget": "playground","display": "visible", "expand": "true"}],
                "group_id": "temp",
                "context": {}}
        Returns:
            None
        '''
        logger.debug("on_update_style")

    async def on_fetch_user_list(self, action):
        """
        Handle the received action of fetching user_list.
        Service function not Agent function.

        Parameters:
            action: Action

        Returns:
            None

        Example:
            Note: Override this method to customize the behavior when a fetch_user_list action is received.
            >>> await self.on_fetch_user_list(action)
        """
        logger.debug("on_action fetch_userlist")

    async def on_fetch_features(self, action):
        """
        Handle the received action of fetching features.
        Service function not Agent function.

        Parameters:
            action: Action

        Returns:
            None

        Example:
            Note: Override this method to customize the behavior when a fetch_features action is received.
            >>> await self.on_fetch_features(action)
        """
        logger.debug("on_action fetch_features")

    async def on_fetch_playground(self, action):
        """
        Handle the received action of fetching playground.
        Service function not Agent function.

        Parameters:
            action: Action

        Returns:
            None

        Example:
            Note: Override this method to customize the behavior when a fetch_playground action is received.
            >>> await self.on_fetch_playground(action)
        """
        logger.debug("on_action fetch_playground")

    async def on_fetch_channel_info(self, action):
        """
        Handle the received action of fetching channel info.
        Service function not Agent function.

        Parameters:
            action: Action

        Returns:
            None

        Example:
            Note: Override this method to customize the behavior when a fetch_channel_info action is received.
            >>> await self.on_fetch_channel_info(action)
        """
        logger.debug("on_action fetch_channel_info")

    async def on_join_channel(self, action):
        """
        Handle the received action of joining channel.
        Service function not Agent function.

        Parameters:
            action: Action

        Returns:
            None

        Example:
            Note: Override this method to customize the behavior when a join_channel action is received.
            >>> await self.on_join_channel(action)
        """
        logger.debug("on_action join_channel")

    async def on_leave_channel(self, action):
        """
        Handle the received action of leaving channel.
        Service function not Agent function.

        Parameters:
            action: Action

        Returns:
            None

        Example:
            Note: Override this method to customize the behavior when a leave_channel action is received.
            >>> await self.on_leave_channel(action)
        """
        logger.debug("on_action leave_channel")

    async def on_feature_call(self, feature_call: FeatureCall):
        """
        Handle a feature call from a user.
        Service function not Agent function.

        Parameters:
            feature_call: FeatureCall

        Returns:
            None

        Example:
            Note: Override this method to customize the behavior when a feature call is received.
            >>> await self.on_feature_call(feature_call)
        """
        logger.debug(f"Feature call received: {feature_call}")

    async def on_copy_client(self, copy):
        '''
        Parameters:
            copy: Dict organized in same way as Copy object. Example:
              {'request_id': '1c5...', 'origin_type': 'action', 'status': True, 'context': {'msg': 'Action received'}}
        Returns:
            None
        '''
        if not self.is_agent and not copy.status:
            await self.send_service_login()

        logger.debug("on_copy_client")

    async def on_unknown_payload(self, payload: Payload):
        '''
        One of the multible update callbacks, overload to handle changes to the style.

        Parameters:
            update: dict
                The structure of the dict varies depending on the payload.
        Returns:
            None
        '''
        logger.debug(f"Unknown payload received: {payload}")

    def __str__(self):
        fname = self.config_path
        http_server_uri = self.config["http_server_uri"]
        ws_server_uri = self.config["ws_server_uri"]
        email = self.config["email"]
        num_bands = len(self.bands)
        agsv = 'Agent' if self.is_agent else 'Service'
        return f'moobius.SDK({agsv}; config=config={fname}, http_server_uri={http_server_uri}, ws_server_uri={ws_server_uri}, ws={ws_server_uri}, email={email}, password=****, num_bands={num_bands})'
    def __repr__(self):
        return self.__str__()
