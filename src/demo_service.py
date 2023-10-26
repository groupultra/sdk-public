# demo_service.py

import asyncio
import json

from moobius.moobius_service import MoobiusService
from moobius.basic.types import Character
from moobius.dbtools.moobius_band import MoobiusBand
from dacite import from_dict

class DemoService(MoobiusService):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        

    async def on_start(self):
        """
        Called after successful connection to websocket server and service login success.
        """
        li = self.http_api.get_service_list()
        self.channel_ids = []

        for d in li:
            if d.get('service_id', None) == self.service_id:
                self.channel_ids = d.get('channel_ids', [])
                break

        print("channel_ids", self.channel_ids)
        
        # ==================== load features ====================
        with open('demo_features.json', 'r') as f:
            features = json.load(f)

        for channel_id in self.channel_ids:
            self.bands[channel_id] = MoobiusBand(self.service_id, channel_id, db_settings=self.db_settings)
            real_characters = await self.fetch_real_characters(channel_id)

            for character in real_characters:
                character_id = character.user_id
                self.bands[channel_id].real_characters[character_id] = character

            for feature in features:
                feature_id = feature["feature_id"]
                self.bands[channel_id].features[feature_id] = feature


    # on_xxx, default implementation, to be override
    async def on_msg_up(self, msg_up):
        """
        Handle the received message.
        """
        print("on_msg_up", msg_up)
        if msg_up.subtype == "text":
            if msg_up.content['text'] == "ping":
                msg_up.content['text'] = "pong"
        msg_down = self.msg_up_to_msg_down(msg_up)
        
        await self.send(payload_type='msg_down', payload_body=msg_down)

    async def on_feature_call(self, feature_call):
        """
        Handle the received feature call.
        """
        print("Feature call received:", feature_call)
        channel_id = feature_call.channel_id
        feature_id = feature_call.feature_id
        feature_name = self.bands[channel_id].features[feature_id]["feature_name"]
        character = self.bands[channel_id].real_characters[feature_call.sender]
        nickname = character.user_context.nickname
        recipients = list(self.bands[channel_id].real_characters.keys())

        await self.send_msg_down(
            channel_id=channel_id,
            recipients=recipients,
            subtype="text",
            message_content=f'{nickname} clicked {feature_name}!',
            sender=feature_call.sender
        )
        

    async def on_unknown_message(self, message_data):
        """
        Handle the received unknown message.
        """
        print("Received unknown message:", message_data)
