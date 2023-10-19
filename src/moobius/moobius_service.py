# moobius_service.py

from dacite import from_dict

from moobius.basic.types import Character
from moobius.moobius_basic_service import MoobiusBasicService

# with database
class MoobiusService(MoobiusBasicService):
    def __init__(self, db_settings=(), **config):
        super().__init__(**config)

        self.bands = {}
        self.db_settings = db_settings

