from service import MahjongService
from moobius import MoobiusWand

if __name__ == "__main__":
    wand = MoobiusWand()
    handle = wand.run(MahjongService, service_config_path="config/service.json", db_config_path="config/db.json", background=True)

