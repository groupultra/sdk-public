from moobius import Moobius, MoobiusWand


class ZeroService(Moobius):
    pass


if __name__ == "__main__":
    MoobiusWand().run(ZeroService, config='config/config.json')