from service import TranslateService
from moobius.core.wand import MoobiusWand

if __name__ == "__main__":
    wand = MoobiusWand()
    
    handle = wand.run(
        TranslateService,
        log_file="logs/service.log",
        service_config_path="config/service.json",
        db_config_path="config/db_settings.json",
        background=True
    )

