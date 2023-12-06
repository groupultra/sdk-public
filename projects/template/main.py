from service import TemplateService
from moobius import MoobiusWand

if __name__ == "__main__":
    wand = MoobiusWand()
    handle = wand.run(TemplateService, service_config_path="config/service.json", db_config_path="config/db.json", background=True)
