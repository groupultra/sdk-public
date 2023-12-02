# moobius_basic_service.py

import asyncio
import json
import time
import uuid
import traceback
import aioprocessing
import time
import threading
from dataclasses import asdict
from dacite import from_dict
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from moobius.basic.ws_client import WSClient
from moobius.basic.ws_payload_builder import WSPayloadBuilder
from moobius.basic.http_api_wrapper import HTTPAPIWrapper
from moobius.basic._types import MessageUp, Action, FeatureCall, Copy, Payload, Character
from moobius.moobius_wand import MoobiusWand
from moobius.basic.logging_config import log_info, log_error

class MoobiusBasicService:
    def __init__(self, http_server_uri="", ws_server_uri="", service_id="", email="", password="", create_new=True, **kwargs):
        self.http_api = HTTPAPIWrapper(http_server_uri, email, password)
        self.queue = aioprocessing.AioQueue()
        self.create_new = create_new
        
        self._ws_client = WSClient(ws_server_uri, on_connect=self.send_service_login, handle=self.handle_received_payload)
        self._ws_payload_builder = WSPayloadBuilder()
        
        
        self.refresh_interval = 6 * 60 * 60             # 24h expire, 6h refresh
        self.authenticate_interval = 7 * 24 * 60 * 60   # 30d expire, 7d refresh
        self.heartbeat_interval = 30                    # 30s heartbeat
        self.service_id = service_id

    # =================== jobs ===================

    # todo: if token expires for some reason, do authentication again
    async def _do_send_heartbeat(self):
        payload = self._ws_payload_builder.ping()
        await self._ws_client.send(payload)

    # this method will automatically set http_api headers
    async def _do_refresh(self):
        access_token = self.http_api.refresh()
        log_info(f"Refreshed access token: {access_token}")

    # this method will automatically set http_api headers
    async def _do_authenticate(self):
        access_token, refresh_token = self.http_api.authenticate()
        log_info(f"Authenticated. Access token: {access_token}")

    # =================== start ===================
    
    async def start(self, bind_to_channels=None):
        log_info("Starting service...")
        
        await self._do_authenticate()
        # Connect to websocket server
        await self._ws_client.connect()
        log_info("Connected to websocket server.")
        
        if self.create_new:
            if bind_to_channels:
                for channel_id in bind_to_channels:
                    unbind_info = self.http_api.unbind_service_from_channel(self.service_id, channel_id)
                    log_info(f"Unbind to channel {channel_id}: {unbind_info}")
            self.service_id = self.http_api.create_service(description="Generated by MoobiusBasicService")
            log_info(f"Service ID: {self.service_id}, waiting for 5 seconds to bind to channels...")
            print(f"\033[1;35m=================================================\033[0m")
            print(f"\033[1;36m Service ID:{self.service_id}\033[0m")
            print(f"\033[1;35m=================================================\033[0m")
            try:
                with open("config.json", "r") as f:
                    old_data = json.load(f)
            except FileNotFoundError:
                print("JSON file not found. Creating a new one.")
                old_data = {}
            new_data = old_data
            new_data["service_id"] = self.service_id
            new_data["create_new"] = False
            with open("config.json", "w") as f:
                json.dump(new_data, f, indent=4)
        else:
            pass
        
        # make sure service is created
        time.sleep(5)
        
        if bind_to_channels:
            for channel_id in bind_to_channels:
                bind_info = self.http_api.bind_service_to_channel(self.service_id, channel_id)
                log_info(f"Bind to channel {channel_id}: {bind_info}")
        else:
            pass
        
        self.scheduler = AsyncIOScheduler()
        
        # The details of access_token and refresh_token are managed by self.http_api
        self.scheduler.add_job(self._do_refresh, 'interval', seconds=self.refresh_interval)
        self.scheduler.add_job(self._do_authenticate, 'interval', seconds=self.authenticate_interval)
        self.scheduler.add_job(self._do_send_heartbeat, 'interval', seconds=self.heartbeat_interval)

        self.scheduler.start()
        log_info("Scheduler started.")

        await self.on_start()
        log_info("on_start() finished.")
        
        
        await self._ws_client.connect()
        recv_task = self._ws_client.receive()
        listen_task = self.listen()
        await asyncio.gather(recv_task, listen_task)
    
    async def listen(self):
        while True:
            try:
                message = await self.queue.coro_get()
                await self.handle_queue_message(message)
            except Exception as e:
                traceback.print_exc()

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
            log_error(f"MoobiusBasicService.handle_received_payload(): Error occurred: {e}")


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
    
    async def handle_queue_message(self, message):
        if message[:4] == "RECV":
            payload = message[4:]
            await self.handle_received_payload(payload)
        else:
            await self._ws_client.send(message)


    # =================== on_xxx, to be override ===================
    async def on_start(self):
        """
        Called when the service is initialized.
        """
        log_info("Service started. Override this method to perform initialization tasks.")
        pass


    async def on_msg_up(self, msg_up: MessageUp):
        """
        Handle a payload from a user.
        """
        log_info(f"MessageUp received: {msg_up}")
        pass

    async def on_fetch_userlist(self, action):
        """
        Handle the received action of fetching userlist.
        """
        log_info("on_action fetch_userlist")
        pass
    
    async def on_fetch_features(self, action):
        """
        Handle the received action of fetching features.
        """
        log_info("on_action fetch_features")
        pass
    
    async def on_fetch_playground(self, action):
        """
        Handle the received action of fetching playground.
        """
        log_info("on_action fetch_playground")
        pass
    
    async def on_join_channel(self, action):
        """
        Handle the received action of joining channel.
        """
        log_info("on_action join_channel")
        pass

    async def on_leave_channel(self, action):
        """
        Handle the received action of leaving channel.
        """
        log_info("on_action leave_channel")
        pass
        
    async def on_fetch_channel_info(self, action):
        """
        Handle the received action of fetching channel info.
        """
        log_info("on_action fetch_channel_info")
        pass
    
    async def on_action(self, action: Action):
        """
        Handle an action from a user.
        """
        log_info(f"Action received: {action}")
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
            log_info(f"Unknown action subtype: {action.action_subtype}")

    async def on_feature_call(self, feature_call: FeatureCall):
        """
        Handle a feature call from a user.
        """
        log_info(f"Feature call received: {feature_call}")
        pass


    async def on_copy(self, copy: Copy):
        """
        Handle a copy from Moobius.
        """
        pass


    async def on_unknown_payload(self, payload: Payload):
        """
        Handle an unknown payload.
        """
        log_info(f"Unknown payload received: {payload}")
        pass

    # =================== send_xxx, to be used ===================
    
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
        log_info(payload)
        await self._ws_client.send(payload)

    async def send_update_userlist(self, channel_id, user_list, recipients):
        payload = self._ws_payload_builder.update_userlist(self.service_id, channel_id, user_list, recipients)
        log_info(payload)
        await self._ws_client.send(payload)

    async def send_update_channel_info(self, channel_id, channel_data):
        payload = self._ws_payload_builder.update_channel_info(self.service_id, channel_id, channel_data)
        log_info(payload)
        await self._ws_client.send(payload)

    async def send_update_playground(self, channel_id, content, recipients):
        payload = self._ws_payload_builder.update_playground(self.service_id, channel_id, content, recipients)
        log_info(payload)
        await self._ws_client.send(payload)

    async def send_update_features(self, channel_id, feature_data, recipients):
        payload = self._ws_payload_builder.update_features(self.service_id, channel_id, feature_data, recipients)
        log_info(payload)
        await self._ws_client.send(payload)
    
    async def send_update_style(self, channel_id, style_content, recipients):
        payload = self._ws_payload_builder.update_style(self.service_id, channel_id, style_content, recipients)
        log_info(payload)
        await self._ws_client.send(payload)

    async def send_ping(self):
        log_info("Sending ping...")
        payload = self._ws_payload_builder.ping()
        await self._ws_client.send(payload)