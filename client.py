import socket
import threading
from typing import TYPE_CHECKING, Optional, Tuple
from db_client.group_message import GroupMessage
from db_client.private_message import PrivateMessage
from handshaking.client import ClientHandShaker
from key_holder import SecureKeyHolder
from menu.login_register import LoginRegisterMenu
from sockets.interfaces import Socket
from sockets.message import MessageSocket
from sockets.network import NetworkSocket, create_socket
from sockets.secure import SecureSocket
from thread_pool import ThreadPool
from config import Config, main_config

if TYPE_CHECKING:
    from menu.interfaces import Menu


class ChatListener:
    def __init__(self, client: "Client"):
        self.client = client
        # if __is_chat_listening__: "chat_thread is running" else: "chat_thread is None"
        self.__is_chat_listening__ = False
        self.__chat_thread: Optional[threading.Thread] = None

    def toggle_chat_listening(self):
        if self.__is_chat_listening__:
            self.__end_chat_listening()
        else:
            self.__start_chat_listening()

    def __start_chat_listening(self):
        self.__is_chat_listening__ = True
        self.__chat_thread = threading.Thread(target=self.__listen_to_chats)
        self.__chat_thread.start()

    def __end_chat_listening(self):
        self.__is_chat_listening__ = False
        self.__chat_thread.join()
        self.__chat_thread = None

    def __listen_to_chats(self):
        while self.__is_chat_listening__:
            # listen to client message, and save
            pass


class Client:
    def __init__(self, login_socket: "Socket", other_socket: "Socket") -> None:
        self.login_socket = login_socket
        self.other_socket = other_socket
        self.chat_listener = ChatListener(self)
        self.menu: "Menu" = LoginRegisterMenu(self)

    def menu_transition(self, menu: "Menu"):
        self.menu = menu

    def toggle_chat_listening(self):
        self.chat_listener.toggle_chat_listening()

    def save_private_message(self, private_message: PrivateMessage):
        pass

    def save_group_message(self, group_message: GroupMessage):
        pass

    def run(self):
        while True:
            self.menu.render()


key_holder = SecureKeyHolder()


def create_concrete_socket(socket: socket.socket) -> "Socket":
    networked_socket = NetworkSocket(socket)
    handshaker = ClientHandShaker(key_holder=key_holder, socket=networked_socket)
    handshaker.run_handshaking()
    concrete_socket = SecureSocket(key_holder=key_holder, socket=networked_socket)
    # concrete_socket = MessageSocket(concrete_socket)
    return concrete_socket


def main(config: "Config"):
    login_socket = create_socket()
    login_socket.connect((config.host, config.login_port))
    print("client: sockets connected")
    with login_socket:
        other_socket = create_socket()
        other_socket.connect((config.host, config.other_port))
        with other_socket:
            login_concrete_socket = create_concrete_socket(login_socket)
            other_concrete_socket = create_concrete_socket(other_socket)
            Client(
                login_socket=login_concrete_socket, other_socket=other_concrete_socket
            ).run()


if __name__ == "__main__":
    main(config=main_config)
