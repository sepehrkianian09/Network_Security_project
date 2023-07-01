from messaging import Request, RequestType, Response
from sockets.interfaces import Socket


class OtherHandler:
    def __init__(self, socket: "Socket") -> None:
        self.socket = socket

    def run(self):
        request: "Request" = Request.schema().loads(self.socket.receive(1024))
        if request.type == RequestType.register:
            #Add to db: PostgrSQL
            print(
                f"server: registered {request.data['username']} with password {request.data['password']}."
            )
            self.socket.send(Response().to_json())
        if request.type == RequestType.logout:
            #remove token
            #remove conn
            pass
        if request.type == RequestType.show_online_users:
            pass
        if request.type == RequestType.show_groups:
            pass
        if request.type == RequestType.show_chats:
            pass
        if request.type == RequestType.send_private_message:
            pass
        if request.type == RequestType.send_group_message:
            pass
        if request.type == RequestType.enter_group:
            pass
        if request.type == RequestType.create_group:
            pass