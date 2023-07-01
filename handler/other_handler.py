from db_server.user import User, UserAuthentication
from handler.connection_pool import ConnectionPool
from messaging import Request, RequestType, Response
from sockets.interfaces import Socket


class OtherHandler:
    def __init__(self, socket: "Socket") -> None:
        self.socket = socket

    def run(self):
        request: "Request" = Request.schema().loads(self.socket.receive(1024))
        if request.type == RequestType.register:
            # Add to db: PostgrSQL
            User(
                user_name=request.data["username"], password=request.data["password"]
            ).save()
            print(
                f"server: registered {request.data['username']} with password {request.data['password']}."
            )
            self.socket.send(Response().to_json())
        elif request.type == RequestType.logout:
            if UserAuthentication.auth_exists(request.auth_token):
                user = UserAuthentication.find_auth(request.auth_token).user
                UserAuthentication.remove_auth(request.auth_token)
                ConnectionPool.instance().remove_connection(user.user_name)
                self.socket.send(Response().to_json())
                print(f"server: logout successful")
        elif request.type == RequestType.show_online_users:
            if UserAuthentication.auth_exists(request.auth_token):
                response = Response(
                    data={"online_users": ConnectionPool.instance().get_connected_ids()}
                )
                self.socket.send(response.to_json())
        elif request.type == RequestType.show_groups:
            pass
        elif request.type == RequestType.show_chats:
            pass
        elif request.type == RequestType.send_private_message:
            pass
        elif request.type == RequestType.send_group_message:
            pass
        elif request.type == RequestType.enter_group:
            pass
        elif request.type == RequestType.create_group:
            pass
