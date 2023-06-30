import socket
import threading
from typing import TYPE_CHECKING, Tuple
from handshaking.client import ClientHandShaker
from key_holder import SecureKeyHolder
from menu.login_register import LoginRegisterMenu
from sockets.interfaces import Socket
from sockets.network import NetworkSocket, create_socket
from sockets.secure import SecureSocket
from thread_pool import ThreadPool

if TYPE_CHECKING:
    from menu.interfaces import Menu


class Client:
    def __init__(self, login_socket: "Socket", other_socket: "Socket") -> None:
        self.socket = socket
        self.menu: "Menu" = LoginRegisterMenu(self)

    def run(self):
        while True:
            self.menu = self.menu.render()


key_holder = SecureKeyHolder()


def create_concrete_socket(socket: socket.socket) -> "Socket":
    networked_socket = NetworkSocket(socket)
    handshaker = ClientHandShaker(key_holder=key_holder, socket=networked_socket)
    handshaker.run_handshaking()
    concrete_socket = SecureSocket(key_holder=key_holder, socket=networked_socket)
    return concrete_socket


def main(host: str, login_port: int, other_port: int):
    login_socket = create_socket()
    login_socket.connect((host, login_port))
    other_socket = create_socket()
    other_socket.connect((host, other_port))
    with login_socket:
        with other_socket:
            login_concrete_socket = create_concrete_socket(login_socket)
            other_concrete_socket = create_concrete_socket(other_socket)
            Client(
                login_socket=login_concrete_socket, other_socket=other_concrete_socket
            ).run()


if __name__ == "__main__":
    main(host="127.0.0.1", login_port=65432, other_port=65433)
