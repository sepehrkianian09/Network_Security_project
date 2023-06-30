from abc import ABC, abstractmethod, abstractproperty
from typing import Any


class Socket(ABC):
    @abstractmethod
    def send(self, message):
        pass

    @abstractmethod
    def receive(self, message_size: int) -> Any:
        pass

    @abstractmethod
    def __exit__(self):
        pass


class DecoratorSocket(Socket):
    def __init__(self, __socket: "Socket") -> None:
        super().__init__()
        self.__socket__ = __socket

    def send(self, message):
        return self.__socket__.send(message)

    def receive(self, message_size):
        return self.__socket__.receive(message_size)

    def __exit__(self):
        return self.__socket__.__exit__()
