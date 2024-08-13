from service import PuppetService
from bot import Bot
from moobius import MoobiusWand

if __name__ == "__main__":

    wand = MoobiusWand()

    handle = wand.run(
        PuppetService,
        config_path="config/service.json",
        db_config_path="config/db.json",
        log_settings="config/log_settings.json",
        background=True)

    agent_handle = wand.run(
        Bot,
        log_settings="config/log_settings.json",
        config_path="config/bot.json",
        db_config_path="config/bot_db.json",
        is_agent=True,
        background=True)
