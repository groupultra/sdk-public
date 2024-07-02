import os
from service import DemoService
from agent import DemoAgent
from moobius import MoobiusWand
from loguru import logger

if __name__ == "__main__":

    wand = MoobiusWand()

    handle = wand.run(
        DemoService,
        log_file="logs/service.log",
        error_log_file="logs/error.log",
        terminal_log_level="INFO",
        config_path="config/service.json",
        db_config_path="config/db.json",
        is_agent=False, # It defaults to False anyway.
        background=True)

    do_agent = True
    if os.path.exists("./config/agent.json"):
        agent_handle = wand.run(
            DemoAgent,
            log_file="logs/agent.log",
            error_log_file="logs/agent_error.log",
            terminal_log_level="INFO",
            config_path="config/agent.json",
            db_config_path="config/agent_db.json",
            is_agent=True,
            background=True)
    else:
        logger.warning('No conig/agent.json, agent cannot run')
