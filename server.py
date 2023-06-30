import socket
import threading
from typing import Callable, Tuple
from handshaking.server import ServerHandShaker
from key_holder import SecureKeyHolder
from server.login_handler import LoginHandler
from server.other_handler import OtherHandler
from sockets.interfaces import Socket
from sockets.network import NetworkSocket, create_socket
from sockets.secure import SecureSocket
from thread_pool import ThreadPool

key_holder = SecureKeyHolder()


def handle_login_request(client_socket: socket.socket):
    networked_socket = NetworkSocket(client_socket)
    handshaker = ServerHandShaker(socket=networked_socket, key_holder=key_holder)
    handshaker.run_handshaking()
    concrete_socket = SecureSocket(key_holder=key_holder, socket=networked_socket)
    LoginHandler(concrete_socket).run()


def handle_other_request(client_socket: socket.socket):
    with client_socket:
        networked_socket = NetworkSocket(client_socket)
        handshaker = ServerHandShaker(socket=networked_socket, key_holder=key_holder)
        handshaker.run_handshaking()
        concrete_socket = SecureSocket(key_holder=key_holder, socket=networked_socket)
        OtherHandler(concrete_socket).run()


def start_handling(host: str, port: int, handler: Callable[[socket.socket], None]):
    with create_socket() as server_socket:
        server_socket.bind((host, port))
        server_socket.listen()
        while True:
            client_socket, address = server_socket.accept()
            threading.Thread(target=handler, args=[client_socket]).start()


def main(host: str, login_port: int, other_port: int):
    ThreadPool(
        threads=[
            threading.Thread(
                target=start_handling, args=[host, login_port, handle_login_request]
            ),
            threading.Thread(
                target=start_handling, args=[host, other_port, handle_other_request]
            ),
        ]
    ).run()


if __name__ == "__main__":
    main(host="127.0.0.1", login_port=65432, other_port=65433)
