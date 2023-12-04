import json
import asyncio
import time

from service import TestService
from moobius.moobius_wand import MoobiusWand

if __name__ == "__main__":
    wand = MoobiusWand()
    handle = wand.run(TestService, service_config_path="config/service.json", db_config_path="config/db.json", background=True)
    
    time.sleep(5)
    print("start sending")

    async def test_aspell():
        for i in range(10):
            await wand.aspell(handle, ('ASYNC', i))
            await asyncio.sleep(1)


    def test_spell():
        for i in range(10):
            wand.spell(handle, ('SYNC', i))
            time.sleep(1)

    def test_bomb():
        for i in range(10):
            wand.spell(handle, ('BOMB' * 10000, i)) # 40KB, MAX i = 3
            time.sleep(2)

    async def test_survive():
        for i in range(10):
            await wand.aspell(handle, ('SURVIVE', i))
            await asyncio.sleep(1)

    test_spell()
    asyncio.run(test_aspell())

    test_bomb()
    asyncio.run(test_survive())
    
    print('test finished')
