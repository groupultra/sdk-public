from moobius import Moobius

class PuppetService(Moobius):
    def __init__(self, log_file="logs/service.log", error_log_file="logs/error.log", **kwargs):
        super().__init__(log_file=log_file, error_log_file=error_log_file, **kwargs)

        self._puppet = None

    async def _get_puppet_id(self):
        if not self._puppet:
            self._puppet = (await self.create_character("Bot", "https://www.moobius.net/images/index/6.jpeg", "A bot!")).character_id
        return self._puppet

    async def _update_char_list(self, action, all=False):
        ids = await self.fetch_real_character_ids(action.channel_id, False)+[await self._get_puppet_id()]
        await self.send_update_character_list(channel_id=action.channel_id, character_list=ids, recipients=[ids] if all else [action.sender])

    async def on_fetch_canvas(self, action):
        await self.send_message('Try sending messages to the other characters in this chat!', action.channel_id, action.sender, [action.sender])

    async def on_fetch_service_characters(self, action):
        await self._update_char_list(action, all=False)

    async def on_join_channel(self, action):
        await self._update_char_list(action, all=True)

    async def on_leave_channel(self, action):
        await self._update_char_list(action, all=True)

    async def on_message_up(self, message):
        puppet_id = await self._get_puppet_id()
        if puppet_id in message.recipients:
            await self.send_message("I am a puppet! "+str(message.content), message.channel_id,
                                    sender=puppet_id, recipients=[message.sender])
        await self.send_message(message)
