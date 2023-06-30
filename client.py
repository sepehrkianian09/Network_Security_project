import threading
from typing import Tuple
from handshaking.client import ClientHandShaker
from key_holder import SecureKeyHolder
from sockets.interfaces import Socket
from sockets.network import NetworkSocket, create_socket
from sockets.secure import SecureSocket
from thread_pool import ThreadPool


class Client:
    def __init__(self, socket: "Socket") -> None:
        self.socket = socket
        self.sent_messages: str = ""

    def run(self):
        ThreadPool(
            threads=[
                threading.Thread(target=self.write_messages, args=()),
                threading.Thread(target=self.read_messages, args=()),
            ]
        ).run()
        print(f"sent_messages: {self.sent_messages}")

    def read_messages(self):
        while True:
            read_message = self.socket.receive(1024)
            # print(f"read Message: {read_message}")
            if read_message == "stop":
                break
            self.sent_messages += read_message

    def write_messages(self):
        while True:
            read_line = input()
            self.socket.send(read_line)
            if read_line == "stop":
                break


def main(args: Tuple[str, int]):
    HOST, PORT = args
    key_holder = SecureKeyHolder()
    socket = create_socket()
    with socket:
        socket.connect((HOST, PORT))
        networked_socket = NetworkSocket(socket)
        handshaker = ClientHandShaker(key_holder=key_holder, socket=networked_socket)
        handshaker.run_handshaking()
        concrete_socket = SecureSocket(key_holder=key_holder, socket=networked_socket)
        Client(socket=concrete_socket).run()


if __name__ == "__main__":
    main(("127.0.0.1", 65432))
