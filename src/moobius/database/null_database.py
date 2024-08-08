# A 

from .database_interface import DatabaseInterface
from loguru import logger


class NullDatabase(DatabaseInterface):
    """The NullDatabase is like /dev/null; nothing is ever stored.
    Get returns (True, None) and set/delete return (True, "")."""
    def __init__(self, domain='', **kwargs):
        """Accepts the domain and optional kwargs."""
        super().__init__(domain=domain, **kwargs)

    def get_value(self, key):
        """Accepts the key. Returns (True, None)."""
        logger.info('NullDatabase: Loading key {k}'.format(k=key))
        return True, None

    def set_value(self, key, value):
        """Accepts the key and value. Returns (True, '')."""
        logger.info('NullDatabase: Saving key {k} with value {v}'.format(k=key, v=value))
        return True, ""

    def delete_key(self, key):
        """Accepts the key. Returns (True, '')."""
        logger.info('NullDatabase: Deleting key {k}'.format(k=key))
        return True, ""

    def all_keys(self):
        """Returns []."""
        return []

    def __str__(self):
        return f'moobius.NullDatabase()'
    def __repr__(self):
        return self.__str__()
