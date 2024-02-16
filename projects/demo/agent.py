# Defines class NekoAgent(MoobiusAgent).

import json, asyncio

from dacite import from_dict
from loguru import logger
from moobius.types import MessageBody, Character
from moobius import SDK, MoobiusStorage, Moobius
import time


class DemoAgent(SDK):
    def __init__(self, log_file="logs/agent.log", error_log_file="logs/error.log", **kwargs):
        super().__init__(**kwargs)
        self.log_file = log_file
        self.error_log_file = error_log_file

    # todo: channels and channel_ids, unbind_first, write back channels
    async def on_start(self):
        """Called after successful connection to websocket server and agent login success. Launches join tasks."""
        logger.add(self.log_file, rotation="1 day", retention="7 days", level="DEBUG")
        logger.add(self.error_log_file, rotation="1 day", retention="7 days", level="ERROR")

        # Log into the default set of channels if not already:
        with open('./config/service.json', 'r') as f_obj:
            channels = json.load(f_obj)['channels']
        logger.info('Agent joining Service default channels (if not already joined). Will not join to any extra channels:', channels)
        join_tasks = [self.send_join_channel(channel_id) for channel_id in channels]
        await asyncio.wait(join_tasks)

    async def on_message_down(self, message_down: MessageBody):
        """Listen to messages the user sends and respond to them."""
        ch_id = message_down.channel_id
        content = message_down.content
        if not ch_id in self.channels:
            self.channels[ch_id] = MoobiusStorage(self.client_id, ch_id, db_config=self.db_config)       
            await self.send_fetch_userlist(ch_id)
            await self.send_fetch_buttons(ch_id)

        if message_down.context['sender'] == self.client_id:
            # avoid infinite loop
            return
        will_log_out = False
        if message_down.subtype == "text":
            if content['text'] == "nya":
                content['text'] = "meow"
                button_list = [{"button_id": "keyc", "button_name": "cat talk","button_text": "Meow/Nya", "new_window": False}]
                print('AGENT BUTTON UPDATE:', ch_id, [message_down.sender])
                await self.send_update_buttons(ch_id, button_list, [message_down.sender]) # TODO: can buttons be updated by agent?
            elif content['text'] == "meow":
                content['text'] = "nya"
            elif content['text'] == "log agent out":
                content['text'] = "Agent logging out. Will not be usable until restart."
                will_log_out = True
            elif content['text'] == "agent info":
                the_agent_id = self.client_id
                agent_info1 = await self.fetch_user_profile(the_agent_id) # Should be equal to self.agent_info
                content['text'] = f"Agent profile:\n{agent_info1}"
            elif content['text'].strip().startswith("rename agent"):
                new_name = content['text'].strip().replace("rename agent",'').strip()
                the_agent_id = self.client_id # Will not be needed for update_current_user in the .net version.
                logger.info('About to update the agent\'s name!')
                await self.update_current_user(avatar="null", description='Agent got an updated name!', name=new_name, user_id=the_agent_id)
                content['text'] = "renamed the agent (refresh)!"
            elif len(content['text']) > 160:
                content['text'] = f'Long message len={len(content["text"])}.'
            content['text'] = f"agent repeat: {content['text']}"

        message_down.timestamp = int(time.time() * 1000)
        recipients = [message_down.sender]
        message_down.recipients = recipients

        await self.send(payload_type='message_up', payload_body=message_down)
        if will_log_out: # After the message is sent.
            await self.sign_out()

    async def on_update_userlist(self, update):
        for user_id in update['userlist']:
            if type(user_id) is not str:
                raise Exception('The userlist update should be a list of user_ids not users.') # Extra assert just to be sure the update is the list of user ids.
            c_id = update['channel_id']
            while c_id not in self.channels:
                logger.info(f'Agent waiting (for on_start) while update userlist for channel: {c_id}')
                await asyncio.sleep(2)

            self.channels[c_id].characters[user_id] = await self.fetch_user_profile(user_id)

    async def on_update_buttons(self, update):
        logger.info("agent_update_buttons", update['buttons'])
        # update buttons [{'button_id': 'key1', 'button_name': 'name1', 'button_text': 'Meet Tubbs or Hermeowne', 'new_window': True, 'arguments': [{'name': 'arg1', 'type': 'enum', 'optional': False, 'values': ['Meet Tubbs', 'Meet Hermeowne'], 'placeholder': 'placeholder'}]}, {'button_id': 'key2', 'button_name': 'name2', 'button_text': 'Meet Ms Fortune', 'new_window': False, 'arguments': None}]
        self.channels[update['channel_id']].buttons = update['buttons']

    async def on_update_canvas(self, update):
        logger.info("agent_on_update_canvas", update)
        # agent_on_update_canvas {'subtype': 'update_canvas', 'channel_id': '32f38b98-2ac5-4ada-8945-52a845a0d574', 'content': {'path': 'https://social-public-bucket-1.s3.amazonaws.com/32947f5b-3951-43ad-8fc5-d7d898efc5ec.png', 'text': "I'm Tubbs on canvas!"}, 'group_id': 'temp', 'context': {}}

    async def on_fetch_channel_info(self, update):
        # TODO: not agent function?
        logger.info("agent_on_fetch_channel_info", update)

    async def on_button_click(self, button_click):
        logger.info("agent_on_button_click", button_click)

    async def on_spell(self, text):
        """The agent can be tested with spells which call the self.send_... functions."""
        # 7 Actions
        if text == "send_fetch_userlist":
            for channel_id in self.channels.keys():
                await self.send_fetch_userlist(channel_id)
        elif text == "send_fetch_buttons":
            for channel_id in self.channels.keys():
                await self.send_fetch_buttons(channel_id)
        # elif text == "send_fetch_style":
        #     for channel_id in self.channels.keys():
        #         await self.send_fetch_style(channel_id)
        elif text == "send_fetch_canvas":
            for channel_id in self.channels.keys():
                await self.send_fetch_canvas(channel_id)
        elif text == "send_join_channel":
            for channel_id in self.channels.keys():
                await self.send_join_channel(channel_id)
        elif text == "send_leave_channel":
            for channel_id in self.channels.keys():
                await self.send_leave_channel(channel_id)
        elif text == "send_fetch_channel_info":
            for channel_id in self.channels.keys():
                await self.send_fetch_channel_info(channel_id)
        elif text == "send_button_click_key1":
            for channel_id in self.channels.keys():
                for button in self.channels[channel_id].buttons:
                    if button['button_id'] == "key1":
                        await self.send_button_click(channel_id, "key1", [('arg1', "Meet Tubbs")])
        elif text == "send_button_click_key2":
            for channel_id in self.channels.keys():
                for button in self.channels[channel_id].buttons:
                    if button['button_id'] == "key2":
                        await self.send_button_click(channel_id, "key2", [])
        elif text == "nya_all":
            for channel_id in self.channels.keys():
                recipients = list(self.channels[channel_id].characters.keys())
                await self.create_message(channel_id, "nya nya nya", recipients)
