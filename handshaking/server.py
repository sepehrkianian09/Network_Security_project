from key_holder import KeyHolder
from sockets.interfaces import Socket


class ServerHandShaker:
    def __init__(self, socket: "Socket", key_holder: KeyHolder) -> None:
        self.socket = socket
        self.__key_holder = key_holder

    def run_handshaking(self):
        pass
