# moobius_band.py

from moobius.dbtools.null_database import NullDatabase
from moobius.dbtools.simple_json_database import SimpleJSONDatabase
from moobius.dbtools.magical_storage import MagicalStorage
from loguru import logger

class MoobiusBand(MagicalStorage):
    def __init__(self, service_id, band_id, db_config=()):
        super().__init__()

        self.service_id = service_id
        self.band_id = band_id
 
        for config in db_config:
            self.add_container(**config)

    @logger.catch
    def add_container(self, implementation, settings, name, load=True, clear=False):
        domain = f'service_{self.service_id}.band_{self.band_id}.{name}'
        
        if implementation == 'json':
            database_class = SimpleJSONDatabase
        else:
            logger.warning('Band: Unsupported database type. Using NullDatabase instead.')
            database_class = NullDatabase

        database = database_class(domain=domain, **settings)
        self.put(name, database=database, load=load, clear=clear)