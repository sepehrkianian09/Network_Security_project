from abc import ABC, abstractmethod

from client.key_holder import KeyHolder


class MessageListener(ABC):
    @abstractmethod
    def listen(self, message):
        pass


class MessageReceiver(ABC):
    def __init__(self, socket) -> None:
        self.__socket = socket

    @abstractmethod
    def start_broadcasting_received_messages(self, listener: "MessageListener"):
        pass


class SecureMessageReceiver(MessageReceiver):
    def __init__(self, socket, key_holder: KeyHolder) -> None:
        super().__init__(socket)
        self.__key_holder = key_holder

    def start_broadcasting_received_messages(self, listener: "MessageListener"):
        pass
