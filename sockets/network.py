import socket
from typing import Optional
from sockets.interfaces import Socket


class NetworkSocket(Socket):
    encode_format = "UTF-8"

    def __init__(self, __socket: Optional[socket.socket] = None) -> None:
        super().__init__()
        if __socket:
            self.__socket = __socket
        else:
            self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def send(self, message: str):
        self.__socket.sendall(message.encode(self.encode_format))

    def receive(self, __bufsize: int) -> str:
        return self.__socket.recv(__bufsize).decode(self.encode_format, "strict")

    def connect(self, HOST: str, PORT: int):
        self.__socket.connect((HOST, PORT))

    def bind(self, HOST: str, PORT: int):
        self.__socket.bind((HOST, PORT))

    def listen(self):
        self.__socket.listen()

    def accept(self):
        return self.__socket.accept()

    def __enter__(self):
        self.__socket.__enter__()
        return self

    def __exit__(self, *args):
        self.__socket.__exit__(self, args)
