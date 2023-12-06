# magical_storage.py

from loguru import logger
from moobius.database.null_database import NullDatabase
from moobius.database.json_database import JSONDatabase
from moobius.database.magical_storage import MagicalStorage


class MoobiusStorage(MagicalStorage):
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
            database_class = JSONDatabase
        else:
            logger.warning('Band: Unsupported database type. Using NullDatabase instead.')
            database_class = NullDatabase

        database = database_class(domain=domain, **settings)
        self.put(name, database=database, load=load, clear=clear)
