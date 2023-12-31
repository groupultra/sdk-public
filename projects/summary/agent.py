# agent.py

import json
import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from dacite import from_dict
from loguru import logger
from openai import AsyncOpenAI
from moobius.types import MessageBody, Character
from moobius import MoobiusAgent, MoobiusStorage, Moobius


class SummaryAgent(MoobiusAgent):
    def __init__(self, log_file="logs/agent.log", error_log_file="logs/error.log", **kwargs):
        super().__init__(**kwargs)
        self.log_file = log_file
        self.error_log_file = error_log_file
        self.summary_interval = 30 # 30s summary interval for testing
        

    # todo: channels and channel_ids, unbind_first, write back channels
    async def on_start(self):
        """
        Called after successful connection to websocket server and agent login success.
        """
        # ==================== load features ====================
        logger.add(self.log_file, rotation="1 day", retention="7 days", level="DEBUG")
        logger.add(self.error_log_file, rotation="1 day", retention="7 days", level="ERROR")
        scheduler = AsyncIOScheduler()
        scheduler.add_job(self._do_summary, 'interval', seconds=self.summary_interval)
        scheduler.start()
        self.openai_client = AsyncOpenAI()
        
    async def _do_summary(self):
        print("do_summary", self.bands)
        for channel_id in self.bands:
            recipients = list(self.bands[channel_id].characters.keys())
            prompt = 'Summarize these chat messages:\n\n'
            channel_history = ""
            for k in self.bands[channel_id].messages:
                channel_history += f'{k}: {self.bands[channel_id].messages[k]}\n'
            self.bands[channel_id].messages = {}
            response = await self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": prompt + channel_history
                            }
                        ],
                    }
                ],
                max_tokens=1000,
            )

            summary_history = response.choices[0].message.content
            await self.create_message(channel_id, summary_history, recipients)
        
    # on_xxx, default implementation, to be override
    async def on_msg_down(self, msg_down: MessageBody):
        """
        Handle the received message.
        """
        if not msg_down['channel_id'] in self.bands:
            self.bands[msg_down['channel_id']] = MoobiusStorage(self.agent_id, msg_down['channel_id'], db_config=self.db_config)       
            await self.send_fetch_userlist(msg_down['channel_id'])
            await self.send_fetch_features(msg_down['channel_id'])
        
        if msg_down['sender'] == self.agent_id:
            # avoid infinite loop
            return
        
        if msg_down['subtype'] == "text":
            timestamp_str = datetime.datetime.fromtimestamp(msg_down['timestamp'] / 1000).strftime('%Y-%m-%d %H:%M:%S')
            self.bands[msg_down['channel_id']].messages[msg_down['sender'] + ' ' + timestamp_str] = msg_down['content']['text']
        
    async def on_update_userlist(self, update):
        print("agent_update_userlist", update)
        # agent_update_userlist {'subtype': 'update_userlist', 'channel_id': 'a117ccdb-7f36-4261-9bac-db9273e5eccd', 'userlist': [{'user_id': '321e7409-e19a-4608-a623-2bae497568d0', 'context': {'nickname': 'Kamisato Ayaka', 'description': 'Master of Inazuma Kamisato Art Tachi Jutsu — Kamisato Ayaka, present!', 'avatar': 'https://social-public-bucket-1.s3.amazonaws.com/b32086f5-0806-4636-870e-d3aa11c13ba4.15.05 PM.png'}}, {'user_id': '9a5e0ac1-c1ba-42e6-a661-db2151dede25', 'context': {'avatar': 'https://social-public-bucket-1.s3.amazonaws.com/beddf326-f88e-4e93-8994-f0acd3265f91.png.webp', 'description': 'I am a Moobius Character.', 'nickname': 'Kirara'}}, {'user_id': 'b42d0cb1-b97a-4c63-bbab-1d456cc26490', 'context': {'avatar': 'https://social-public-bucket-1.s3.amazonaws.com/9f18f213-6142-4b28-b5cf-632e9e2faf78.26.10 PM.png', 'description': 'The maid of all maids', 'nickname': 'Noelle'}}], 'context': {}}
        for user in update['userlist']:
            self.bands[update['channel_id']].characters[user['user_id']] = user
        
    async def on_update_features(self, update):
        print("agent_update_features", update['features'])
        # update features [{'feature_id': 'key1', 'feature_name': 'name1', 'button_text': 'Meet Tubbs or Hermeowne', 'new_window': True, 'arguments': [{'name': 'arg1', 'type': 'enum', 'optional': False, 'values': ['Meet Tubbs', 'Meet Hermeowne'], 'placeholder': 'placeholder'}]}, {'feature_id': 'key2', 'feature_name': 'name2', 'button_text': 'Meet Ms Fortune', 'new_window': False, 'arguments': None}]
        self.bands[update['channel_id']].features = update['features']
    
    # async def on_update_playground(self, update):
    #     print("agent_on_update_playground", update)
    #     # agent_on_update_playground {'subtype': 'update_playground', 'channel_id': '32f38b98-2ac5-4ada-8945-52a845a0d574', 'content': {'path': 'https://social-public-bucket-1.s3.amazonaws.com/32947f5b-3951-43ad-8fc5-d7d898efc5ec.png', 'text': "I'm Tubbs on playground!"}, 'group_id': 'temp', 'context': {}}
    
    # async def on_fetch_channel_info(self, update):
    #     print("agent_on_fetch_channel_info", update)
        
    # async def on_feature_call(self, feature_call):
    #     print("agent_on_feature_call", feature_call)
        
    
    # async def on_spell(self, text):
    #     # 7 Actions
    #     if text == "send_fetch_userlist":
    #         for channel_id in self.bands:
    #             await self.send_fetch_userlist(channel_id)
    #     elif text == "send_fetch_features":
    #         for channel_id in self.bands:
    #             await self.send_fetch_features(channel_id)
    #     # elif text == "send_fetch_style":
    #     #     for channel_id in self.bands:
    #     #         await self.send_fetch_style(channel_id)
    #     elif text == "send_fetch_playground":
    #         for channel_id in self.bands:
    #             await self.send_fetch_playground(channel_id)
    #     elif text == "send_join_channel":
    #         for channel_id in self.bands:
    #             await self.send_join_channel(channel_id)
    #     elif text == "send_leave_channel":
    #         for channel_id in self.bands:
    #             await self.send_leave_channel(channel_id)
    #     elif text == "send_fetch_channel_info":
    #         for channel_id in self.bands:
    #             await self.send_fetch_channel_info(channel_id)
    #     elif text == "send_feature_call_key1":
    #         for channel_id in self.bands:
    #             for feature in self.bands[channel_id].features:
    #                 if feature['feature_id'] == "key1":
    #                     await self.send_feature_call(channel_id, "key1", [('arg1', "Meet Tubbs")])
    #     elif text == "send_feature_call_key2":
    #         for channel_id in self.bands:
    #             for feature in self.bands[channel_id].features:
    #                 if feature['feature_id'] == "key2":
    #                     await self.send_feature_call(channel_id, "key2", [])
    #     elif text == "nya_all":
    #         for channel_id in self.bands:
    #             recipients = list(self.bands[channel_id].characters.keys())
    #             await self.create_message(channel_id, "nya nya nya", recipients)