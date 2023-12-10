import asyncio
import time

from service import NekoService
from moobius import MoobiusWand

if __name__ == "__main__":
    wand = MoobiusWand()
    
    handle = wand.run(
        NekoService,
        log_file="logs/service.log",
        service_config_path="config/service.json",
        db_config_path="config/db.json",
        background=True
    )


