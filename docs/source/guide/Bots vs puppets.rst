.. _bot-puppet-tut:

Service-created puppets
================================================
Puppet characters are created and controlled by the service.
They appear just as any user would, and like real users can be sent messages.
However, all recieved messages go to the service and all messages they sent are sent from the service.

**A Pythonic usage pattern**:

First, initialize an empty puppet character id:

.. code-block:: Python

    self._puppet = None

Then provide a *getter* that makes a puppet the first time it is called, but then caches the result and returns it for subsequent calls.
This means only one puppet is created per startup which improves performnace.

.. code-block:: Python

    async def _get_puppet_id(self):
        if not self._puppet:
            self._puppet = (await self.create_puppet("Bot", "https://www.moobius.net/images/index/6.jpeg", "A bot!")).character_id
        return self._puppet

Use the puppet's id to send messages "from" them. This example has them "respond" to messages:

.. code-block:: Python

    async def on_message_up(self, message):
        puppet_id = await self._get_puppet_id()
        if puppet_id in message.recipients:
            await self.send_message("I am a puppet! "+str(message.content), message.channel_id,
                                    sender=puppet_id, recipients=[message.sender])
        await self.send_message(message)


Agents (bots)
==============================================
Agents, unlike puppets, are actual bots in that they can independently send and recieve messages.

Agents correspond to *real accounts* and are best used when *both humans and AI* need to control a character's behavior,
otherwise it is easier to use puppets.

They can request canvas, buttons, and other with `send_fetch_xyz`. This simulates the user's browser asking for the different widgets.
The agents will recieve an update which can be listened to with `on_update_xyz`.

To make an agent, first create a config/agent.json file with thier account credentials:
```
{
    "http_server_uri": "https://api.moobius.net/",
    "ws_server_uri": "wss://ws.moobius.net/",
    "email": "...@....com",
    "password": "*********"
}
```

Then create an agent.py file that, much like the service, extends the Moobius class. 

In this example it responds to messages.
Agents make use of "on_message_down" instead of "on_message_up" because they are listening to messages sent *down from* the service.

.. code-block:: Python
    from moobius import Moobius

    class BotAgent(Moobius):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)

        async def on_start(self): # Log in the agent using thier credentials.
            """Called after successful connection to Platform websocket and Agent login success."""
            await self.agent_join_service_channels('./config/service.json') # Log into the default set of channels if not already.

        async def on_message_down(self, the_message):
            await self.send_message('The agent got this message: '+str(the_message), the_message.channel_id, self.client_id, [the_message.sender])

A single modification to the wand.run function is needed, namely `is_agent=True`. Here is a typical agent launching code:

.. code-block:: Python

    agent_handle = wand.run(
        BotAgent,
        log_file="logs/service.log",
        error_log_file="logs/error.log",
        terminal_log_level="INFO",
        config_path="config/agent.json",
        db_config_path="config/agent_db.json",
        is_agent=True, # Set to True for agents.
        background=True)

If `background=True` this code will launch the agent on a seperate process and will not block.
This allows each agent, as well as the service itself, to have it's own process. This in some cases helps performance.

Demo code
================================
The demo code is available on

`the public repo <https://github.com/groupultra/sdk-public/tree/main/projects/Bot puppet>`.