import socket
import threading
from typing import TYPE_CHECKING, Optional, Tuple
from db_client.message import PrivateMessage, GroupMessage
from handshaking.client import ClientHandShaker
from key_holder import SecureKeyHolder
from menu.login_register import LoginRegisterMenu
from messaging import Request, RequestType, Response
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
            request: "Request" = Request.schema().loads(
                self.client.login_socket.receive(1024)
            )
            if request.type == RequestType.send_private_message:
                self.client.save_private_message(
                    PrivateMessage(
                        content=request.data["content"],
                        sender=request.data["sender"],
                        time=request.data["time"],
                    )
                )
                self.client.login_socket.send(Response().to_json())
            elif request.type == RequestType.send_group_message:
                self.client.save_group_message(
                    GroupMessage(
                        content=request.data["content"],
                        sender=request.data["sender"],
                        group_name=request.data['group_name'],
                        time=request.data["time"],
                    )
                )
                self.client.login_socket.send(Response().to_json())


class SocketBalancer:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.__network_socket: Optional[NetworkSocket] = None
        self.__concrete_socket: Optional["Socket"] = None

    def is_socket_closed(self) -> bool:
        return self.__network_socket is None or self.__network_socket.socket_closed

    def __create_socket(self) -> socket.socket:
        s = create_socket()
        s.connect((self.host, self.port))
        return s

    def __create_concrete_socket(self, socket: "Socket") -> "Socket":
        handshaker = ClientHandShaker(key_holder=key_holder, socket=socket)
        handshaker.run_handshaking()
        concrete_socket = SecureSocket(key_holder=key_holder, socket=socket)
        # concrete_socket = MessageSocket(concrete_socket)
        return concrete_socket

    @property
    def concrete_socket(self) -> "Socket":
        if self.is_socket_closed():
            self.__network_socket = NetworkSocket(self.__create_socket())
            self.__concrete_socket = self.__create_concrete_socket(
                self.__network_socket
            )
        return self.__concrete_socket


class Client:
    def __init__(self, config: "Config") -> None:
        self.login_socket_balancer = SocketBalancer(
            host=config.host, port=config.login_port
        )
        self.other_socket_balancer = SocketBalancer(
            host=config.host, port=config.other_port
        )
        self.chat_listener = ChatListener(self)
        self.menu: "Menu" = LoginRegisterMenu(self)

    def menu_transition(self, menu: "Menu"):
        self.menu = menu

    @property
    def login_socket(self) -> "Socket":
        return self.login_socket_balancer.concrete_socket

    @property
    def other_socket(self) -> "Socket":
        return self.other_socket_balancer.concrete_socket

    def toggle_chat_listening(self):
        self.chat_listener.toggle_chat_listening()

    def save_private_message(self, private_message: PrivateMessage):
        private_message.save()

    def save_group_message(self, group_message: GroupMessage):
        group_message.save()

    def show_private_messages(self):
        PrivateMessage.show_messages()

    def show_group_messages(self, group_name):
        GroupMessage.show_messages(group_name)

    def run(self):
        while True:
            self.menu.render()


key_holder = SecureKeyHolder()


def main(config: "Config"):
    print("client: sockets connected")
    Client(config=config).run()


if __name__ == "__main__":
    main(config=main_config)
