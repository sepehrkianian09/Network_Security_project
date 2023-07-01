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
    show_chats = "Show Chats"
    send_group_message = "Send Group Message"


@dataclass_json
@dataclass
class Request:
    type: RequestType
    data: Dict
    header: Optional[Dict] = None


class ResponseType(Enum):
    success = "success!"


@dataclass_json
@dataclass
class Response:
    type: ResponseType = ResponseType.success
    data: Optional[Dict] = None


if __name__ == "__main__":
    print(Request(RequestType.add_user, {}).to_json())
