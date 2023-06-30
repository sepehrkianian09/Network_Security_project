from abc import ABC, abstractmethod, abstractproperty


class Socket(ABC):
    @abstractmethod
    def send(self, message):
        pass

    @abstractmethod
    def receive(self, message_size: int) -> str:
        pass


class DecoratorSocket(Socket):
    def __init__(self, __socket: "Socket") -> None:
        super().__init__()
        self.__socket = __socket

    def send(self, message):
        return self.__socket.send(message)

    def receive(self, message_size):
        return self.__socket.receive(message_size)
