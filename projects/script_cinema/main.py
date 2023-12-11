from service import ScriptService
from moobius.core.wand import MoobiusWand

if __name__ == "__main__":
    wand = MoobiusWand()
    
    handle = wand.run(
        ScriptService,
        log_file="logs/service.log",
        service_config_path="config/script_config.json",
        db_config_path="config/script_db_settings.json",
        background=True
    )

