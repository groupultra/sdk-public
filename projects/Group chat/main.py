from service import GroupService
from moobius import MoobiusWand

if __name__ == "__main__":

    wand = MoobiusWand()

    handle = wand.run(GroupService, config="config.json", background=True)

