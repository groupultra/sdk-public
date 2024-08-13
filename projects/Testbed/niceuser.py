# Agents are bots attached to real user accounts.
# This is a different concept from puppet characters created by the service.


import sys, json, asyncio, time, pprint
import service

from dacite import from_dict
from loguru import logger
from moobius.types import MessageBody
from moobius import Moobius, MoobiusStorage, utils, types


class TestbedUser(Moobius):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        logger.info("I speak 中国人, English, and many other languages because I know Unicode!")
        self.most_recent_updates = {} # Store the most recent updates to characters, canvas, etc. These can be queryed by sending a message to the agent.

    async def on_start(self):
        """Called after successful connection to Platform websocket and Agent login success."""

        await self.agent_join_service_channels('./config/service.json') # Log into the default set of channels if not already

    async def on_message_down(self, message_down: MessageBody):
        """Listen to messages the user sends and respond to them."""
        channel_id = message_down.channel_id
        content = message_down.content
        if not channel_id in self.channel_storages:
            self.channel_storages[channel_id] = MoobiusStorage(self.client_id, channel_id, db_config=self.db_config)
            await self.send_fetch_characters(channel_id)
            await self.send_fetch_buttons(channel_id)

        if message_down.sender == self.client_id:
            return # Avoid an infinite loop of responding to our messages.
        will_log_out = False
        if message_down.subtype == types.TEXT:
            text0 = content.text
            text1 = text0.strip().lower()
            if text1 == "nya":
                text2 = "meow"
                button_list = [{"button_id": "keyc", "button_name": "cat talk","button_name": "Meow/Nya", "new_window": False}]
                print('AGENT BUTTON UPDATE:', channel_id, [message_down.sender])
                await self.send_buttons(button_list, channel_id, [message_down.sender]) # TODO: can buttons be updated by agent?
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
                text2A = self.limit_len(f"Channel group list (this time from the agent):\n{pprint.pformat(glist)}", 4096)
                text2B = self.limit_len(f"Channel group TEMP list (this time from the agent):\n{pprint.pformat(glist_temp)}", 4096)
                text2C = self.limit_len(f"Channel group, dict form from Agent (used internally):\n{pprint.pformat(gdict)}", 4096)
                text2 = '\n\n'.join([text2A,text2B,text2C])
            elif text1 == 'show_updates':
                update_lines = []
                for k, v in self.most_recent_updates.items():
                    update_lines.append(k+': '+str(v))
                show_JSON = False
                if show_JSON:
                    text2 = 'STR:\n'+'\n\n'.join(update_lines)+'\nJSON:\n'+utils.enhanced_json_save(None, self.most_recent_updates, indent=2)
                else:
                    text2 = '\n\n'.join(update_lines)
            elif text1 == 'user_info':
                try:
                    uinfo = await self.http_api.fetch_user_info()
                    text2 = str(uinfo)
                except Exception as e:
                    f'Agent info fetch fail: {e}'
            elif len(text0) > 160:
                text2 = f'Long message len={len(text0)}.'
            else:
                text2 = f"agent repeat: {text0}"
            content.text = text2

        message_down.timestamp = int(time.time() * 1000)
        message_down.recipients = [message_down.sender]
        message_down.sender = self.client_id

        print('AGENT got a message. WILL SEND THIS MESSAGE (as message up); note conversion to/from recipient id vector:', message_down)
        await self.send_message(message_down)
        if will_log_out: # Log out after the message is sent.
            await self.sign_out()

    #################### There are 5 on_update callbacks (not counting the generic on_update switchyard) ####################

    async def on_update_characters(self, update):
        self.most_recent_updates['on_update_characters'] = update # Store this every update.
        character_ids = [e.character.character_id for e in update.content]
        for character_id, character_profile in zip(character_ids, await self.fetch_character_profile(character_ids)):
            if not character_id:
                raise Exception('None character id.')
            if type(character_id) is not str:
                raise Exception('The characters in update should be a list of character ids.') # Extra assert just in case.
            c_id = update.channel_id
            while c_id not in self.channel_storages:
                logger.info(f'Agent waiting (for on_start) while update characters for channel: {c_id}')
                await asyncio.sleep(2)

            self.channel_storages[c_id].characters[character_id] = character_profile

    async def on_update_buttons(self, update):
        self.most_recent_updates['on_update_buttons'] = update
        self.channel_storages[update.channel_id].buttons = [c.button for c in update.content]

    async def on_update_canvas(self, update):
        self.most_recent_updates['on_update_canvas'] = update

    async def on_update_channel_info(self, update):
        self.most_recent_updates['on_update_channel_info'] = update

    async def on_update_canvas(self, update):
        self.most_recent_updates['on_update_canvas'] = update

    async def on_update_menu(self, update):
        self.most_recent_updates['on_update_menu'] = update

    ###########################################################################################################

    async def on_spell(self, text):
        """The agent can also be tested with spells which call the self.send_... functions."""
        if type(text) is not str:
            logger.warning('Agent spell got non-string text')
        if text == "refresh":
            for channel_id in self.channel_storages.keys():
                await self.refresh_socket(channel_id)
        elif text == "send_button_click_key1":
            for channel_id in self.channel_storages.keys():
                for button in self.channel_storages[channel_id].buttons:
                    if button['button_id'] == "key1":
                        await self.send_button_click("key1", [('arg1', "Meet Tubbs")], channel_id)
        elif text == "send_button_click_key2":
            for channel_id in self.channel_storages.keys():
                for button in self.channel_storages[channel_id].buttons:
                    if button['button_id'] == "key2":
                        await self.send_button_click("key2", [], channel_id)
        elif text == "nya_all":
            for channel_id in self.channel_storages.keys():
                recipients = list(self.channel_storages[channel_id].characters.keys())
                await self.send_message("nya nya nya", channel_id, recipients)
