from service import PuppetService
from bot import Bot
from moobius import MoobiusWand

if __name__ == "__main__":

    wand = MoobiusWand()

    handle = wand.run(PuppetService, config="config/config.json", background=True)

    agent_handle = wand.run(Bot, config="config/usermode_config.json", background=True)

