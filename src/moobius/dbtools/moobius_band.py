# moobius_band.py

from moobius.dbtools.null_database import NullDatabase
from moobius.dbtools.simple_json_database import SimpleJSONDatabase
from moobius.dbtools.magical_storage import MagicalStorage

class MoobiusBand(MagicalStorage):
    def __init__(self, service_id, band_id, db_settings=()):
        super().__init__()

        self.service_id = service_id
        self.band_id = band_id
 
        for settings in db_settings:
            self.add_container(**settings)


    def add_container(self, db_type, db_config, name, load=True, clear=False):
        domain = f'service_{self.service_id}.band_{self.band_id}.{name}'
        
        if db_type == 'json':
            database_class = SimpleJSONDatabase
        else:
            print('Band: Unsupported database type. Using NullDatabase instead.')
            database_class = NullDatabase

        database = database_class(domain=domain, **db_config)
        self.put(name, database=database, load=load, clear=clear)