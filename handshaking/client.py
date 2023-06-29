from key_holder import KeyHolder
from sockets.interfaces import DecoratorSocket, Socket


class HandShaker(DecoratorSocket):
    def __init__(self, socket: "Socket", key_holder: KeyHolder) -> None:
        super().__init__(socket)
        self.__key_holder = key_holder

    def start_handshaking(self):
        pass
