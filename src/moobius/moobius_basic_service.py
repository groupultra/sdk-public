# moobius_basic_service.py

import asyncio
import json
import uuid
import traceback
import aioprocessing
import time

from dataclasses import asdict

from dacite import from_dict
from moobius.basic.ws_client import WSClient
from moobius.basic.ws_payload_builder import WSPayloadBuilder
from moobius.basic.http_api_wrapper import HTTPAPIWrapper
from moobius.basic.types import MessageUp, Action, FeatureCall, Copy, Payload, Character
from moobius.moobius_wand import MoobiusWand

class MoobiusBasicService:
    def __init__(self, http_server_uri="", ws_server_uri="", service_id="", email="", password="", **kwargs):
        self.http_api = HTTPAPIWrapper(http_server_uri)
        self.parent_pipe, self.child_pipe = aioprocessing.AioPipe()
        self._ws_client = WSClient(ws_server_uri, handle=self.handle_received_payload, horcrux=self.child_pipe)
        self._ws_payload_builder = WSPayloadBuilder()
        
        self._email = email
        self._password = password

        self._access_token = ""
        self._refresh_token = ""
        self.service_id = service_id
        
    def start(self, bind_to_channels=None):
        self.loop = asyncio.get_event_loop()
        self.loop.run_until_complete(self.main_operation(bind_to_channels))
        # asyncio.run(self.main_operation(bind_to_channels))
        print("Authentication complete. Starting main loop...")
        process_forever = aioprocessing.AioProcess(target=self.main_loop, args=())
        process_forever.start()
    
    def get_wand(self):
        return MoobiusWand(self, self.parent_pipe)
    
    async def main_operation(self, bind_to_channels):
        self._access_token, self._refresh_token = self.http_api.authenticate(self._email, self._password)
        await self._ws_client.connect()
        self.service_id = self.service_id or self.http_api.create_service(description="Generated by MoobiusBasicAgent")
        await self.send_service_login()
        if bind_to_channels:
            for channel_id in bind_to_channels:
                self.http_api.bind_service_to_channel(self.service_id, channel_id)
        else:
            pass

        await self.on_start()
        
    def main_loop(self):
        # self.loop = asyncio.get_event_loop()
        # self.loop = asyncio.new_event_loop()
        # asyncio.set_event_loop(self.loop)
        
        self.loop.create_task(self.send_heartbeat())
        self.loop.create_task(self._ws_client.pipe_receive())
        
        self.loop.run_forever()

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
            print("Error occurred:", e)


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
        print("Service started. Override this method to perform initialization tasks.")
        pass


    async def on_msg_up(self, msg_up: MessageUp):
        """
        Handle a payload from a user.
        """
        print("MessageUp received:", msg_up)
        pass

    async def on_fetch_userlist(self, action):
        """
        Handle the received action of fetching userlist.
        """
        print("on_action fetch_userlist")
        pass
    
    async def on_fetch_features(self, action):
        """
        Handle the received action of fetching features.
        """
        print("on_action fetch_features")
        pass
    
    async def on_fetch_playground(self, action):
        """
        Handle the received action of fetching playground.
        """
        print("on_action fetch_playground")
        pass
    
    async def on_join_channel(self, action):
        """
        Handle the received action of joining channel.
        """
        print("on_action join_channel")
        pass

    async def on_leave_channel(self, action):
        """
        Handle the received action of leaving channel.
        """
        print("on_action leave_channel")
        pass
        
    async def on_fetch_channel_info(self, action):
        """
        Handle the received action of fetching channel info.
        """
        print("on_action fetch_channel_info")
        pass
    
    async def on_action(self, action: Action):
        """
        Handle an action from a user.
        """
        print("Action received:", action)
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
            print("Unknown action subtype:", action_subtype)

    async def on_feature_call(self, feature_call: FeatureCall):
        """
        Handle a feature call from a user.
        """
        print("Feature call received:", feature_call)
        pass


    async def on_copy(self, copy: Copy):
        """
        Handle a copy from Moobius.
        """
        print("Copy received:", copy)
        pass


    async def on_unknown_payload(self, payload: Payload):
        """
        Handle an unknown payload.
        """
        print("Unknown payload received:", payload)
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
            print("fetch_real_characters error", data)

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

    async def send_service_login(self):
        payload = self._ws_payload_builder.service_login(self.service_id, self.access_token)
        print("payload", payload)
        await self._ws_client.send(payload)

    async def send_msg_down(self, channel_id, recipients, subtype, message_content, sender):
        payload = self._ws_payload_builder.msg_down(self.service_id, channel_id, recipients, subtype, message_content, sender)
        await self._ws_client.send(payload)

    async def send_update(self, target_client_id, data):
        payload = self._ws_payload_builder.update(self.service_id, target_client_id, data)
        print(payload)
        await self._ws_client.send(payload)

    async def send_update_userlist(self, channel_id, user_list, recipients):
        payload = self._ws_payload_builder.update_userlist(self.service_id, channel_id, user_list, recipients)
        print("send_update_userlist", payload)
        await self._ws_client.send(payload)

    async def send_update_channel_info(self, channel_id, channel_data):
        payload = self._ws_payload_builder.update_channel_info(self.service_id, channel_id, channel_data)
        print(payload)
        await self._ws_client.send(payload)

    async def send_update_playground(self, channel_id, content, recipients):
        payload = self._ws_payload_builder.update_playground(self.service_id, channel_id, content, recipients)
        print(payload)
        await self._ws_client.send(payload)

    async def send_update_features(self, channel_id, feature_data, recipients):
        payload = self._ws_payload_builder.update_features(self.service_id, channel_id, feature_data, recipients)
        print(payload)
        await self._ws_client.send(payload)
    
    async def send_update_style(self, channel_id, style_content, recipients):
        payload = self._ws_payload_builder.update_style(self.service_id, channel_id, style_content, recipients)
        print(payload)
        await self._ws_client.send(payload)

    async def send_ping(self):
        print("Sending ping...")
        payload = self._ws_payload_builder.ping()
        await self._ws_client.send(payload)

    async def send_heartbeat(self):
        """
        Send a ping payload every 30 seconds and check the response.
        """
        while True:
            await asyncio.sleep(30)
            try:
                await self.send_ping()
            except websockets.exceptions.ConnectionClosed:
                print("Connection closed. Attempting to reconnect...")
                await self.send_heartbeat()
                print("Reconnected!")
                break
            except Exception as e:
                traceback.print_exc()
                print("Error occurred:", e)
                await self.send_heartbeat()
                print("Reconnected!")
                break
            '''response = await self.websocket.recv()
            if not json.loads(response).get("status", False):
                await self.send_service_login()'''