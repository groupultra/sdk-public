.. _bot-puppet-tut:

puppet character puppets
================================================
puppet characters are controlled by the service.

A simple usage pattern:

Initialize and empty puppet character id:

.. code-block:: Python
    self._puppet = None

Provide a gettor that only makes a character once per app start:

.. code-block:: Python
    async def _get_puppet_id(self):
        if not self._puppet:
            self._puppet = (await self.create_puppet("Bot", "https://www.moobius.net/images/index/6.jpeg", "A bot!")).character_id
        return self._puppet

Use the puppet's id to send messages when certain events happen. This example has them to messages:

.. code-block:: Python
    async def on_message_up(self, message):
        puppet_id = await self._get_puppet_id()
        if puppet_id in message.recipients:
            await self.send_message("I am a puppet! "+str(message.content), message.channel_id,
                                    sender=puppet_id, recipients=[message.sender])
        await self.send_message(message)


Agents (bots)
==============================================
Agents are proper bots. They can be programmed to respond to anything a user would see. Usually this means messages, however they can also respond to changes to the canvas and buttons, etc.

Agents coorespond to *real accounts* and are best used when *both humans and AI* need to control a character's behavior.

First create a config/agent.json file with thier account credentials:
```
{
    "http_server_uri": "https://api.moobius.net/",
    "ws_server_uri": "wss://ws.moobius.net/",
    "email": "...@....com",
    "password": "*********"
}
```

Then create an agent.py file that, in this case, respondes to messages.

Note the use of "on_message_down" instead of "on_message_up"; it is responding to messages down from the service instead of up to the service:

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

Create an empty list config/agent_db.json file, this can be filled later if you need to use agent_dbs.

The main.py launches the service. Make it also launch the agent by adding this code:

.. code-block:: Python
    agent_handle = wand.run(
        BotAgent,
        log_file="logs/service.log",
        error_log_file="logs/error.log",
        terminal_log_level="INFO",
        config_path="config/agent.json",
        db_config_path="config/agent_db.json",
        is_agent=True,
        background=True)
