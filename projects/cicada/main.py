from service import CicadaService
from moobius import MoobiusWand

if __name__ == '__main__':
    wand = MoobiusWand()

    handle = wand.run(
        CicadaService,
        service_config_path="config/service.json",
        db_config_path="config/db.json",
        background=True
    )
