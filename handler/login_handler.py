from db_server.user import User, UserAuthentication
from sockets.interfaces import Socket
from messaging import Request, RequestType, Response
from handler.connection_pool import ConnectionPool


class LoginHandler:
    def __init__(self, socket: "Socket") -> None:
        self.socket = socket

    def run(self):
        request: "Request" = Request.schema().loads(self.socket.receive(1024))
        if request.type == RequestType.login:
            # check password and user existence
            user = User.get_user(request.data["username"])
            if user.check_password(request.data["password"]):
                login_token = UserAuthentication(user=user)
                login_token.save()
                ConnectionPool.instance.add_connection(
                    request.data["username"], self.socket
                )
                print(f"server: login {request.data['username']}.")
                response = Response(data={"token": login_token.auth})
                self.socket.send(response.to_json())
