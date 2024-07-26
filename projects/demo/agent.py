# Agents are bots attached to real user accounts.

import sys, json, asyncio, time, pprint
import service

from dacite import from_dict
from loguru import logger
from moobius.types import MessageBody
from moobius import Moobius, MoobiusStorage, utils, types


class DemoAgent(Moobius):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        logger.info("I speak 中国人, English, and many other languages because I know Unicode!")

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
            elif text1 == "meow":
                text2 = "nya"
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
        self.channel_storages[update.channel_id].buttons = [c.button for c in update.content]

    async def on_update_canvas(self, update):
        pass

    async def on_update_channel_info(self, update):
        pass

    async def on_update_canvas(self, update):
        pass

    async def on_fetch_channel_info(self, update):
        pass

    async def on_update_context_menu(self, update):
        pass

    ###########################################################################################################

    async def on_spell(self, text):
        """Spells can be sent from the Wand from other processes."""
        if type(text) is not str:
            logger.warning('Agent spell got non-string text')
        if text == "nya_all":
            for channel_id in self.channel_storages.keys():
                recipients = list(self.channel_storages[channel_id].characters.keys())
                await self.send_message("nya nya nya", channel_id, recipients)
