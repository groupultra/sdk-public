from moobius import Moobius

class PuppetService(Moobius):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._puppet = None

    async def _get_agent_id(self):
        if not self._puppet:
            self._puppet = (await self.create_agent("Bot", "https://www.moobius.net/images/index/6.jpeg", "A bot!")).character_id
        return self._puppet

    async def _update_char_list(self, action, all=False):
        ids = await self.fetch_member_ids(action.channel_id, False)+[await self._get_agent_id()]
        await self.send_characters(characters=ids, channel_id=action.channel_id, recipients=[ids] if all else [action.sender])

    async def on_refresh(self, action):
        await self.send_message('Try sending messages to the other characters in this chat!', action.channel_id, action.sender, [action.sender])
        await self._update_char_list(action, all=False)

    async def on_join_channel(self, action):
        await self._update_char_list(action, all=True)

    async def on_leave_channel(self, action):
        await self._update_char_list(action, all=True)

    async def on_message_up(self, message):
        agent_id = await self._get_agent_id()
        if agent_id in message.recipients:
            await self.send_message("I am a puppet! "+str(message.content), message.channel_id,
                                    sender=agent_id, recipients=[message.sender])
        await self.send_message(message)
