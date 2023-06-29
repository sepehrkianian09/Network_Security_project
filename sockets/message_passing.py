from key_holder import KeyHolder
from sockets.interfaces import ConcurrentSocket, DecoratorSocket, MessageListener, Socket

MESSAGE_TYPE = str


class MessagePassingSocket(DecoratorSocket, Socket):
    def __init__(self, key_holder: KeyHolder, socket: "Socket") -> None:
        super().__init__(socket)
        self.__key_holder = key_holder

    def append_hash(self, message: MESSAGE_TYPE) -> MESSAGE_TYPE:
        return ""

    def encrypt(self, message: MESSAGE_TYPE) -> MESSAGE_TYPE:
        return ""

    def send(self, message: MESSAGE_TYPE):
        message = self.append_hash(message)
        message = self.encrypt(message)
        self.__socket.send(message.encode("UTF-8"))

    def receive(self, message_size):
        pass
