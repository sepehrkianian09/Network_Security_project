from messaging import Request, RequestType, Response
from sockets.interfaces import Socket


class OtherHandler:
    def __init__(self, socket: "Socket") -> None:
        self.socket = socket

    def run(self):
        request: "Request" = Request.schema().loads(self.socket.receive(1024))
        if request.type == RequestType.register:
            print(
                f"server: registered {request.data['username']} with password {request.data['password']}."
            )
            self.socket.send(Response().to_json())
