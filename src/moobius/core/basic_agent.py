# basic_agent.py

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
from moobius.types import MessageBody, Action, FeatureCall, FeatureCallArgument, Copy, Payload
from loguru import logger


class MoobiusBasicAgent:
    def __init__(self, config_path="", **kwargs):
        self.config_path = config_path

        with open(self.config_path, "r") as f:
            self.config = json.load(f)

        http_server_uri = self.config["http_server_uri"]
        ws_server_uri = self.config["ws_server_uri"]
        email = self.config["email"]
        password = self.config["password"]
        
        self.channels = []  # real channel ids. Not necessarily the same as self.config["channels"]

        self.http_api = HTTPAPIWrapper(http_server_uri, email, password)
        self._ws_client = WSClient(ws_server_uri, on_connect=self.send_agent_login, handle=self.handle_received_payload)
        self._ws_payload_builder = WSPayloadBuilder()

        self.queue = aioprocessing.AioQueue()
        
        self.refresh_interval = 6 * 60 * 60             # 24h expire, 6h refresh
        self.authenticate_interval = 7 * 24 * 60 * 60   # 30d expire, 7d refresh
        self.heartbeat_interval = 30                    # 30s heartbeat

        self.scheduler = None

    # =================== jobs ===================

    # todo: if token expires for some reason, do authentication again
    async def _do_send_heartbeat(self):
        await self.send_heartbeat()

    # this method will automatically set http_api headers
    async def _do_refresh(self):
        access_token = self.http_api.refresh()
        logger.info(f"Refreshed access token: {access_token}")

    # this method will automatically set http_api headers
    async def _do_authenticate(self):
        access_token, refresh_token = self.http_api.authenticate()
        logger.info(f"Authenticated. Access token: {access_token}")


    async def _get_agent_info(self):
        self.agent_info = self.http_api.get_user_info()
        self.agent_id = self.agent_info["sub"]
        
    # =================== start ===================
    
    # todo: config["others"]: "ignore" (default) | "unbind" | "include"
    async def start(self):
        logger.debug("Starting agent...")
        
        await self._do_authenticate()
        await self._ws_client.connect()
        logger.debug("Connected to websocket server.")
        
        await self._get_agent_info()
        await self.send_agent_login()

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
        while True:
            obj = await self.queue.coro_get()
            await self.on_spell(obj)


    @logger.catch
    async def handle_received_payload(self, payload):
        payload_data = json.loads(payload)
        if 'type' in payload_data:
            if payload_data['type'] == "msg_down":
                await self.on_msg_down(payload_data['body'])
            elif payload_data['type'] == "update":
                await self.on_update(payload_data['body'])
            elif payload_data['type'] == "copy_client":
                await self.on_copy_client(payload_data['body'])
            else:   # todo: add types (copy_client etc)
                await self.on_unknown_payload(payload)
        else:
            logger.error(f"Unknown payload without type: {payload_data}")

    # =================== on_xxx, to be override ===================

    async def on_spell(self, obj):
        logger.debug(f'Spell Received {obj}')
        pass

    async def on_start(self):
        logger.debug("Agent started. Override this method to perform initialization tasks.")
        pass

    async def on_msg_down(self, msg_down: MessageBody):
        logger.debug(f"MessageDown received: {msg_down}")
        pass

    async def on_update(self, update):
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

    async def on_update_userlist(self, update):
        logger.debug("on_update_user_list")
        pass

    async def on_update_channel_info(self, update):
        logger.debug("on_update_channel_info")
        pass

    async def on_update_playground(self, update):
        logger.debug("on_update_playground")
        pass

    async def on_update_features(self, update):
        logger.debug("on_update_features")
        pass

    async def on_update_style(self, update):
        logger.debug("on_update_style")
        pass
    
    async def on_copy_client(self, copy: Copy):
        logger.debug("on_copy_client")
        pass

    async def on_unknown_payload(self, payload: Payload):
        logger.debug(f"Unknown payload received: {payload}")
        pass

    # =================== send_xxx, to be used ===================
    
    async def send(self, payload_type, payload_body):
        if isinstance(payload_body, dict):
            payload_dict = {
                'type': payload_type,
                'request_id': str(uuid.uuid4()),
                'client_id': self.agent_id,
                'body': payload_body
            }
        else:
            payload_obj = Payload(
                type=payload_type,
                request_id=str(uuid.uuid4()),
                client_id=self.agent_id,
                body=payload_body
            )
            payload_dict = asdict(payload_obj)

        payload_str = self._ws_payload_builder.dumps(payload_dict)
        await self._ws_client.send(payload_str)

    # todo: decouple access_token here!
    # every 2h aws force disconnect, so we send agent_login on connect
    async def send_agent_login(self):
        payload = self._ws_payload_builder.agent_login(self.http_api.access_token)
        print("send_agent_login payload", payload)
        await self._ws_client.send(payload)

    async def send_msg_up(self, channel_id, recipients, subtype, message_content):
        payload = self._ws_payload_builder.msg_up(self.agent_id, channel_id, recipients, subtype, message_content)
        await self._ws_client.send(payload)

    async def send_heartbeat(self):
        payload = self._ws_payload_builder.ping()
        await self._ws_client.send(payload)
        
    async def send_fetch_userlist(self, channel_id):
        print("send_fetch_userlist", channel_id)
        payload = self._ws_payload_builder.fetch_userlist(self.agent_id, channel_id)
        await self._ws_client.send(payload)
    
    async def send_fetch_features(self, channel_id):
        payload = self._ws_payload_builder.fetch_features(self.agent_id, channel_id)
        await self._ws_client.send(payload)
        
    async def send_fetch_style(self, channel_id):
        payload = self._ws_payload_builder.fetch_style(self.agent_id, channel_id)
        await self._ws_client.send(payload)
    
    async def send_fetch_playground(self, channel_id):
        payload = self._ws_payload_builder.fetch_playground(self.agent_id, channel_id)
        await self._ws_client.send(payload)
    
    async def send_fetch_channel_info(self, channel_id):
        payload = self._ws_payload_builder.fetch_channel_info(self.agent_id, channel_id)
        await self._ws_client.send(payload)
    
    async def send_feature_call(self, channel_id, feature_id, feature_args):
        feature_call_instance = FeatureCall(
            feature_id=feature_id,
            channel_id=channel_id,
            sender=self.agent_id,
            arguments=[FeatureCallArgument(name=arg[0], value=arg[1]) for arg in feature_args],
            context={}
        )
        await self.send("feature_call", feature_call_instance)
    
    async def send_join_channel(self, channel_id):
        payload = self._ws_payload_builder.join_channel(self.agent_id, channel_id)
        await self._ws_client.send(payload)
    
    async def send_leave_channel(self, channel_id):
        payload = self._ws_payload_builder.leave_channel(self.agent_id, channel_id)
        await self._ws_client.send(payload)