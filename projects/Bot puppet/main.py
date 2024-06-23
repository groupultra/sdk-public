from service import PuppetService
from agent import BotAgent
from moobius import MoobiusWand

if __name__ == "__main__":

    wand = MoobiusWand()

    handle = wand.run(
        PuppetService,
        config_path="config/service.json",
        db_config_path="config/db.json",
        is_agent=False,
        background=True)

    agent_handle = wand.run(
        BotAgent,
        log_file="logs/agent.log",
        error_log_file="logs/error.log",
        config_path="config/agent.json",
        db_config_path="config/agent_db.json",
        is_agent=True,
        background=True)
