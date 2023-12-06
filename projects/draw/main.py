import json
import asyncio
import time

from service import DrawService
from moobius.moobius_wand import MoobiusWand

if __name__ == "__main__":
    wand = MoobiusWand()
    handle = wand.run(DrawService, service_config_path="config/service.json", db_config_path="config/db.json", background=True)
