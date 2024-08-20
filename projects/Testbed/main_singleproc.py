# Multithreaded instead of multiprocess.
import time
import asyncio
import sys

from service import TestbedService
from agent import TestbedAgent
from moobius import MoobiusWand
from threading import Thread

from loguru import logger

do_agent = True
multi_thread = True

if __name__ == "__main__":

    wand = MoobiusWand()

    service_kwargs = dict(
        config_path="config/service.json",
        db_config_path="config/db.json",
        log_file="logs/service.log",
        error_log_file="logs/error.log",
        terminal_log_level="INFO",
        is_agent=False, # It defaults to False anyway.
        background=False)
    if multi_thread:
        service_thread = Thread(target=wand.run,
                                args=[TestbedService],
                                kwargs=service_kwargs)
        service_thread.start()
    else:
        wand.run(TestbedService, **service_kwargs)

    agent_kwargs = dict(
        log_file="logs/agent.log",
        error_log_file="logs/error.log",
        config_path="config/agent.json",
        db_config_path="config/agent_db.json",
        is_agent=True,
        background=False)

    if do_agent:
        if multi_thread:
            agent_thread = Thread(target=wand.run,
                                args=[TestbedAgent],
                                kwargs=agent_kwargs)
            agent_thread.start()
        else:
            wand.run(TestbedAgent, **agent_kwargs)
    else:
        logger.warning('Agent has been DISABLED this run.')
