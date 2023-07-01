import datetime


class GroupMessage:
    def __init__(self, group, sender) -> None:
        self.time = datetime.datetime.now()
        self.group = group
        self.sender = sender