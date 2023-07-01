from typing import TYPE_CHECKING
from menu.interfaces import Menu, MenuHandler
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
        self.client.other_socket.__exit__()

    def login(self):
        self.client.login_socket.send(
            Request(
                type=RequestType.login,
                data={
                    "username": self.get_input("username"),
                    "password": self.get_input("password"),
                },
            ).to_json()
        )
        response: "Response" = Response.schema().loads(
            self.client.login_socket.receive(1024)
        )
        if response.type == ResponseType.success:
            print("client: Login Successful!")
            Request.set_auth(response.data["token"])
            self.client.toggle_chat_listening()
            self.client.menu_transition(ChatMenu(self.client))


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
        request = Request(type=RequestType.show_online_users)
        request.add_auth()
        self.client.other_socket.send(request.to_json())
        response: "Response" = Response.schema().loads(
            self.client.other_socket.receive(1024)
        )
        if response.type == ResponseType.success:
            print(f"Online Users: {response.data['online_users']}")
        self.client.other_socket.__exit__()

    def send_message(self):
        pass

    def show_received_messages(self):
        pass

    def create_group(self):
        request = Request(
            type=RequestType.create_group,
            data={
                "group_name": self.get_input("Group Name"),
            },
        )
        request.add_auth()
        self.client.other_socket.send(request.to_json())
        response: "Response" = Response.schema().loads(
            self.client.other_socket.receive(1024)
        )
        if response.type == ResponseType.success:
            print("Create Group Successful!")
        self.client.other_socket.__exit__()

    def show_groups(self):
        request = Request(type=RequestType.show_groups)
        request.add_auth()
        self.client.other_socket.send(request.to_json())
        response: "Response" = Response.schema().loads(
            self.client.other_socket.receive(1024)
        )
        if response.type == ResponseType.success:
            print(f"Groups: {response.data['groups']}")
        self.client.other_socket.__exit__()

    def enter_group(self):
        group_name = self.get_input("Group Name")
        request = Request(
            type=RequestType.enter_group,
            data={"group_name": group_name},
        )
        request.add_auth()
        self.client.other_socket.send(request.to_json())
        response: "Response" = Response.schema().loads(
            self.client.other_socket.receive(1024)
        )
        if response.type == ResponseType.success:
            print(f"Entered Group {group_name}")
            is_admin = response.data["is_admin"]
            self.client.menu_transition(
                GroupChatMenu(self.client, group_name=group_name, is_admin=is_admin)
            )
        self.client.other_socket.__exit__()

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
            self.client.login_socket.__exit__()
            self.client.menu_transition(LoginRegisterMenu(self.client))
        self.client.other_socket.__exit__()


class GroupChatMenu(Menu):
    def __init__(self, client: "Client", group_name: str, is_admin: bool) -> None:
        super().__init__(client=client)
        self.group_name = group_name
        self.menu_items = [
            MenuHandler(name="Show Members", handler=self.show_members),
            MenuHandler(name="Show Chats", handler=self.show_chats),
            MenuHandler(name="Send Message", handler=self.send_message),
            MenuHandler(name="Back", handler=self.back),
        ]
        # This should be shown if user is the Admin
        if is_admin:
            self.menu_items.insert(
                0, MenuHandler(name="Add User", handler=self.add_user)
            )

    def add_user(self):
        request = Request(
            type=RequestType.add_user,
            data={"group_name": self.group_name, "user_name": self.get_input("User Name")},
        )
        request.add_auth()
        self.client.other_socket.send(request.to_json())
        response: "Response" = Response.schema().loads(
            self.client.other_socket.receive(1024)
        )
        if response.type == ResponseType.success:
            print(f"User Added")
        self.client.other_socket.__exit__()

    def show_members(self):
        request = Request(
            type=RequestType.show_members,
            data={"group_name": self.group_name},
        )
        request.add_auth()
        self.client.other_socket.send(request.to_json())
        response: "Response" = Response.schema().loads(
            self.client.other_socket.receive(1024)
        )
        if response.type == ResponseType.success:
            print(f"Members: {response.data['members']}")
        self.client.other_socket.__exit__()

    def show_chats(self):
        pass

    def send_message(self):
        pass

    def back(self):
        self.client.menu_transition(ChatMenu(self.client))
