import socket
from typing import Optional
from sockets.interfaces import Socket


def create_socket() -> socket.socket:
    return socket.socket()


class NetworkSocket(Socket):
    encode_format = "UTF-8"

    def __init__(self, __socket: Optional[socket.socket] = None) -> None:
        super().__init__()
        if __socket:
            self.__socket = __socket
        else:
            self.__socket = create_socket()
        self.__socket_closed__ = False

    def send(self, message: str):
        self.__socket.sendall(message.encode(self.encode_format))

    def receive(self, __bufsize: int) -> str:
        try:
            return self.__socket.recv(__bufsize).decode(self.encode_format, "strict")
        except:
            return ""

    @property
    def socket_closed(self):
        return self.__socket_closed__

    def __exit__(self):
        self.__socket_closed__ = True
        return self.__socket.__exit__()
