from abc import ABC, abstractmethod


class DatabaseInterface(ABC):
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
        