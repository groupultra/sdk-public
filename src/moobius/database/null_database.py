# null_database.py

from .database_interface import DatabaseInterface
from loguru import logger


class NullDatabase(DatabaseInterface):
    """The NullDatabase is like /dev/null. Gets returns (True, None) and sets/deletes return (True, "")."""
    def __init__(self, domain='', **kwargs):
        super().__init__(domain=domain, **kwargs)

    def get_value(self, key):
        logger.info('NullDatabase: Loading key {k}'.format(k=key))
        return True, None

    def set_value(self, key, value):
        logger.info('NullDatabase: Saving key {k} with value {v}'.format(k=key, v=value))
        return True, ""

    def delete_key(self, key):
        logger.info('NullDatabase: Deleting key {k}'.format(k=key))
        return True, ""

    def all_keys(self):
        return []

    def __str__(self):
        return f'moobius.NullDatabase()'
    def __repr__(self):
        return self.__str__()
