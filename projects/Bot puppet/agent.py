# Agents are bots attached to real user accounts.
from moobius import Moobius

class BotAgent(Moobius):
    def __init__(self, log_file="logs/agent.log", error_log_file="logs/error.log", **kwargs):
        super().__init__(**kwargs)

    async def on_start(self):
        """Called after successful connection to Platform websocket and Agent login success."""
        await self.agent_join_service_channels('./config/service.json') # Log into the default set of channels if not already.

    async def on_message_down(self, the_message):
        await self.send_message('The agent got this message: '+str(the_message), the_message.channel_id, self.client_id, [the_message.sender])
