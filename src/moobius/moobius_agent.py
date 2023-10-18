from dacite import from_dict

from moobius.basic.types import Character
from moobius.moobius_basic_agent import MoobiusBasicAgent

# with database
class MoobiusAgent(MoobiusBasicAgent):
    def __init__(self, db_settings=(), **config):
        super().__init__(**config)

        self.bands = {}
        self.db_settings = db_settings

