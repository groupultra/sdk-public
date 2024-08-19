from service import ZeroService
from moobius import MoobiusWand

if __name__ == "__main__":

    wand = MoobiusWand()
    handle = wand.run(ZeroService, config="config.json", background=True)


