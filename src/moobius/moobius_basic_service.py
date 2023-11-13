# moobius_basic_service.py

import asyncio
import json
import time
import uuid
import traceback
import aioprocessing
import time

from dataclasses import asdict

from dacite import from_dict
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from moobius.basic.ws_client import WSClient
from moobius.basic.ws_payload_builder import WSPayloadBuilder
from moobius.basic.http_api_wrapper import HTTPAPIWrapper
from moobius.basic.types import MessageUp, Action, FeatureCall, Copy, Payload, Character
from moobius.moobius_wand import MoobiusWand
from moobius.basic._logging_config import logger

event = aioprocessing.AioEvent()
lock = aioprocessing.AioLock()

class MoobiusBasicService:
    def __init__(self, http_server_uri="", ws_server_uri="", service_id="", email="", password="", **kwargs):
        self.http_api = HTTPAPIWrapper(http_server_uri, email, password)
        self.parent_pipe, self.child_pipe = aioprocessing.AioPipe()
        self.second_parent_pipe, self.second_child_pipe = aioprocessing.AioPipe()
        self._ws_client = WSClient(ws_server_uri, on_connect=self.send_service_login, handle=self.handle_received_payload, second_horcrux=self.second_child_pipe)
        self._ws_payload_builder = WSPayloadBuilder()
        
        self.refresh_interval = 6 * 60 * 60             # 24h expire, 6h refresh
        self.authenticate_interval = 7 * 24 * 60 * 60   # 30d expire, 7d refresh
        self.heartbeat_interval = 30                    # 30s heartbeat
        self.service_id = service_id

        self.scheduler = AsyncIOScheduler()

        # The details of access_token and refresh_token are managed by self.http_api
        self.scheduler.add_job(self._do_refresh, 'interval', seconds=self.refresh_interval)
        self.scheduler.add_job(self._do_authenticate, 'interval', seconds=self.authenticate_interval)
        self.scheduler.add_job(self._do_send_heartbeat, 'interval', seconds=self.heartbeat_interval)

    # =================== jobs ===================

    # todo: if token expires for some reason, do authentication again
    async def _do_send_heartbeat(self):
        payload = self._ws_payload_builder.ping()
        await self._ws_client.send(payload)

    # this method will automatically set http_api headers
    async def _do_refresh(self):
        access_token = self.http_api.refresh()
        logger.info(f"Refreshed access token: {access_token}")

    # this method will automatically set http_api headers
    async def _do_authenticate(self):
        access_token, refresh_token = self.http_api.authenticate()
        logger.info(f"Authenticated. Access token: {access_token}")

    # =================== start ===================
    
    def start(self, bind_to_channels=None):
        print("Starting service...")
        # loop = asyncio.get_event_loop()
        # loop.run_until_complete(self._do_authenticate())
        # event = aioprocessing.AioEvent()
        # lock = aioprocessing.AioLock()
        # loop.run_until_complete(self._ws_client.connect(event))
        
        
        # loop.run_until_complete(self.main_operation(bind_to_channels))
        asyncio.get_event_loop().run_until_complete(self.main_operation(bind_to_channels))
        print("Starting process_forever")
        logger.info("Authentication complete. Starting main loop...")
        # def pipe_forever():
        #     # asyncio.create_task(self._ws_client.pipe_receive())
        #     # loop.create_task(self._ws_client.pipe_receive())
        #     tasks = [
        #         # asyncio.ensure_future(self._ws_client.pipe_receive()), 
        #         asyncio.ensure_future(WSClient.pipe_middleware(self.child_pipe, self.second_parent_pipe)),
        #     ]
        #     loop.run_until_complete(asyncio.wait(tasks))
        #     # loop.create_task(WSClient.pipe_middleware(self.child_pipe, self.second_parent_pipe, loop))
        #     # loop.run_forever()
        # # self.loop.create_task(self._ws_client.pipe_receive())
        # # self.loop.run_forever()
        # # asyncio.create_task(self.pipe_receive())
        
        # process_forever = aioprocessing.AioProcess(target=WSClient.pipe_middleware, args=(self.child_pipe, self.second_parent_pipe, ))
        process_forever = aioprocessing.AioProcess(target=WSClient.pipe_middleware, args=(self.child_pipe, self.second_parent_pipe,))
        process_forever.start()
        
        
        
        
        # self._ws_client.init_pipe_middleware(self.child_pipe, event, lock)
        
        
        print("Finished starting process_forever")
    
    def get_wand(self):
        return MoobiusWand(self, self.parent_pipe)
    
        
    async def main_operation(self, bind_to_channels):
        await self._do_authenticate()
        # Connect to websocket server
        await self._ws_client.connect()
        print("Connected to websocket server.")

        # if no service_id is passed, create a new service
        self.service_id = self.service_id or self.http_api.create_service(description="Generated by MoobiusBasicService")
        
        if bind_to_channels:
            for channel_id in bind_to_channels:
                self.http_api.bind_service_to_channel(self.service_id, channel_id)
        else:
            pass
        
        self.scheduler.start()
        print("Scheduler started.")
        await self.on_start()
        print("on_start() finished.")

    @property
    def access_token(self):
        return self._access_token

    @property
    def refresh_token(self):
        return self._refresh_token


    async def handle_received_payload(self, payload):
        """
        Handle a received payload.
        """
        try:
            await self._handle_received_payload(payload)
        except Exception as e:
            traceback.print_exc()
            logger.error(f"MoobiusBasicService.handle_received_payload(): Error occurred: {e}")


    async def _handle_received_payload(self, payload):
        """
        Decode the received payload and handle based on its type.
        """
        payload_data = json.loads(payload)
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


    # =================== on_xxx, to be override ===================
    async def on_start(self):
        """
        Called when the service is initialized.
        """
        logger.info("Service started. Override this method to perform initialization tasks.")
        pass


    async def on_msg_up(self, msg_up: MessageUp):
        """
        Handle a payload from a user.
        """
        logger.info(f"MessageUp received: {msg_up}")
        pass

    async def on_fetch_userlist(self, action):
        """
        Handle the received action of fetching userlist.
        """
        logger.info("on_action fetch_userlist")
        pass
    
    async def on_fetch_features(self, action):
        """
        Handle the received action of fetching features.
        """
        logger.info("on_action fetch_features")
        pass
    
    async def on_fetch_playground(self, action):
        """
        Handle the received action of fetching playground.
        """
        logger.info("on_action fetch_playground")
        pass
    
    async def on_join_channel(self, action):
        """
        Handle the received action of joining channel.
        """
        logger.info("on_action join_channel")
        pass

    async def on_leave_channel(self, action):
        """
        Handle the received action of leaving channel.
        """
        logger.info("on_action leave_channel")
        pass
        
    async def on_fetch_channel_info(self, action):
        """
        Handle the received action of fetching channel info.
        """
        logger.info("on_action fetch_channel_info")
        pass
    
    async def on_action(self, action: Action):
        """
        Handle an action from a user.
        """
        logger.info(f"Action received: {action}")
        if action.subtype == "fetch_userlist":
            await self.on_fetch_userlist(action)
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
            logger.info(f"Unknown action subtype: {action.action_subtype}")

    async def on_feature_call(self, feature_call: FeatureCall):
        """
        Handle a feature call from a user.
        """
        logger.info(f"Feature call received: {feature_call}")
        pass


    async def on_copy(self, copy: Copy):
        """
        Handle a copy from Moobius.
        """
        #  print("Copy received:", copy)
        pass


    async def on_unknown_payload(self, payload: Payload):
        """
        Handle an unknown payload.
        """
        logger.info(f"Unknown payload received: {payload}")
        pass

    # =================== send_xxx, to be used ===================
    
    # fetch real users and set features to db
    async def fetch_real_characters(self, channel_id):
        """
        Fetches data from Moobius using HTTP request
        """
        
        data = self.http_api.get_channel_userlist(channel_id, self.service_id)

        if data["code"] == 10000:
            userlist = data["data"]["userlist"]

            return [from_dict(data_class=Character, data=d) for d in userlist]
        else:
            logger.error(f"fetch_real_characters error {data}")

            return []

    
    async def send(self, payload_type, payload_body):
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
        payload = self._ws_payload_builder.service_login(self.service_id, self.http_api.access_token)
        await self._ws_client.send(payload)

    async def send_msg_down(self, channel_id, recipients, subtype, message_content, sender):
        payload = self._ws_payload_builder.msg_down(self.service_id, channel_id, recipients, subtype, message_content, sender)
        await self._ws_client.send(payload)

    async def send_update(self, target_client_id, data):
        payload = self._ws_payload_builder.update(self.service_id, target_client_id, data)
        logger.info(payload)
        await self._ws_client.send(payload)

    async def send_update_userlist(self, channel_id, user_list, recipients):
        payload = self._ws_payload_builder.update_userlist(self.service_id, channel_id, user_list, recipients)
        logger.info(f"send_update_userlist {payload}")
        await self._ws_client.send(payload)

    async def send_update_channel_info(self, channel_id, channel_data):
        payload = self._ws_payload_builder.update_channel_info(self.service_id, channel_id, channel_data)
        logger.info(payload)
        await self._ws_client.send(payload)

    async def send_update_playground(self, channel_id, content, recipients):
        payload = self._ws_payload_builder.update_playground(self.service_id, channel_id, content, recipients)
        logger.info(payload)
        await self._ws_client.send(payload)

    async def send_update_features(self, channel_id, feature_data, recipients):
        payload = self._ws_payload_builder.update_features(self.service_id, channel_id, feature_data, recipients)
        logger.info(payload)
        await self._ws_client.send(payload)
    
    async def send_update_style(self, channel_id, style_content, recipients):
        payload = self._ws_payload_builder.update_style(self.service_id, channel_id, style_content, recipients)
        logger.info(payload)
        await self._ws_client.send(payload)

    async def send_ping(self):
        logger.info("Sending ping...")
        payload = self._ws_payload_builder.ping()
        await self._ws_client.send(payload)