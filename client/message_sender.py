from abc import ABC, abstractmethod

from client.key_holder import KeyHolder


class MessageSender(ABC):
    def __init__(self, socket) -> None:
        self.__socket = socket

    @abstractmethod
    def send_message(self, message):
        pass


class SecureMessageSender(MessageSender):
    def __init__(self, socket, key_holder: KeyHolder) -> None:
        super().__init__(socket)
        self.__key_holder = key_holder

    def send_message(self, message):
        pass
