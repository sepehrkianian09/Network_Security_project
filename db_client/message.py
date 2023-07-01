import datetime
from typing import Any, Dict, List, Optional


class Message:
    def __init__(
        self, content: str, time: Optional[Any] = None, sender: str = "You"
    ) -> None:
        self.time = time if time else datetime.datetime.now()
        self.content = content

    def __str__(self) -> str:
        return f"{self.time} : {self.content}"


class PrivateMessage(Message):
    messages: Dict[str, List["PrivateMessage"]] = dict()

    def __init__(
        self,
        content: str,
        time: Optional[Any] = None,
        sender: str = "You",
        receiver_name: str = "You",
    ) -> None:
        super().__init__(content, time, sender)
        self.receiver = receiver_name

    def save(self):
        if not self.messages.__contains__(self.receiver):
            self.messages[self.receiver] = []

        self.messages[self.receiver].append(self)

    @classmethod
    def show_messages(cls):
        for receiver_name in cls.messages:
            print(f"{receiver_name}:")
            for message in cls.messages[receiver_name]:
                print(f"\t{message}")


class GroupMessage(Message):
    messages: Dict[str, List["GroupMessage"]] = dict()

    def __init__(
        self,
        content: str,
        time: Optional[Any] = None,
        sender: str = "You",
        group_name: str = "You",
    ) -> None:
        super().__init__(content, time, sender)
        self.group = group_name

    @classmethod
    def __init_group_message_store__(cls, group_name: str):
        if not cls.messages.__contains__(group_name):
            cls.messages[group_name] = []

    def save(self):
        self.__init_group_message_store__(self.group)
        self.messages[self.group].append(self)

    @classmethod
    def show_messages(cls, group_name: str):
        cls.__init_group_message_store__(group_name)
        for message in cls.messages[group_name]:
            print(f"\t{message}")
