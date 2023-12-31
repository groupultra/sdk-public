import asyncio
import time

from agent import SummaryAgent
from moobius import MoobiusWand

if __name__ == "__main__":
    wand = MoobiusWand()
    
    agent_handle = wand.run(
        SummaryAgent,
        log_file="logs/agent.log",
        error_log_file="logs/error.log",
        agent_config_path="config/agent.json",
        db_config_path="config/agent_db.json",
        background=True)
    