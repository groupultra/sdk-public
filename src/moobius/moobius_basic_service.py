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
from moobius.basic.logging_config import log

class MoobiusBasicService:
    def __init__(self, config_path="", **kwargs):
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
        payload = self._ws_payload_builder.ping()
        await self._ws_client.send(payload)

    # this method will automatically set http_api headers
    async def _do_refresh(self):
        access_token = self.http_api.refresh()
        log(f"Refreshed access token: {access_token}")

    # this method will automatically set http_api headers
    async def _do_authenticate(self):
        access_token, refresh_token = self.http_api.authenticate()
        log(f"Authenticated. Access token: {access_token}")

    # =================== start ===================
    
    # todo: config["others"]: "ignore" (default) | "unbind" | "include"
    async def start(self):
        log("Starting service...")
        
        await self._do_authenticate()
        await self._ws_client.connect()
        log("Connected to websocket server.")
        
        if not self.service_id:
            log('No service_id in config file. Will create a new service if necessary.')
        else:
            pass
            
        service_list = self.http_api.get_service_list()
        log(f"{service_list}")
        log(f"Service ID: {self.service_id}")
        
        # find all channels that could be run on later
        for channel_id in set(self.config["channels"]):
            for service in service_list:
                if service["service_id"] == self.service_id:    # default service_id is "", which is not in service_list
                    self.channels.append(channel_id)    # would be rebinded
                    break
                else:
                    if channel_id in service["channel_ids"]:
                        log(f"Channel {channel_id} already binded to a service_id: {service['service_id']}")
                        break
                    else:
                        continue
            else:
                self.channels.append(channel_id)

        log(f"Channels to bind: {self.channels}")

        if not self.channels:
            log("No proper channel to run on. The process will exit. Please check your config file.")
            
            return
        else:
            if not self.service_id:
                self.service_id = self.http_api.create_service(description="Generated by MoobiusBasicService")

                log(f"NEW SERVICE CREATED!!!")
                log("=================================================", color="magenta")
                log(f" Service ID: {self.service_id}", color="cyan")
                log("=================================================", color="magenta")
                log(f"Please wait for 5 seconds...")

                await asyncio.sleep(5)
            else:
                pass

            for channel_id in self.channels:
                bind_info = self.http_api.bind_service_to_channel(self.service_id, channel_id)  # may already be binded to the service itself
                log(f"Bind service to channel {channel_id}: {bind_info}")

            try:
                with open(self.config_path, "r") as f:
                    f.seek(0)
                    data = json.load(f)
            except:
                log("No config file found. Creating a new one...")
                data = {}

            data["service_id"] = self.service_id
            data["channels"] = self.channels

            with open(self.config_path, "w") as f:
                json.dump(data, f, indent=4)

            log(f"Config file updated: {self.config_path}")
            await self.send_service_login()

            # Schedulers cannot be serialized so that you have to initialize it here
            self.scheduler = AsyncIOScheduler()

            # The details of access_token and refresh_token are managed by self.http_api
            self.scheduler.add_job(self._do_refresh, 'interval', seconds=self.refresh_interval)
            self.scheduler.add_job(self._do_authenticate, 'interval', seconds=self.authenticate_interval)
            self.scheduler.add_job(self._do_send_heartbeat, 'interval', seconds=self.heartbeat_interval)

            self.scheduler.start()
            log("Scheduler started.")

            await self.on_start()
            log("on_start() finished.")

            await asyncio.gather(self._ws_client.receive(), self.listen())
    
    async def listen(self):
        while True:
            try:
                obj = await self.queue.coro_get()
                await self.on_spell(obj)
            except Exception as e:
                traceback.print_exc()

    async def handle_received_payload(self, payload):
        """
        Handle a received payload.
        """
        try:
            await self._handle_received_payload(payload)
        except Exception as e:
            traceback.print_exc()
            log(f"MoobiusBasicService.handle_received_payload(): Error occurred: {e}", error=True)


    async def _handle_received_payload(self, payload):
        """
        Decode the received payload and handle based on its type.
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
            log(f"MoobiusBasicService.handle_received_payload(): Unknown payload without type: {payload_data}", error=True)
    


    # =================== on_xxx, to be override ===================

    async def on_spell(self, obj):
        """
        Called when a spell is received.
        """
        print(f'MoobiusBasicService.on_spell: {obj}')
        pass


    async def on_start(self):
        """
        Called when the service is initialized.
        """
        log("Service started. Override this method to perform initialization tasks.")
        pass


    async def on_msg_up(self, msg_up: MessageUp):
        """
        Handle a payload from a user.
        """
        log(f"MessageUp received: {msg_up}")
        pass

    async def on_fetch_userlist(self, action):
        """
        Handle the received action of fetching userlist.
        """
        log("on_action fetch_userlist")
        pass
    
    async def on_fetch_features(self, action):
        """
        Handle the received action of fetching features.
        """
        log("on_action fetch_features")
        pass
    
    async def on_fetch_playground(self, action):
        """
        Handle the received action of fetching playground.
        """
        log("on_action fetch_playground")
        pass
    
    async def on_join_channel(self, action):
        """
        Handle the received action of joining channel.
        """
        log("on_action join_channel")
        pass

    async def on_leave_channel(self, action):
        """
        Handle the received action of leaving channel.
        """
        log("on_action leave_channel")
        pass
        
    async def on_fetch_channel_info(self, action):
        """
        Handle the received action of fetching channel info.
        """
        log("on_action fetch_channel_info")
        pass
    
    async def on_action(self, action: Action):
        """
        Handle an action from a user.
        """
        log(f"Action received: {action}")
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
            log(f"Unknown action subtype: {action.action_subtype}")

    async def on_feature_call(self, feature_call: FeatureCall):
        """
        Handle a feature call from a user.
        """
        log(f"Feature call received: {feature_call}")
        pass


    async def on_copy(self, copy: Copy):
        """
        Handle a copy from Moobius.
        """
        if not copy.status:
            await self.send_service_login()
        else:
            pass


    async def on_unknown_payload(self, payload: Payload):
        """
        Handle an unknown payload.
        """
        log(f"Unknown payload received: {payload}")
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
        log(payload)
        await self._ws_client.send(payload)

    async def send_update_userlist(self, channel_id, user_list, recipients):
        payload = self._ws_payload_builder.update_userlist(self.service_id, channel_id, user_list, recipients)
        log(payload)
        await self._ws_client.send(payload)

    async def send_update_channel_info(self, channel_id, channel_data):
        payload = self._ws_payload_builder.update_channel_info(self.service_id, channel_id, channel_data)
        log(payload)
        await self._ws_client.send(payload)

    async def send_update_playground(self, channel_id, content, recipients):
        payload = self._ws_payload_builder.update_playground(self.service_id, channel_id, content, recipients)
        log(payload)
        await self._ws_client.send(payload)

    async def send_update_features(self, channel_id, feature_data, recipients):
        payload = self._ws_payload_builder.update_features(self.service_id, channel_id, feature_data, recipients)
        log(payload)
        await self._ws_client.send(payload)
    
    async def send_update_style(self, channel_id, style_content, recipients):
        payload = self._ws_payload_builder.update_style(self.service_id, channel_id, style_content, recipients)
        log(payload)
        await self._ws_client.send(payload)

    async def send_ping(self):
        log("Sending ping...")
        payload = self._ws_payload_builder.ping()
        await self._ws_client.send(payload)