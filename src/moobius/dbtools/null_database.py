# null_database.py

from moobius.dbtools.database_interface import DatabaseInterface
from moobius.basic.logging_config import log_info, log_error
class NullDatabase(DatabaseInterface):
    def __init__(self, domain='', **kwargs):
        super().__init__(domain=domain, **kwargs)

    def get_value(self, key):
        log_info('NullDatabase: Loading key {k}'.format(k=key))
        return True, None

    def set_value(self, key, value):
        log_info('NullDatabase: Saving key {k} with value {v}'.format(k=key, v=value))
        return True, ""

    def delete_key(self, key):
        log_info('NullDatabase: Deleting key {k}'.format(k=key))
        return True, ""

    def all_keys(self):
        return []