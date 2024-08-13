import os
from service import DemoService
from agent import DemoAgent
from moobius import MoobiusWand
from loguru import logger

if __name__ == "__main__":

    wand = MoobiusWand()

    handle = wand.run(
        DemoService,
        config_path="config/service.json",
        db_config_path="config/db.json",
        log_settings="config/log_settings.json",
        background=True)
