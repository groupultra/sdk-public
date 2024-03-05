# Defines class NekoAgent(MoobiusAgent).

import json, asyncio, time, pprint
import service

from dacite import from_dict
from loguru import logger
from moobius.types import MessageBody, Character
from moobius import Moobius, MoobiusStorage


class DemoAgent(Moobius):
    def __init__(self, log_file="logs/agent.log", error_log_file="logs/error.log", **kwargs):
        super().__init__(**kwargs)
        self.log_file = log_file
        self.error_log_file = error_log_file

    # todo: channels and channel_ids, unbind_first, write back channels
    async def on_start(self):
        """Called after successful connection to websocket server and agent login success. Launches join tasks."""
        logger.add(self.log_file, rotation="1 day", retention="7 days", level="DEBUG")
        logger.add(self.error_log_file, rotation="1 day", retention="7 days", level="ERROR")

        await self.agent_join_service_channels('./config/service.json') # Log into the default set of channels if not already:

    async def on_message_down(self, message_down: MessageBody):
        """Listen to messages the user sends and respond to them."""
        print('AGENT GOT THIS MESSAGE:', message_down)
        channel_id = message_down.channel_id
        content = message_down.content
        if not channel_id in self.channels:
            self.channels[channel_id] = MoobiusStorage(self.client_id, channel_id, db_config=self.db_config)
            #await self.send_fetch_characters(channel_id) # Deprecated function?
            await self.send_fetch_buttons(channel_id)

        if message_down.sender == self.client_id:
            # avoid infinite loop
            return
        will_log_out = False
        if message_down.subtype == "text":
            text0 = content['text']
            text1 = text0.strip().lower()
            if text1 == "nya":
                text2 = "meow"
                button_list = [{"button_id": "keyc", "button_name": "cat talk","button_text": "Meow/Nya", "new_window": False}]
                print('AGENT BUTTON UPDATE:', channel_id, [message_down.sender])
                await self.send_update_buttons(channel_id, button_list, [message_down.sender]) # TODO: can buttons be updated by agent?
            elif text1 == "meow":
                text2 = "nya"
            elif text1 == "log agent out":
                text2 = "Agent logging out. Will not be usable until restart."
                will_log_out = True
            elif text1 == "agent info":
                the_agent_id = self.client_id
                agent_info1 = await self.fetch_character_profile(the_agent_id) # Should be equal to self.agent_info
                text2 = f"Agent profile:\n{agent_info1}"
            elif text1.startswith("rename agent"):
                new_name = text1.replace("rename agent",'').strip()
                the_agent_id = self.client_id # Will not be needed for update_current_user in the .net version.
                logger.info('About to update the agent\'s name!')
                await self.update_current_user(avatar="null", description='Agent got an updated name!', name=new_name)
                text2 = "renamed the agent (refresh)!"
            elif text1 == 'channel groups' or text1 == 'channel_groups':
                glist_temp = await self.fetch_channel_temp_group(channel_id)
                glist = await self.fetch_channel_group_list(channel_id)
                gdict = await self.http_api.fetch_channel_group_dict(channel_id, self.client_id)
                text2A = service.limit_len(f"Channel group list (this time from the agent):\n{pprint.pformat(glist)}")
                text2B = service.limit_len(f"Channel group TEMP list (this time from the agent):\n{pprint.pformat(glist_temp)}")
                text2C = service.limit_len(f"Channel group, dict form from Agent (used internally):\n{pprint.pformat(gdict)}")
                text2 = '\n\n'.join([text2A,text2B,text2C])
            elif len(text0) > 160:
                text2 = f'Long message len={len(text0)}.'
            else:
                text2 = f"agent repeat: {text0}"
            content['text'] = text2

        message_down.timestamp = int(time.time() * 1000)
        message_down.recipients = [message_down.sender]
        message_down.sender = self.client_id
        try:
            uinfo = await self.http_api.fetch_user_info()
            print('AGENT INFO:', uinfo)
        except Exception as e:
            print('Agent info fetch fail:', e)
        print('AGENT WILL SEND THIS MESSAGE (as message up); note conversion to/from recipient id vector:', message_down)
        await self.convert_and_send_message(message_down)
        if will_log_out: # After the message is sent.
            await self.sign_out()

    async def on_update_characters(self, update):
        for character_id in update['content']['characters']:
            if type(character_id) is not str or type(update['content']['characters']) is not list:
                raise Exception('The characters in update should be a list of character ids not dicts.') # Extra assert just to be sure the update is the list of user ids.
            c_id = update['channel_id']
            while c_id not in self.channels:
                logger.info(f'Agent waiting (for on_start) while update characters for channel: {c_id}')
                await asyncio.sleep(2)

            self.channels[c_id].characters[character_id] = await self.fetch_character_profile(character_id)

    async def on_update_buttons(self, update):
        logger.info("agent_update_buttons", update['content'])
        # update buttons [{'button_id': 'key1', 'button_name': 'name1', 'button_text': 'Meet Tubbs or Hermeowne', 'new_window': True, 'arguments': [{'name': 'arg1', 'type': 'enum', 'optional': False, 'values': ['Meet Tubbs', 'Meet Hermeowne'], 'placeholder': 'placeholder'}]}, {'button_id': 'key2', 'button_name': 'name2', 'button_text': 'Meet Ms Fortune', 'new_window': False, 'arguments': None}]
        self.channels[update['channel_id']].buttons = update['content']

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
        if text == "send_fetch_characters":
            for channel_id in self.channels.keys():
                await self.send_fetch_characters(channel_id)
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
