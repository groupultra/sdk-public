import os
from service import TemplateService
from moobius import MoobiusWand

if __name__ == "__main__":

    wand = MoobiusWand()

    handle = wand.run(
        TemplateService,
        config_path="config/service.json",
        db_config_path="config/db.json",
        is_agent=False, # It defaults to False anyway.
        background=True)

