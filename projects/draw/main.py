from service import DrawService
from moobius import MoobiusWand

if __name__ == "__main__":
    wand = MoobiusWand()
    
    service_handle = wand.run(
        DrawService,
        log_file="logs/service.log",
        service_config_path="config/service.json",
        db_config_path="config/service_db.json",
        background=True
    )