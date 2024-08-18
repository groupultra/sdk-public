import os
from service import DemoService
from agent import DemoAgent
from moobius import MoobiusWand
from loguru import logger

if __name__ == "__main__":

    wand = MoobiusWand()

    handle = wand.run(
        DemoService,
        service_config="config/service.json",
        db_config="config/db.json",
        log_config="config/log.json",
        account_config="config/account.json",
        background=True)
