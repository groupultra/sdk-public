from service import DbExampleService
from moobius import MoobiusWand

if __name__ == "__main__":

    wand = MoobiusWand()

    handle = wand.run(
        DbExampleService,
        config_path="config/service.json",
        db_config_path="config/db.json",
        is_agent=False,
        background=True)
