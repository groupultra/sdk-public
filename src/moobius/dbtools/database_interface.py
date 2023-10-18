from abc import ABC, abstractmethod


class DatabaseInterface(ABC):
    @abstractmethod
    def __init__(self, domain='', **kwargs):
        """
        The concrete methods should expect a `domain` parameter as a `str`.
        It is used to separate different domains in the same database.
        Like different tables in the same database.
        Or different folders in the same file system.
        The keys inside different domains may overlap, but they are different entries.
        For example, two bands may have entries with the same feature id.
        domains are '.' seperated strings, like '<band_id>.<character_id>'
        """
        super().__init__()

    @abstractmethod
    def get_value(self, key) -> (bool, any):
        """
        Returns a tuple of (is_success, value)
        """
        pass

    @abstractmethod
    def set_value(self, key, value) -> (bool, any):
        """
        Returns a tuple of (is_success=True, key) or (is_success=False, err_msg)
        """
        pass

    @abstractmethod
    def delete_key(self, key) -> (bool, any):
        """
        Returns a tuple of (is_success=True, key) or (is_success=False, err_msg)
        """
        pass
    
    @abstractmethod
    def all_keys(self) -> any:
        """
        Returns an iteratable of all keys
        """
        pass
        