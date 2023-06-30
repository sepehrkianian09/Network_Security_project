from sockets.interfaces import Socket


class OtherHandler:
    def __init__(self, socket: "Socket") -> None:
        self.socket = socket

    def run(self):
        pass
