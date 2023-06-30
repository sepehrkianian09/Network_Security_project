from typing import TYPE_CHECKING, List
from menu.interfaces import Menu, MenuHandler

if TYPE_CHECKING:
    from client import Client


class GroupChatMenu(Menu):
    def __init__(self, client: "Client") -> None:
        super().__init__(client=client)
        self.menu_items = [
            # This should be shown if user is the Admin
            # MenuHandler(name="Add Users", handler=self.add_users),
            MenuHandler(name="Show Chats", handler=self.show_chats),
            MenuHandler(name="Send Message", handler=self.send_message),
            MenuHandler(name="Back", handler=self.back),
        ]

    def add_users(self):
        pass

    def show_chats(self):
        pass

    def send_message(self):
        pass

    def back(self):
        pass
