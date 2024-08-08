.. _group-chat-tut:

###################################################################################
Group chat
###################################################################################

A group chat within which users can talk to each-other is at the core of most CCS apps.

There are two ingredients for setting up the chat: The user list and the messaging system.


The user list
===============================================

Your users need to see who is in the chat and be able to send them messages. This means that it is necessary to *query* and
*send out* the list of currently onlne members.

This example implementation first makes a function that queries and updates the list, either for just the user who reqested it or for all users:

.. code-block:: Python

    async def _update_char_list(self, action, all=False):
        ids = await self.fetch_member_ids(action.channel_id, False)
        await self.send_update_characters(character_ids=ids, channel_id=action.channel_id, recipients=[ids] if all else [action.sender])

There are three cases for which the user list needs to be sent out:
* A user joins.
* A user requests the list.
* a user leaves.

This example code handles all three cases:

.. code-block:: Python

    async def on_join_channel(self, action):
        await self._update_char_list(action, all=True)

    async def on_fetch_characters(self, action):
        await self._update_char_list(action, all=False)

    async def on_leave_channel(self, action):
        await self._update_char_list(action, all=True)

The messaging system
===============================================

When users send mesasges they are sent to the service, *not* to other users. The service must in turn send out messages, 
much like a mail carrier delivering mail.

Sending the user's message back out to the other users, unmodified, is very simple.

This is because the send_message function is very polymorphic and messages have both sender and recipient information:

.. code-block:: Python

    async def on_message_up(self, the_message):
        await self.send_message(the_message)

But more complex actions are available as well. For example, what about having a "vip" role that
can hear exclusive messages from other "vips" as well as a "quiet" role that does not hear anything?

This is how it can be implemented:

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

Group chat is very complex to implement because of human factors.

A fully-featured service will require systems to mute/unmute and ban/unban users,
as well as other mechanisms to prevent people from talking over each-other.

Thankfully, the fine-grained control allowed by Moobius allows for highly customized solutions.
