# main.py
import time
import asyncio
import sys

from service import DemoService
from agent import DemoAgent
from moobius import MoobiusWand, utils

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
        background=True)

    do_agent = True
    if do_agent:
        agent_handle = wand.run(
            DemoAgent,
            log_file="logs/agent.log",
            error_log_file="logs/error.log",
            config_path="config/agent.json",
            db_config_path="config/agent_db.json",
            is_agent=True,
            background=True)

    else:
        agent_handle = None
        logger.warning('Agent has been DISABLED this run (debugging).')

    do_simple_spells = True
    if do_simple_spells:
        for i in range(8):
            time.sleep(8)
            wand.spell(handle, [f'Simple spell {i} of 8 ', i]) # The Service expects spells to be (string, times) spells.

    ################# Testing code below: `python main.py test` to run these tests ###############

    if len(sys.argv) >= 2 and sys.argv[1].lower().strip() in ['test', '-test', '--test']:
        logger.info("Test will start in 48 seconds...")
        time.sleep(48)
        wand.spell(handle, ['SYNC SPELL!', 1])
        asyncio.run(wand.aspell(handle,['ASYNC SPELL!', 1])) # Both Sync and Async spells should be supported.
        wand.spell(handle,['OVERFLOW' * 10000, 1]) # Only the first BOMB (10000) will pass. Subsequent ones will cause the websocket to disconnect. This message will NOT go through.
        asyncio.run(wand.aspell(handle,['SURVIVED!', 1])) # There is an automatic reconnection mechanism. This will still work

        if agent_handle:
            wand.spell(agent_handle, "meow")
            wand.spell(agent_handle, "nya")
            wand.spell(agent_handle, "send_fetch_characters") # Agent spells expect a single string.
            wand.spell(agent_handle, "send_fetch_buttons")
            wand.spell(agent_handle, "nya_all")
            wand.spell(agent_handle, "send_fetch_canvas")
            wand.spell(agent_handle, "send_fetch_channel_info")
            wand.spell(agent_handle, "send_button_click_key1")
            wand.spell(agent_handle, "send_button_click_key2")
            wand.spell(agent_handle, "send_leave_channel")
            wand.spell(agent_handle, "send_join_channel")

        logger.info('Test finished. If you see this, it means the service is still running.')
    else:
        logger.info("Demo service started.")
