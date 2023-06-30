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

    def send(self, message: str):
        self.__socket.sendall(message.encode(self.encode_format))

    def receive(self, __bufsize: int) -> str:
        try:
            return self.__socket.recv(__bufsize).decode(self.encode_format, "strict")
        except:
            return ""
