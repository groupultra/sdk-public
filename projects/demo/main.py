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

    # ======================= Code below are only for test purposes! =========================
    # ======================= And a DEMO for wand spells =====================================
    
    @logger.catch
    def test_spell(word='SYNC', repeat=10, interval=1):
        for i in range(repeat):
            wand.spell(handle, (word, i + 1))
            time.sleep(interval)

    @logger.catch
    async def test_aspell(word='ASYNC', repeat=10, interval=1):
        for i in range(repeat):
            await wand.aspell(handle, (word, i + 1))
            await asyncio.sleep(interval)
     
    logger.info("Test will start in 5 seconds...")
    time.sleep(10)
    test_spell('SYNC TEST! ', 5, 1)           # Sync spell
    asyncio.run(test_aspell('ASYNC TEST! ', 5, 1))         # Async spell
    test_spell('BOMB' * 10000, 5, 2)    # Only the first BOMB (10000) will pass. Subsequent ones will cause the websocket to disconnect
    asyncio.run(test_aspell('SURVIVED! ', 5, 1))       # There is an automatic reconnection mechanism. This will still work
    logger.info('Test finished. If you see this, it means the service is still running.')
