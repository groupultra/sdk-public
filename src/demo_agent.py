# demo_agent.py

import asyncio
import json
from dataclasses import asdict

from moobius.moobius_agent import MoobiusAgent
from moobius.dbtools.moobius_band import MoobiusBand

class DemoAgent(MoobiusAgent):
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
            text_content = msg_up.content["text"]

            await self.send_msg_down(
                channel_id=msg_up.channel_id,
                recipients=msg_up.recipients,
                subtype="text",
                message_content=text_content,
                sender=msg_up.context.sender
            )
        else:
            pass

    async def on_action(self, action):
        """
        Handle the received action.
        """
        print("on_action", action)

        if action.subtype == "fetch_userlist":
            print("fetch_userlist")
            real_characters = self.bands[action.channel_id].real_characters
            user_list = list(real_characters.values())

            await self.send_update_userlist(action.channel_id, user_list, [action.sender])

        elif action.subtype == "fetch_features":
            print("fetch_features")
            features = self.bands[action.channel_id].features
            feature_data_list = list(features.values())

            await self.send_update_features(action.channel_id, feature_data_list, [action.sender])

        elif action.subtype == "fetch_playground":
            print("fetch_playground")
            """
            content = self.db_helper.get_playground_info(client_id)
            await self.send_update_playground(channel_id, content, [client_id])
            """
        elif action.subtype == "join_channel":
            print("join_channel")

        elif action.subtype == "fetch_channel_info":
            print("fetch_channel_info")
            """
            await self.send_update_channel_info(channel_id, self.db_helper.get_channel_info(channel_id))
            """
        else:
            raise Exception("Unknown action subtype:", action_subtype)

    async def on_feature_call(self, feature_call):
        """
        Handle the received feature call.
        """
        print("Feature call received:", feature_call)
        channel_id = feature_call.channel_id
        feature_id = feature_call.feature_id
        feature_name = self.bands[channel_id].features[feature_id]["feature_name"]
        character_dict = asdict(self.bands[channel_id].real_characters[feature_call.sender])
        nickname = character_dict["user_context"]["nickname"]   # todo: make it graceful!
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
