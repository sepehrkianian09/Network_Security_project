from typing import TYPE_CHECKING, List
from menu.interfaces import Menu, MenuHandler

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
        pass

    def register(self):
        pass
