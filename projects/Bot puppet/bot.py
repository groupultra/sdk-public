# Agents are bots attached to real user accounts.
from moobius import Moobius

class Bot(Moobius):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    async def on_start(self):
        """Called after successful connection to Platform websocket and Agent login success."""
        await self.agent_join_service_channels('./config/service.json') # Log into the default set of channels if not already.

    async def on_message_down(self, message):
        await self.send_message('The agent got this message: '+str(message), message.channel_id, self.client_id, [message.sender])
