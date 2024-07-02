from service import ButtonService
from moobius import MoobiusWand

if __name__ == "__main__":

    wand = MoobiusWand()

    handle = wand.run(
        ButtonService,
        config_path="config/service.json",
        db_config_path="config/db.json",
        log_file="logs/service.log",
        error_log_file="logs/error.log",
        terminal_log_level="INFO",
        is_agent=False,
        background=True)

