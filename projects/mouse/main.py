from service import MouseService
from moobius.core.wand import MoobiusWand

if __name__ == "__main__":
    wand = MoobiusWand()
    handle = wand.run(MouseService, service_config_path="config/service.json", db_config_path="config/db.json", background=True)
