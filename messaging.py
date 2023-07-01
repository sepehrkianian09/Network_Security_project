from dataclasses import dataclass
from enum import Enum
import json
from typing import Dict, Optional

from dataclasses_json import dataclass_json


class RequestType(Enum):
    register = "Register"
    login = "Login"
    show_online_users = "Show Online Users"
    send_private_message = "Send Message"
    create_group = "Create Group"
    show_groups = "Show Groups"
    enter_group = "Enter Group"
    logout = "Logout"
    add_user = "Add User"
    show_members = "Show Members"
    send_group_message = "Send Group Message"


auth: Optional[str] = None


@dataclass_json
@dataclass
class Request:
    type: RequestType
    data: Optional[Dict] = None
    auth_token: Optional[str] = None

    def add_auth(self):
        self.auth_token = auth

    @classmethod
    def remove_auth(cls):
        global auth
        auth = None

    @classmethod
    def set_auth(cls, new_auth: str):
        global auth
        auth = new_auth


class ResponseType(Enum):
    success = "success!"


@dataclass_json
@dataclass
class Response:
    type: ResponseType = ResponseType.success
    data: Optional[Dict] = None


if __name__ == "__main__":
    print(Request(RequestType.add_user, {}).to_json())
