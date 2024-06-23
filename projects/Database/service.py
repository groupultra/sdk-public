from moobius import Moobius, MoobiusStorage
from moobius.types import MessageBody

class DbExampleService(Moobius):
    def __init__(self, log_file="logs/service.log", error_log_file="logs/error.log", **kwargs):
        super().__init__(log_file=log_file, error_log_file=error_log_file, **kwargs)

        self.channels = {} # One MoobiusStorage object per channel.

    async def initialize_channel(self, channel_id):
        self.channels[channel_id] = MoobiusStorage(self.client_id, channel_id, self.db_config)

    async def on_fetch_canvas(self, action):
        await self.send_message('Try sending some messages!', action.channel_id, action.sender, [action.sender])

    async def on_message_up(self, the_message):
        c_id = the_message.channel_id; sender = the_message.sender

        default_stats = {'str':1, 'dex':1, 'int':1}
        stats = self.channels[c_id].stats.get(sender, default_stats)

        report = ''
        if the_message.subtype == 'text':
            txt = the_message.content.text.lower().strip()
            for k in default_stats.keys():
                if txt == k:
                    stats[k] += 1; report = f'{k.upper()} increased to {stats[k]}'
            if not report:
                report = f'Current stats: {stats}; type in one of these stats to boost it by one point..'
        else:
            report = 'Send text messages to boost your stats.'
        self.channels[c_id].stats[sender] = stats # Important! This reassign keeps it loaded.
        await self.send_message(report, c_id, sender, [sender])
