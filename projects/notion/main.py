# main.py
import time
import asyncio

from service import DemoService
from moobius import MoobiusWand

from loguru import logger

if __name__ == "__main__":
    wand = MoobiusWand()
    
    handle = wand.run(
        DemoService,
        service_config_path="config/service.json",
        db_config_path="config/db.json",
        background=True
    )