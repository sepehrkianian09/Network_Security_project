from abc import ABC, abstractmethod


class KeyHolder(ABC):
    @abstractmethod
    def store_key(self, key_name, key):
        pass

    @abstractmethod
    def receive_key(self, key_name, key):
        pass


class SecureKeyHolder(KeyHolder):
    def store_key(self, key_name, key):
        pass

    def receive_key(self, key_name, key):
        pass
