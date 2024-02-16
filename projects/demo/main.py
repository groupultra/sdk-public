# main.py
import time
import asyncio
import sys

from service import DemoService
from agent import DemoAgent
from moobius import MoobiusWand

from loguru import logger

if __name__ == "__main__":
    test_json_encode = False
    if test_json_encode:
        import json, dataclasses
        from moobius import types
        from moobius.utils import EnhancedJSONEncoder
        msg = types.MessageBody(subtype="A subtype", channel_id="e4-123", content={'a':1,'b':2}, timestamp=123,
                                recipients=['id_1', 'id_2'], sender='Sender_id 1234', message_id='<random id>', context={})
        msgj = json.dumps(msg, cls=EnhancedJSONEncoder)
        msg1 = json.loads(msgj)
        print('Object:', msg)
        print('Object dict:', dataclasses.asdict(msg))
        print('JSON:', msgj)
        print('Object1:', msg1)
        x = input('Simple test done, press enter to continue or q to quit.')
        if x and x.lower()=='q':
            quit()

    wand = MoobiusWand()

    handle = wand.run(
        DemoService,
        config_path="config/service.json",
        db_config_path="config/db.json",
        is_agent=False, # It defaults to False anyway.
        background=True
    )

    agent_handle = wand.run(
        DemoAgent,
        log_file="logs/agent.log",
        error_log_file="logs/error.log",
        config_path="config/agent.json",
        db_config_path="config/agent_db.json",
        is_agent=True,
        background=True)

    # service on_spell
    #wand.spell(handle, "meow")
    #wand.spell(handle, "nya")

    #asyncio.run(asyncio.sleep(3))
    # agent on_spell
    #wand.spell(agent_handle, "send_fetch_userlist")
    #wand.spell(agent_handle, "send_fetch_buttons")

    #wand.spell(agent_handle, "nya_all")

    #asyncio.run(asyncio.sleep(3))

    #wand.spell(agent_handle, "send_fetch_canvas")

    #wand.spell(agent_handle, "send_fetch_channel_info")
    #wand.spell(agent_handle, "send_button_click_key1")
    #wand.spell(agent_handle, "send_button_click_key2")

    #asyncio.run(asyncio.sleep(3))
    #wand.spell(agent_handle, "send_leave_channel")
    #asyncio.run(asyncio.sleep(3))

    #wand.spell(agent_handle, "send_join_channel")

    # ======================= Code below are only for test purposes! =========================
    # ======================= And a DEMO for wand spells =====================================
    # use `python main.py test` to run the test
    # use `python main.py` to run the service without test


    def test_spell(word='SYNC', repeat=10, interval=1):
        for i in range(repeat):
            wand.spell(handle, (word, i + 1))
            time.sleep(interval)


    async def test_aspell(word='ASYNC', repeat=10, interval=1):
        for i in range(repeat):
            await wand.aspell(handle, (word, i + 1))
            await asyncio.sleep(interval)


    if len(sys.argv) >= 2 and sys.argv[1] == 'test':
        logger.info("Test will start in 10 seconds...")
        time.sleep(10)
        test_spell('SYNC TEST! ', 5, 1)           # Sync spell
        asyncio.run(test_aspell('ASYNC TEST! ', 5, 1))         # Async spell
        test_spell('BOMB' * 10000, 5, 2)    # Only the first BOMB (10000) will pass. Subsequent ones will cause the websocket to disconnect
        asyncio.run(test_aspell('SURVIVED! ', 5, 1))       # There is an automatic reconnection mechanism. This will still work
        logger.info('Test finished. If you see this, it means the service is still running.')
    else:
        logger.info("Demo service started.")
