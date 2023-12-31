# agent.py

import json

from dacite import from_dict
from loguru import logger
from moobius.types import MessageBody, Character
from moobius import MoobiusAgent, MoobiusStorage, Moobius
import time

class NekoAgent(MoobiusAgent):
    def __init__(self, log_file="logs/agent.log", error_log_file="logs/error.log", **kwargs):
        super().__init__(**kwargs)
        self.log_file = log_file
        self.error_log_file = error_log_file

    # todo: channels and channel_ids, unbind_first, write back channels
    async def on_start(self):
        """
        Called after successful connection to websocket server and agent login success.
        """
        # ==================== load features ====================
        logger.add(self.log_file, rotation="1 day", retention="7 days", level="DEBUG")
        logger.add(self.error_log_file, rotation="1 day", retention="7 days", level="ERROR")

    # on_xxx, default implementation, to be override
    async def on_msg_down(self, msg_down: MessageBody):
        """
        Handle the received message.
        """
        if not msg_down['channel_id'] in self.bands:
            self.bands[msg_down['channel_id']] = MoobiusStorage(self.agent_id, msg_down['channel_id'], db_config=self.db_config)       
            await self.send_fetch_userlist(msg_down['channel_id'])
            await self.send_fetch_features(msg_down['channel_id'])
        
        if msg_down['context']['sender'] == self.agent_id:
            # avoid infinite loop
            return
        
        if msg_down['subtype'] == "text":
            if msg_down['content']['text'] == "nya":
                msg_down['content']['text'] = "meow"
            elif msg_down['content']['text'] == "meow":
                msg_down['content']['text'] = "nya"

            msg_down['content']['text'] = f"agent repeat: {msg_down['content']['text']}"

        msg_down['timestamp'] = int(time.time() * 1000)
        recipients = [msg_down['sender']]
        msg_down['recipients'] = recipients

        await self.send(payload_type='msg_up', payload_body=msg_down)
        
    async def on_update_userlist(self, update):
        for user in update['userlist']:
            self.bands[update['channel_id']].characters[user['user_id']] = from_dict(data_class=Character, data=user)
        
    async def on_update_features(self, update):
        print("agent_update_features", update['features'])
        # update features [{'feature_id': 'key1', 'feature_name': 'name1', 'button_text': 'Meet Tubbs or Hermeowne', 'new_window': True, 'arguments': [{'name': 'arg1', 'type': 'enum', 'optional': False, 'values': ['Meet Tubbs', 'Meet Hermeowne'], 'placeholder': 'placeholder'}]}, {'feature_id': 'key2', 'feature_name': 'name2', 'button_text': 'Meet Ms Fortune', 'new_window': False, 'arguments': None}]
        self.bands[update['channel_id']].features = update['features']
    
    async def on_update_playground(self, update):
        print("agent_on_update_playground", update)
        # agent_on_update_playground {'subtype': 'update_playground', 'channel_id': '32f38b98-2ac5-4ada-8945-52a845a0d574', 'content': {'path': 'https://social-public-bucket-1.s3.amazonaws.com/32947f5b-3951-43ad-8fc5-d7d898efc5ec.png', 'text': "I'm Tubbs on playground!"}, 'group_id': 'temp', 'context': {}}
    
    async def on_fetch_channel_info(self, update):
        print("agent_on_fetch_channel_info", update)
        
    async def on_feature_call(self, feature_call):
        print("agent_on_feature_call", feature_call)
        
    
    async def on_spell(self, text):
        # 7 Actions
        if text == "send_fetch_userlist":
            for channel_id in self.bands:
                await self.send_fetch_userlist(channel_id)
        elif text == "send_fetch_features":
            for channel_id in self.bands:
                await self.send_fetch_features(channel_id)
        # elif text == "send_fetch_style":
        #     for channel_id in self.bands:
        #         await self.send_fetch_style(channel_id)
        elif text == "send_fetch_playground":
            for channel_id in self.bands:
                await self.send_fetch_playground(channel_id)
        elif text == "send_join_channel":
            for channel_id in self.bands:
                await self.send_join_channel(channel_id)
        elif text == "send_leave_channel":
            for channel_id in self.bands:
                await self.send_leave_channel(channel_id)
        elif text == "send_fetch_channel_info":
            for channel_id in self.bands:
                await self.send_fetch_channel_info(channel_id)
        elif text == "send_feature_call_key1":
            for channel_id in self.bands:
                for feature in self.bands[channel_id].features:
                    if feature['feature_id'] == "key1":
                        await self.send_feature_call(channel_id, "key1", [('arg1', "Meet Tubbs")])
        elif text == "send_feature_call_key2":
            for channel_id in self.bands:
                for feature in self.bands[channel_id].features:
                    if feature['feature_id'] == "key2":
                        await self.send_feature_call(channel_id, "key2", [])
        elif text == "nya_all":
            for channel_id in self.bands:
                recipients = list(self.bands[channel_id].characters.keys())
                await self.create_message(channel_id, "nya nya nya", recipients)