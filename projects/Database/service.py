from moobius import Moobius, MoobiusStorage, MoobiusWand
from moobius.types import MessageBody

class DbExampleService(Moobius):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    async def on_channel_init(self, channel_id):
        self.channel_storages[channel_id] = MoobiusStorage(self.client_id, channel_id, self.db_config)

    async def on_refresh(self, action):
        await self.send_message('Try sending some messages!', action.channel_id, action.sender, [action.sender])

    async def on_message_up(self, message):
        c_id = message.channel_id; sender = message.sender

        default_stats = {'str':1, 'dex':1, 'int':1}
        stats = self.channel_storages[c_id].stats.get(sender, default_stats)

        report = ''
        if message.subtype == 'text':
            txt = message.content.text.lower().strip()
            for k in default_stats.keys():
                if txt == k:
                    stats[k] += 1; report = f'{k.upper()} increased to {stats[k]}'
            if not report:
                report = f'Current stats: {stats}; type in one of these stats to boost it by one point..'
        else:
            report = 'Send text messages to boost your stats.'
        self.channel_storages[c_id].stats[sender] = stats # Important! This reassign keeps it loaded.
        await self.send_message(report, c_id, sender, [sender])

if __name__ == "__main__":
    MoobiusWand().run(DbExampleService, config='config/config.json')