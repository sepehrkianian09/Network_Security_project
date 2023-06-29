from abc import ABC, abstractmethod

from sockets.interfaces import DecoratorSocket, Sender


class MessageListener(ABC):
    @abstractmethod
    def listen(self, message):
        pass


class ConcurrentSocket(Sender):
    @abstractmethod
    def start_broadcasting_received_messages(self, listener: "MessageListener"):
        pass


class AsyncSocket(DecoratorSocket, ConcurrentSocket):
    def start_broadcasting_received_messages(self, listener: MessageListener):
        return super().start_broadcasting_received_messages(listener)
