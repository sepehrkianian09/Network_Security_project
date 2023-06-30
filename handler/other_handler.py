from sockets.interfaces import Socket


class OtherHandler:
    def __init__(self, socket: "Socket") -> None:
        self.socket = socket

    def run(self):
        message: dict = self.socket.receive(1024)
        if message["type"] == "register":
            print(
                f"server: registered {message['data']['username']} with password {message['data']['password']}."
            )
