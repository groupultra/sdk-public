from service import DbExampleService
from moobius import MoobiusWand

if __name__ == "__main__":

    wand = MoobiusWand()

    handle = wand.run(DbExampleService, config="config.json", background=True)

