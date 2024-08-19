import os
from service import TemplateService
from moobius import MoobiusWand

if __name__ == "__main__":

    wand = MoobiusWand()

    handle = wand.run(TemplateService, config="config.json", background=True)
