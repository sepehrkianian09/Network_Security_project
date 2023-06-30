from typing import TYPE_CHECKING, List
from menu.interfaces import Menu, MenuHandler

if TYPE_CHECKING:
    from client import Client


class LoginRegisterMenu(Menu):
    def __init__(self, client: "Client") -> None:
        super().__init__(client=client)
        self.__menu_items = [
            MenuHandler(name="Register", handler=self.register),
            MenuHandler(name="Login", handler=self.login),
        ]

    def menu_items(self) -> List[MenuHandler]:
        return self.__menu_items

    def login(self) -> "Menu":
        return self

    def register(self) -> "Menu":
        return self
