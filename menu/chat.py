from typing import TYPE_CHECKING, List
from menu.interfaces import Menu, MenuHandler
from messaging import Request, RequestType, Response, ResponseType

if TYPE_CHECKING:
    from client import Client


class ChatMenu(Menu):
    def __init__(self, client: "Client") -> None:
        super().__init__(client=client)
        self.menu_items = [
            MenuHandler(name="Show Online Users", handler=self.show_online_users),
            MenuHandler(name="Send Message", handler=self.send_message),
            MenuHandler(
                name="Show Received Messages", handler=self.show_received_messages
            ),
            MenuHandler(name="Create Group", handler=self.create_group),
            MenuHandler(name="Show Groups", handler=self.show_groups),
            MenuHandler(name="Enter Group", handler=self.enter_group),
            MenuHandler(name="Logout", handler=self.logout),
        ]

    def show_online_users(self):
        pass

    def send_message(self):
        pass

    def show_received_messages(self):
        pass

    def create_group(self):
        pass

    def show_groups(self):
        pass

    def enter_group(self):
        pass

    def logout(self):
        logout_request = Request(type=RequestType.logout)
        logout_request.add_auth()
        self.client.other_socket.send(logout_request.to_json())
        response: "Response" = Response.schema().loads(
            self.client.other_socket.receive(1024)
        )
        if response.type == ResponseType.success:
            print("client: Logout Successful!")
            Request.remove_auth()
            self.client.toggle_chat_listening()
