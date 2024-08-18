from service import PuppetService
from bot import Bot
from moobius import MoobiusWand

if __name__ == "__main__":

    wand = MoobiusWand()

    handle = wand.run(
        PuppetService,
        service_config="config/service.json",
        db_config="config/db.json",
        log_config="config/log.json",
        account_config="config/account.json",
        background=True)

    agent_handle = wand.run(
        Bot,
        service_config="config/usermode_service.json",
        db_config="config/usermode_db.json",
        log_config="config/usermode_log.json",
        account_config="config/usermode_account.json",
        background=True)
