from moobius import Moobius
from moobius.types import Button, ButtonClick

class GroupService(Moobius):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.roles = {}

    async def on_fetch_buttons(self, action):
        ids = ['default', 'quiet', 'vip']
        names = ['Default mode', 'Hear nothing mode', 'VIP mode']
        buttons = [Button(button_id=ids[i], button_name=names[i], new_window=False) for i in range(len(ids))]
        await self.send_update_buttons(action.channel_id, buttons, [action.sender])

    async def on_button_click(self, button_click: ButtonClick):
        channel_id = button_click.channel_id
        sender = button_click.sender
        self.roles[channel_id] = self.roles.get(channel_id, {})
        self.roles[channel_id][button_click.sender] = button_click.button_id
        await self.send_message('Your role set to: '+button_click.button_id, channel_id, sender, [sender])

    async def _update_char_list(self, action, all=False):
        ids = await self.fetch_member_ids(action.channel_id, False)
        await self.send_update_characters(channel_id=action.channel_id, character_ids=ids, recipients=[ids] if all else [action.sender])

    async def on_fetch_characters(self, action):
        await self._update_char_list(action, all=False)

    async def on_join_channel(self, action):
        await self._update_char_list(action, all=True)

    async def on_leave_channel(self, action):
        await self._update_char_list(action, all=True)

    async def on_message_up(self, the_message):
        to_whom = the_message.recipients
        roles = self.roles.get(the_message.channel_id, {})
        sender_role = roles.get(the_message.sender, 'default')
        recip_roles = [roles.get(the_id, 'default') for the_id in to_whom]

        if sender_role == 'vip':
            filtered_recips = [to_whom[i] for i in list(filter(lambda i: recip_roles[i]=='vip', range(len(to_whom))))]
        else:
            filtered_recips = [to_whom[i] for i in list(filter(lambda i: recip_roles[i] != 'quiet', range(len(to_whom))))]
        await self.send_message(the_message, recipients=filtered_recips)
