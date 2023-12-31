# magical_storage.py

from loguru import logger
from moobius.database.null_database import NullDatabase
from moobius.database.json_database import JSONDatabase
from moobius.database.magical_storage import MagicalStorage


class MoobiusStorage(MagicalStorage):
    '''
    MoobiusStorage helps to use multiple databases using a single interface.
    Currently, it supports JSONDatabase and NullDatabase.
    
    To use this class, you need to specify the database config in the config file.
    
    The config file should be a list of dicts. The dict parameters are:
        implementation: str
            The type of the database.
        load: bool
            Whether to load the database when initializing the database.
        clear: bool
            Whether to clear the database when initializing the database.
        name: str
            The name of the json database.
        settings: dict
            root_dir: str
                The root directory of the all the json files.
    '''
    def __init__(self, service_id, band_id, db_config=()):
        '''
        Initialize a MoobiusStorage object.
        
        Parameters:
            service_id: str
                The id of the service.
            band_id: str
                The id of the band.
            db_config: list
                The config of the databases, should be a list of config dicts.
                
        Returns:
            None
        
        Example:
            >>> storage = MoobiusStorage(service_id='1', band_id='1', db_config=[{'implementation': 'json', 'load': True, 'clear': False, 'name': 'character', 'settings': {'root_dir': 'data'}}])
            >>> storage.get('character').set_value('1', {'name': 'Alice'})
        '''
        super().__init__()

        self.service_id = service_id
        self.band_id = band_id

        for config in db_config:
            self.add_container(**config)

    @logger.catch
    def add_container(self, implementation, settings, name, load=True, clear=False):
        '''
        Add a database using the config dict.
        
        Parameters:
            implementation: str
                The type of the database.
            settings: dict
                root_dir: str
                    The root directory of the all the json files.
            name: str
                The name of the json database.
            load: bool
                Whether to load the database when initializing the database.
            clear: bool
                Whether to clear the database when initializing the database.
        
        Returns:
            None

        Example:
            Note: This is a hidden function, you don't need to call it directly.
            >>> storage = MoobiusStorage(service_id='1', band_id='1')
            >>> storage.add_container(implementation='json', settings={'root_dir': 'data'}, name='character', load=True, clear=False)
        '''
        domain = f'service_{self.service_id}.band_{self.band_id}.{name}'

        if implementation == 'json':
            database_class = JSONDatabase
        else:
            logger.warning('Band: Unsupported database type. Using NullDatabase instead.')
            database_class = NullDatabase

        database = database_class(domain=domain, **settings)
        self.put(name, database=database, load=load, clear=clear)
