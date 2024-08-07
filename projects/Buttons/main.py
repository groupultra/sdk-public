from service import ButtonService
from moobius import MoobiusWand

if __name__ == "__main__":

    wand = MoobiusWand()

    handle = wand.run(
        ButtonService,
        config_path="config/service.json",
        db_config_path="config/db.json",
        log_settings="config/logsettings.json",
        is_agent=False,
        background=True)

