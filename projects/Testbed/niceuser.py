# Users are bots attached to real user accounts.
# This is a different concept from puppet characters created by the service.


import sys, json, asyncio, time, pprint
import service

from dacite import from_dict
from loguru import logger
from moobius.types import MessageBody
from moobius import Moobius, MoobiusStorage, types


class TestbedUser(Moobius):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        logger.info("I speak 中国人, English, and many other languages because I know Unicode!")
        self.most_recent_updates = {} # Store the most recent updates to characters, canvas, etc. These can be queryed by sending a message to the user.

    async def on_start(self):
        """Called after successful connection to Platform websocket and User login success."""
        await self.user_join_service_channels() # Log into the default set of channels if not already.

    async def on_message_down(self, message_down: MessageBody):
        """Listen to messages the user sends and respond to them."""
        channel_id = message_down.channel_id
        content = message_down.content
        if not channel_id in self.channels or not self.channels[channel_id]:
            self.channels[channel_id] = MoobiusStorage(self.client_id, channel_id, db_config=self.config['db_config'])

        if message_down.sender == self.client_id:
            return # Avoid an infinite loop of responding to our messages.
        will_log_out = False
        if message_down.subtype == types.TEXT:
            text0 = content.text
            text1 = text0.strip().lower()
            if text1 == "nya":
                text2 = "meow"
                button_list = [{"button_id": "keyc", "button_name": "cat talk","button_name": "Meow/Nya", "new_window": False}]
                print('USER BUTTON UPDATE:', channel_id, [message_down.sender])
                await self.send_buttons(button_list, channel_id, [message_down.sender]) # TODO: can buttons be updated by the user?
            elif text1 == "meow":
                text2 = "nya"
            elif text1 == "log user out":
                text2 = "User logging out. Will not be usable until restart."
                will_log_out = True
            elif text1 == "user info":
                the_user_id = self.client_id
                user_info1 = await self.fetch_character_profile(the_user_id) # Should be equal to self.user_info
                text2 = f"User profile:\n{user_info1}"
            elif text1.startswith("rename user"):
                new_name = text1.replace("rename user",'').strip()
                the_user_id = self.client_id # Will not be needed for update_current_user in the .net version.
                logger.info('About to update the user\'s name!')
                await self.update_current_user(avatar="null", description='User got an updated name!', name=new_name)
                text2 = "renamed the user (refresh)!"
            elif text1 == 'channel groups' or text1 == 'channel_groups':
                glist_temp = await self.fetch_channel_temp_group(channel_id)
                glist = await self.fetch_channel_group_list(channel_id)
                gdict = await self.http_api.fetch_channel_group_dict(channel_id, self.client_id)
                text2A = types.limit_len(f"Channel group list (this time from the user):\n{pprint.pformat(glist)}", 4096)
                text2B = types.limit_len(f"Channel group TEMP list (this time from the user):\n{pprint.pformat(glist_temp)}", 4096)
                text2C = types.limit_len(f"Channel group, dict form from User (used internally):\n{pprint.pformat(gdict)}", 4096)
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
                    f'User info fetch fail: {e}'
            elif len(text0) > 160:
                text2 = f'Long message len={len(text0)}.'
            else:
                text2 = f"User repeat: {text0}"
            content.text = text2

        message_down.timestamp = int(time.time() * 1000)
        message_down.recipients = [message_down.sender]
        message_down.sender = self.client_id

        print('USER got a message. WILL SEND THIS MESSAGE (as message up); note conversion to/from recipient id vector:', message_down)
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
            while c_id not in self.channels:
                logger.info(f'User waiting (for on_start) while update characters for channel: {c_id}')
                await asyncio.sleep(2)

            self.channels[c_id].characters[character_id] = character_profile

    async def on_update_buttons(self, update):
        self.most_recent_updates['on_update_buttons'] = update
        self.channels[update.channel_id].buttons = [c.button for c in update.content]

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
        """The user can also be tested with spells which call the self.send_... functions."""
        if type(text) is not str:
            logger.warning('User spell got non-string text')
        if text == "refresh":
            for channel_id in self.channels.keys():
                await self.refresh_socket(channel_id)
        elif text == "send_button_click_key1":
            for channel_id in self.channels.keys():
                for button in self.channels[channel_id].buttons:
                    if button['button_id'] == "key1":
                        await self.send_button_click("key1", [('arg1', "Meet Tubbs")], channel_id)
        elif text == "send_button_click_key2":
            for channel_id in self.channels.keys():
                for button in self.channels[channel_id].buttons:
                    if button['button_id'] == "key2":
                        await self.send_button_click("key2", [], channel_id)
        elif text == "nya_all":
            for channel_id in self.channels.keys():
                recipients = list(self.channels[channel_id].characters.keys())
                await self.send_message("nya nya nya", channel_id, recipients)
