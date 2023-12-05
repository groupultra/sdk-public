import json
import asyncio
import time

from service import TestService
from moobius.moobius_wand import MoobiusWand
from loguru import logger

@logger.catch
def full_test(wand, handle):
    test_spell(wand, handle)
    asyncio.run(test_aspell(wand, handle))

    test_bomb(wand, handle)
    asyncio.run(test_survive(wand, handle))


async def test_aspell(wand, handle):
    for i in range(10):
        await wand.aspell(handle, ('ASYNC', i))
        await asyncio.sleep(1)


def test_spell(wand, handle):
    for i in range(10):
        wand.spell(handle, ('SYNC', i))
        time.sleep(1)


def test_bomb(wand, handle):
    for i in range(5):
        wand.spell(handle, ('BOMB' * 10000, i)) # 40KB, MAX i = 3
        time.sleep(2)


async def test_survive(wand, handle):
    for i in range(10):
        await wand.aspell(handle, ('SURVIVE', i))
        await asyncio.sleep(1)


if __name__ == "__main__":
    wand = MoobiusWand()
    
    handle = wand.run(
        TestService,
        log_file="logs/service.log",
        service_config_path="config/service.json",
        db_config_path="config/db.json",
        background=True
    )

    # ======================= Code below are only for test purposes! =========================
    logger.debug("Test will start in 5 seconds...")
    time.sleep(5)
    full_test(wand, handle)
    logger.debug('Test finished')
