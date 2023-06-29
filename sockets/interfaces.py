from abc import ABC, abstractmethod, abstractproperty


class Sender(ABC):
    @abstractmethod
    def send(self, message):
        pass


class Socket(Sender):
    @abstractmethod
    def receive(self, message_size):
        pass


class DecoratorSocket(Socket):
    def __init__(self, __socket: "Socket") -> None:
        super().__init__()
        self.__socket = __socket

    def send(self, message):
        return self.__socket.send(message)

    def receive(self, message_size):
        return self.__socket.receive(message_size)


class MessageListener(ABC):
    @abstractmethod
    def listen(self, message):
        pass


class ConcurrentSocket(Sender):
    @abstractmethod
    def start_broadcasting_received_messages(self, listener: "MessageListener"):
        pass
