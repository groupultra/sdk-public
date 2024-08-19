from service import ButtonService
from moobius import MoobiusWand

if __name__ == "__main__":

    wand = MoobiusWand()

    handle = wand.run(ButtonService, config="config.json", background=True)

