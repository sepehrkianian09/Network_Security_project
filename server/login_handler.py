from sockets.interfaces import Socket


class LoginHandler:
    def __init__(self, socket: "Socket") -> None:
        self.socket = socket

    def run(self):
        pass
