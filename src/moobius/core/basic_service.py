# basic_service.py

import asyncio
import json
import uuid
import aioprocessing

from dataclasses import asdict
from dacite import from_dict
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from moobius.network.ws_client import WSClient
from moobius.network.ws_payload_builder import WSPayloadBuilder
from moobius.network.http_api_wrapper import HTTPAPIWrapper
from moobius.types import MessageBody, Action, FeatureCall, Copy, Payload
from loguru import logger


class MoobiusBasicService:
    '''
    MoobiusBasicService is a basic service class. It consists of 4 parts:
    
        1. Scheduling: MoobiusBasicService contains a scheduler which is started automatically when the service is started.
            This part schedules 3 jobs: _do_refresh(), _do_authenticate(), _do_send_heartbeat(). We use apscheduler to do this.
        
        2. Starting the service: MoobiusBasicService will automatically connect to the websocket server, handle channel binding and start listening to the websocket and the wand when start() is called.
        
        3. Handling received payloads: MoobiusBasicService will automatically decode the received payload and call the corresponding method to handle it.
            We have handle_received_payload() to decode the payload and call the corresponding method.
            The corresponding method is on_msg_up(), on_action(), on_feature_call(), on_copy(), on_unknown_payload().
            These methods are to be override by the user in their own service class.
            
        4. Sending payloads: MoobiusBasicService provides some methods to send payloads. These methods are to be used by the user in their own service class.
            We have send(), send_service_login(), send_msg_down(), send_update(), send_update_user_list(), send_update_channel_info(), send_update_playground(), send_update_features(), send_update_style(), send_heartbeat().
    '''
    def __init__(self, config_path="", **kwargs):
        '''
        Initialize the service.
        
        Parameters:
            config_path: str
                The path of the config file. Please add a config file to your project following readme.md.
            kwargs: dict
                The extra parameters.
                
        Returns:
            None
            
        Example:
            Note: This is a hidden function, you don't need to call it directly.
            >>> service = MoobiusBasicService(config_path="config.json")
        '''
        self.config_path = config_path

        with open(self.config_path, "r") as f:
            self.config = json.load(f)

        http_server_uri = self.config["http_server_uri"]
        ws_server_uri = self.config["ws_server_uri"]
        email = self.config["email"]
        password = self.config["password"]
        
        self.service_id = self.config["service_id"]
        self.channels = []  # real channel ids. Not necessarily the same as self.config["channels"]

        self.http_api = HTTPAPIWrapper(http_server_uri, email, password)
        self._ws_client = WSClient(ws_server_uri, on_connect=self.send_service_login, handle=self.handle_received_payload)
        self._ws_payload_builder = WSPayloadBuilder()

        self.queue = aioprocessing.AioQueue()
        
        self.refresh_interval = 6 * 60 * 60             # 24h expire, 6h refresh
        self.authenticate_interval = 7 * 24 * 60 * 60   # 30d expire, 7d refresh
        self.heartbeat_interval = 30                    # 30s heartbeat

        self.scheduler = None

    # =================== jobs ===================

    # todo: if token expires for some reason, do authentication again
    async def _do_send_heartbeat(self):
        '''
        Send heartbeat to the server.
        
        Parameters:
            None
        
        Returns:
            None
        
        Example:
            Note: This is a hidden function, you don't need to call it directly.
            >>> self.scheduler = AsyncIOScheduler()
            >>> self.scheduler.add_job(self._do_send_heartbeat, 'interval', seconds=self.heartbeat_interval)
        '''
        await self.send_heartbeat()

    # this method will automatically set http_api headers
    async def _do_refresh(self):
        '''
        Refresh the access token.
        
        Parameters:
            None
        
        Returns:
            None
        
        Example:
            Note: This is a hidden function, you don't need to call it directly.
            >>> self.scheduler = AsyncIOScheduler()
            >>> self.scheduler.add_job(self._do_refresh, 'interval', seconds=self.refresh_interval)
        '''
        access_token = self.http_api.refresh()
        logger.info(f"Refreshed access token: {access_token}")

    # this method will automatically set http_api headers
    async def _do_authenticate(self):
        '''
        Authenticate the service.
        
        Parameters:
            None
        
        Returns:
            None
            
        Example:
            Note: This is a hidden function, you don't need to call it directly.
            >>> self.scheduler = AsyncIOScheduler()
            >>> self.scheduler.add_job(self._do_authenticate, 'interval', seconds=self.authenticate_interval)
        '''
        
        access_token, refresh_token = self.http_api.authenticate()
        logger.info(f"Authenticated. Access token: {access_token}")

    # =================== start ===================
    
    # todo: config["others"]: "ignore" (default) | "unbind" | "include"
    async def start(self):
        '''
        Start the service. There are 6 steps:
        
            1. Authenticate the service.
            2. Connect to the websocket server.
            3. Bind the service to the channels. If there is no service_id in the config file, create a new service and update the config file.
            4. Start the scheduler, run _do_refresh(), _do_authenticate(), _do_send_heartbeat() periodically.
            5. Call on_start() to perform initialization tasks (override this method to do your own initialization tasks).
            6. Start listening to the websocket and the wand.
        
        Parameters:
            None
        
        Returns:
            None
        
        Example:
            Note: This is a hidden function, you don't need to call it directly.
            >>> service = MoobiusBasicService(config_path="config.json")
            >>> await service.start()
        '''
        
        logger.debug("Starting service...")
        
        await self._do_authenticate()
        await self._ws_client.connect()
        logger.debug("Connected to websocket server.")
        
        if not self.service_id:
            logger.debug('No service_id in config file. Will create a new service if necessary.')
        else:
            pass
            
        service_list = self.http_api.get_service_list()
        logger.debug(f"{service_list}")
        logger.info(f"Service ID: {self.service_id}")
        
        # find all channels that could be run on later
        for channel_id in set(self.config["channels"]):
            for service in service_list:
                if service["service_id"] == self.service_id:    # default service_id is "", which is not in service_list
                    self.channels.append(channel_id)    # would be rebinded
                    break
                else:
                    if channel_id in service["channel_ids"]:
                        logger.info(f"Channel {channel_id} already binded to a service_id: {service['service_id']}")
                        break
                    else:
                        continue
            else:
                self.channels.append(channel_id)

        logger.info(f"Channels to bind: {self.channels}")

        if not self.channels:
            logger.error("No proper channel to run on. The process will exit. Please check your config file.")
            
            return
        else:
            if not self.service_id:
                self.service_id = self.http_api.create_service(description="Generated by MoobiusBasicService")

                logger.info(f"NEW SERVICE CREATED!!!")
                logger.info("=================================================")
                logger.info(f" Service ID: {self.service_id}")
                logger.info("=================================================")
                logger.info(f"Please wait for 5 seconds...")

                await asyncio.sleep(5)
            else:
                pass

            for channel_id in self.channels:
                bind_info = self.http_api.bind_service_to_channel(self.service_id, channel_id)  # may already be binded to the service itself
                logger.info(f"Bind service to channel {channel_id}: {bind_info}")

            try:
                with open(self.config_path, "r") as f:
                    f.seek(0)
                    data = json.load(f)
            except:
                logger.debug("No config file found. Creating a new one...")
                
                data = {
                    "http_server_uri": self.config["http_server_uri"],
                    "ws_server_uri": self.config["ws_server_uri"],
                    "email": self.config["email"],
                    "password": self.config["password"],
                    "service_id": "",
                    "channels": [],
                    "others": "ignore"
                }

            data["service_id"] = self.service_id
            data["channels"] = self.channels

            with open(self.config_path, "w") as f:
                json.dump(data, f, indent=4)

            logger.info(f"Config file updated: {self.config_path}")
            await self.send_service_login()

            # Schedulers cannot be serialized so that you have to initialize it here
            self.scheduler = AsyncIOScheduler()

            # The details of access_token and refresh_token are managed by self.http_api
            self.scheduler.add_job(self._do_refresh, 'interval', seconds=self.refresh_interval)
            self.scheduler.add_job(self._do_authenticate, 'interval', seconds=self.authenticate_interval)
            self.scheduler.add_job(self._do_send_heartbeat, 'interval', seconds=self.heartbeat_interval)

            self.scheduler.start()
            logger.debug("Scheduler started.")

            await self.on_start()
            logger.debug("on_start() finished.")

            await asyncio.gather(self._ws_client.receive(), self.listen())
    
    @logger.catch
    async def listen(self):
        '''
        Listen to the wand so that the wand could send spells to the service at any time (not only before the service is started).
        We use asyncio.Queue to do this.
        
        Parameters:
            None
            
        Returns:
            None
        
        Example:
            Note: This is a hidden function, you don't need to call it directly.
            >>> await self.listen()
        '''
        while True:
            obj = await self.queue.coro_get()
            await self.on_spell(obj)


    @logger.catch
    async def handle_received_payload(self, payload):
        """
        Decode the received payload and handle based on its type.
        Call the corresponding method (on_msg_up(), on_action(), on_feature_call(), on_copy(), on_unknown_payload()) to handle the payload.
        
        Parameters:
            payload: str
        
        Returns:
            None
        
        Example:
            Note: This is a hidden function, you don't need to call it directly.
            >>> await self.handle_received_payload(payload)
            >>> # also we can initialize the ws_client like this:
            >>> self._ws_client = WSClient(ws_server_uri, on_connect=self.send_service_login, handle=self.handle_received_payload)
        """
        payload_data = json.loads(payload)
        
        if 'type' in payload_data:
            payload = from_dict(data_class=Payload, data=payload_data)
            
            if payload.type == "msg_up":
                await self.on_msg_up(payload.body)
            
            elif payload.type == "action":
                await self.on_action(payload.body)
            
            elif payload.type == "feature_call":
                await self.on_feature_call(payload.body)

            elif payload.type == "copy_client":     # todo: legacy
                await self.on_copy(payload.body)

            else:   # todo: add types (copy_client etc)
                await self.on_unknown_payload(payload)
        else:
            logger.error(f"Unknown payload without type: {payload_data}")
    


    # =================== on_xxx, to be override ===================

    async def on_spell(self, obj):
        """
        Called when a spell is received.
        
        Parameters:
            obj: any
        
        Returns:
            None
        
        Example:
            Note: This is a hidden function, you don't need to call it directly. Override this method to customize the behavior when a spell is received.
            >>> await self.on_spell(obj)
        """
        logger.debug(f'Spell Received {obj}')
        pass


    async def on_start(self):
        """
        Called when the service is initialized.
        
        Parameters:
            None
        
        Returns:
            None
        
        Example:
            Note: This is a hidden function, you don't need to call it directly. Override this method to customize initialization tasks.
            >>> await self.on_start()
        """
        logger.debug("Service started. Override this method to perform initialization tasks.")
        pass


    async def on_msg_up(self, msg_up: MessageBody):
        """
        Handle a payload from a user.
        
        Parameters:
            msg_up: MessageUp
        
        Returns:
            None
        
        Example:
            Note: Override this method to customize the behavior when a message is received.
            >>> await self.on_msg_up(msg_up)
        """
        logger.debug(f"MessageUp received: {msg_up}")
        pass

    async def on_fetch_user_list(self, action):
        """
        Handle the received action of fetching user_list.
        
        Parameters:
            action: Action
            
        Returns:
            None
        
        Example:
            Note: Override this method to customize the behavior when a fetch_user_list action is received.
            >>> await self.on_fetch_user_list(action)
        """
        logger.debug("on_action fetch_userlist")
        pass
    
    async def on_fetch_features(self, action):
        """
        Handle the received action of fetching features.
        
        Parameters:
            action: Action
        
        Returns:
            None
        
        Example:
            Note: Override this method to customize the behavior when a fetch_features action is received.
            >>> await self.on_fetch_features(action)
        """
        logger.debug("on_action fetch_features")
        pass
    
    async def on_fetch_playground(self, action):
        """
        Handle the received action of fetching playground.
        
        Parameters:
            action: Action
        
        Returns:
            None
            
        Example:
            Note: Override this method to customize the behavior when a fetch_playground action is received.
            >>> await self.on_fetch_playground(action)
        """
        logger.debug("on_action fetch_playground")
        pass
    
    async def on_join_channel(self, action):
        """
        Handle the received action of joining channel.
        
        Parameters:
            action: Action
        
        Returns:
            None
            
        Example:
            Note: Override this method to customize the behavior when a join_channel action is received.
            >>> await self.on_join_channel(action)
        """
        logger.debug("on_action join_channel")
        pass

    async def on_leave_channel(self, action):
        """
        Handle the received action of leaving channel.
        
        Parameters:
            action: Action
        
        Returns:
            None
            
        Example:
            Note: Override this method to customize the behavior when a leave_channel action is received.
            >>> await self.on_leave_channel(action)
        """
        logger.debug("on_action leave_channel")
        pass
        
    async def on_fetch_channel_info(self, action):
        """
        Handle the received action of fetching channel info.
        
        Parameters:
            action: Action
        
        Returns:
            None
            
        Example:
            Note: Override this method to customize the behavior when a fetch_channel_info action is received.
            >>> await self.on_fetch_channel_info(action)
        """
        logger.debug("on_action fetch_channel_info")
        pass
    
    async def on_action(self, action: Action):
        """
        Handle an action from a user.
        Call the corresponding method (on_fetch_user_list(), on_fetch_features(), on_fetch_playground(), on_join_channel(), on_leave_channel(), on_fetch_channel_info()) to handle different subtypes of action.
        
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

    async def on_feature_call(self, feature_call: FeatureCall):
        """
        Handle a feature call from a user.
        
        Parameters:
            feature_call: FeatureCall
        
        Returns:
            None
        
        Example:
            Note: Override this method to customize the behavior when a feature call is received.
            >>> await self.on_feature_call(feature_call)
        """
        logger.debug(f"Feature call received: {feature_call}")
        pass


    async def on_copy(self, copy: Copy):
        """
        Handle a copy from Moobius.
        
        Parameters:
            copy: Copy
        
        Returns:
            None
        
        Example:
            Note: Override this method to customize the behavior when a copy is received.
            >>> await self.on_copy(copy)
        """
        if not copy.status:
            await self.send_service_login()
        else:
            pass


    async def on_unknown_payload(self, payload: Payload):
        """
        Handle an unknown payload.
        
        Parameters:
            payload: Payload
            
        Returns:
            None
        
        Example:
            Note: Override this method to customize the behavior when an unknown payload is received.
            >>> await self.on_unknown_payload(payload)
        """
        logger.debug(f"Unknown payload received: {payload}")
        pass

    # =================== send_xxx, to be used ===================
    
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
                'client_id': self.service_id,
                'body': payload_body
            }
        else:
            payload_obj = Payload(
                type=payload_type,
                request_id=str(uuid.uuid4()),
                client_id=self.service_id,
                body=payload_body
            )

            payload_dict = asdict(payload_obj)

        payload_str = self._ws_payload_builder.dumps(payload_dict)
        await self._ws_client.send(payload_str)

    # todo: decouple access_token here!
    # every 2h aws force disconnect, so we send service_login on connect
    async def send_service_login(self):
        '''
        Send service_login to the server.
        
        Parameters:
            None
        
        Returns:
            None

        Example:
            Note: This is a hidden function, you don't need to call it directly.
            >>> await self.send_service_login()
            >>> # or you can use this method to send service_login on connect:
            >>> self._ws_client = WSClient(ws_server_uri, on_connect=self.send_service_login, handle=self.handle_received_payload)
        '''
        payload = self._ws_payload_builder.service_login(self.service_id, self.http_api.access_token)
        await self._ws_client.send(payload)

    async def send_msg_down(self, channel_id, recipients, subtype, message_content, sender):
        '''
        Send msg_down to the recipients.
        
        Parameters:
            channel_id: str
                The channel id.
            recipients: list
                The list of recipients.
            subtype: str
                The subtype of the message.
            message_content: str
                The content of the message.
            sender: str
                The sender of the message.
        
        Returns:
            None
        
        Example:
            >>> await self.send_msg_down(channel_id, recipients, subtype, message_content, sender)
        '''
        payload = self._ws_payload_builder.msg_down(self.service_id, channel_id, recipients, subtype, message_content, sender)
        await self._ws_client.send(payload)

    async def send_update(self, target_client_id, data):
        '''
        Send any update to the target client.
        
        Parameters:
            target_client_id: str
                The target client id.
            data: dict
                The data to be sent.
        
        Returns:
            None

        Example:
            >>> await self.send_update(target_client_id, data)
        '''
        payload = self._ws_payload_builder.update(self.service_id, target_client_id, data)
        await self._ws_client.send(payload)

    async def send_update_user_list(self, channel_id, user_list, recipients):
        '''
        Send user list update to the recipients.
        
        Parameters:
            channel_id: str
                The channel id.
            user_list: list
                The user list of to be updated.
            recipients: list
                The list of recipients.
        
        Returns:
            None
        
        Example:
            >>> tubbs = _make_character(channel_id, "tubbs", "tubbs")
            >>> user_list = list(self.bands[channel_id].real_characters.values())
            >>> user_list.append(tubbs)
            >>> await self.send_update_user_list(channel_id, user_list, [feature_call.sender])
        '''
        payload = self._ws_payload_builder.update_userlist(self.service_id, channel_id, user_list, recipients)
        await self._ws_client.send(payload)

    async def send_update_channel_info(self, channel_id, channel_data):
        '''
        Send channel info update to the recipients.
        
        Parameters:
            channel_id: str
                The channel id.
            channel_data: dict
                The channel data to be updated.
            
        Returns:
            None
        
        Example:
            >>> await await self.send_update_channel_info(channel_id, self.db_helper.get_channel_info(channel_id))
        '''
        payload = self._ws_payload_builder.update_channel_info(self.service_id, channel_id, channel_data)
        await self._ws_client.send(payload)

    async def send_update_playground(self, channel_id, content, recipients):
        '''
        Send playground update to the recipients.
        
        Parameters:
            channel_id: str
                The channel id.
            content: str
                The content of the playground.
            recipients: list
                The list of recipients.
            
        Returns:
            None
        
        Example:
            >>> content = self.db_helper.get_playground_info(channel_id)
            >>> await self.send_update_playground(channel_id, content, recipients)
        '''
        payload = self._ws_payload_builder.update_playground(self.service_id, channel_id, content, recipients)
        await self._ws_client.send(payload)

    async def send_update_features(self, channel_id, feature_data, recipients):
        '''
        Send feature update to the recipients.
        
        Parameters:
            channel_id: str
                The channel id.
            feature_data: list of dict
                The feature data to be updated.
            recipients: list
                The list of recipients.
            
        Returns:
            None
        
        Example:
            >>> self.continue_feature = {
            >>>         "feature_id": "play",
            >>>         "feature_name": "Continue Playing",
            >>>         "button_text": "Continue Playing",
            >>>         "new_window": False,
            >>>         "arguments": [
            >>>         ]
            >>>     }
            >>> features = [
            >>>     self.continue_feature
            >>> ]
            >>> await self.send_update_features(action.channel_id, features, [action.sender])
        '''
        payload = self._ws_payload_builder.update_features(self.service_id, channel_id, feature_data, recipients)
        await self._ws_client.send(payload)
    
    async def send_update_style(self, channel_id, style_content, recipients):
        '''
        Send style update to the recipients.
        
        Parameters:
            channel_id: str
                The channel id.
            style_content: str
                The content of the style.
            recipients: list
                The list of recipients.
                
        Returns:
            None
        
        Example:
            >>> style_content = [
            >>>     {
            >>>         "widget": "playground",
            >>>         "display": "visible",
            >>>         "expand": "true"
            >>>     }
            >>> ]
            >>> await self.send_update_style(channel_id, style_content, recipients)
        '''
        payload = self._ws_payload_builder.update_style(self.service_id, channel_id, style_content, recipients)
        await self._ws_client.send(payload)

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
        payload = self._ws_payload_builder.ping()
        await self._ws_client.send(payload)