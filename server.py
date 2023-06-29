import socket
import threading
from typing import Tuple
from handshaking.server import ServerHandShaker
from key_holder import SecureKeyHolder
from sockets.interfaces import Socket
from sockets.network import NetworkSocket, create_socket
from sockets.secure import SecureSocket


class Server:
    def __init__(self, socket: "Socket") -> None:
        self.socket = socket

    def run(self):
        while True:
            received_message = self.socket.receive(1024)
            if received_message:
                self.socket.send(received_message)
            if received_message == "stop":
                break
            else:
                print(f"received message {received_message}")


key_holder = SecureKeyHolder()


def handle_client(client_socket: socket.socket):
    with client_socket:
        networked_socket = NetworkSocket(client_socket)
        handshaker = ServerHandShaker(socket=networked_socket, key_holder=key_holder)
        handshaker.run_handshaking()
        concrete_socket = SecureSocket(key_holder=key_holder, socket=networked_socket)
        Server(concrete_socket).run()


def main(args: Tuple[str, int]):
    HOST, PORT = args
    with create_socket() as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen()
        while True:
            client_socket, address = server_socket.accept()
            threading.Thread(target=handle_client, args=[client_socket]).start()


if __name__ == "__main__":
    main(("127.0.0.1", 65432))
