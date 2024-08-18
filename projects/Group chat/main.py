from service import GroupService
from moobius import MoobiusWand

if __name__ == "__main__":

    wand = MoobiusWand()

    handle = wand.run(
        GroupService,
        service_config="config/service.json",
        db_config="config/db.json",
        log_config="config/log.json",
        account_config="config/account.json",
        background=True)

