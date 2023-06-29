import socket
from sockets.interfaces import Socket


class NetworkSocket(Socket):
    def __init__(self, HOST: str, PORT: int) -> None:
        super().__init__()
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = HOST
        self.port = PORT

    def send(self, __data: bytes):
        self.__socket.sendall(__data)

    def receive(self, __bufsize: int):
        self.__socket.recv(__bufsize)

    def __enter__(self):
        self.__socket.__enter__()

    def __exit__(self, *args):
        self.__socket.__exit__(self, args)