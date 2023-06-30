from key_holder import KeyHolder
from sockets.interfaces import DecoratorSocket, Socket

MESSAGE_TYPE = str


class SecureSocket(DecoratorSocket):
    def __init__(self, key_holder: KeyHolder, socket: "Socket") -> None:
        super().__init__(socket)
        self.__key_holder = key_holder

    def append_hash(self, message: MESSAGE_TYPE) -> MESSAGE_TYPE:
        return message + "2 "

    def check_hash(self, message: MESSAGE_TYPE):
        if message[-2:] != "2 ":
            raise Exception()
        return message[:-2]

    def encrypt(self, message: MESSAGE_TYPE) -> MESSAGE_TYPE:
        return message

    def decrypt(self, message: MESSAGE_TYPE) -> MESSAGE_TYPE:
        return message

    def send(self, message: MESSAGE_TYPE):
        message = self.append_hash(message)
        message = self.encrypt(message)
        super().send(message)

    def receive(self, message_size) -> MESSAGE_TYPE:
        message = super().receive(message_size=message_size)
        message = self.check_hash(message)
        message = self.decrypt(message)
        return message
