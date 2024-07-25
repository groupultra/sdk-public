.. _group-chat-tut:

There are two ingrediants for setting up group chat: The user list and the messaging system.


The user list
===============================================

The users need to see who is in the chat. This is done with self.send_update_characters

It helps to make a function to update the user list:

.. code-block:: Python
    async def _update_char_list(self, action, all=False):
        ids = await self.fetch_member_ids(action.channel_id, False)
        await self.send_update_characters(channel_id=action.channel_id, character_ids=ids, recipients=[ids] if all else [action.sender])


Then it can be used whenever the user list needs to be updated. Which is in three cases (the fetch callback, and when someone else joins or leaves):

.. code-block:: Python
    async def on_fetch_characters(self, action):
        await self._update_char_list(action, all=False)

    async def on_join_channel(self, action):
        await self._update_char_list(action, all=True)

    async def on_leave_channel(self, action):
        await self._update_char_list(action, all=True)

The messing system
===============================================

Sending the user's message back out to the other users, unmodified, is very simple. This is because the send_message function is very polymorphic and messages have both sender and recipient information:

.. code-block:: Python
    async def on_message_up(self, the_message):
        await self.send_message(the_message)

However, this example is a bit more complex because it needs to compute who to send it to. Note that the send_message function in this case only changes the recipients:

.. code-block:: Python
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

Further considerations
===============================================

Group chat is a complex thing to implement because of human factors. So it will require systems to mute/unmute and ban/unban users,
as well as other mechanisms to prevent people from talking over eachother.

Thankfully, the fine-grained control Moobius has to offer can allow highly customized solutions.