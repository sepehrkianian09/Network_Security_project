from typing import TYPE_CHECKING, List
from menu.interfaces import Menu, MenuHandler
from menu.chat import ChatMenu
from messaging import Request, RequestType, Response, ResponseType

if TYPE_CHECKING:
    from client import Client


class LoginRegisterMenu(Menu):
    def __init__(self, client: "Client") -> None:
        super().__init__(client=client)
        self.menu_items = [
            MenuHandler(name="Register", handler=self.register),
            MenuHandler(name="Login", handler=self.login),
        ]

    def login(self):
        self.client.login_socket.send(
            Request(
                type=RequestType.register,
                data={
                    "username": self.get_input("username"),
                    "password": self.get_input("password"),
                },
            ).to_json()
        )
        response: "Response" = Response.schema().loads(
            self.client.other_socket.receive(1024)
        )
        if response.type == ResponseType.success:
            print("client: Register Successful!")
            self.client.menu_transition(ChatMenu(self.client))


    def register(self):
        self.client.other_socket.send(
            Request(
                type=RequestType.register,
                data={
                    "username": self.get_input("username"),
                    "password": self.get_input("password"),
                },
            ).to_json()
        )
        response: "Response" = Response.schema().loads(
            self.client.other_socket.receive(1024)
        )
        if response.type == ResponseType.success:
            print("client: Register Successful!")
