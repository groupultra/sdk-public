from service import MenuCanvasService
from moobius import MoobiusWand

if __name__ == "__main__":

    wand = MoobiusWand()

    handle = wand.run(MenuCanvasService, config="config.json", background=True)
