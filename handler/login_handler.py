from sockets.interfaces import Socket
from messaging import Request, RequestType, Response
from handler.connection_pool import ConnectionPool

class LoginHandler:
    def __init__(self, socket: "Socket") -> None:
        self.socket = socket

    def run(self):
        request: "Request" = Request.schema().loads(self.socket.receive(1024))
        if request.type == RequestType.login:
            #Token Gen
            ConnectionPool.instance.add_connection(request.data['username'], self.socket)
            print(
                f"server: login {request.data['username']}."
            )
            response = Response(data={'token':'fff'})
            self.socket.send(response.to_json())


    def random_token(self):
        pass