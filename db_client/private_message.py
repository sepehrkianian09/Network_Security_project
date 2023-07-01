import datetime


class PrivateMessage:
    def __init__(self, reciver, message) -> None:
        self.time = datetime.datetime.now()
        self.reciver = reciver
        self.message = message