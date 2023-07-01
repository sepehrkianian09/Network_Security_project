from db_server.group import Group
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
                name=request.data["username"], password=request.data["password"]
            ).save()
            print(
                f"server: registered {request.data['username']} with password {request.data['password']}."
            )
            self.socket.send(Response().to_json())
        elif request.type == RequestType.logout:
            if UserAuthentication.auth_exists(request.auth_token):
                user = UserAuthentication.find_auth(request.auth_token).user
                UserAuthentication.remove_auth(request.auth_token)
                ConnectionPool.instance().remove_connection(user.name)
                print(f"server: logout successful")
                self.socket.send(Response().to_json())
        elif request.type == RequestType.show_online_users:
            if UserAuthentication.auth_exists(request.auth_token):
                response = Response(
                    data={"online_users": ConnectionPool.instance().get_connected_ids()}
                )
                self.socket.send(response.to_json())
        elif request.type == RequestType.create_group:
            if UserAuthentication.auth_exists(request.auth_token):
                user = UserAuthentication.find_auth(request.auth_token).user
                group = Group(
                    name=request.data["group_name"], owner=user, members=[user]
                )
                group.save()
                self.socket.send(Response().to_json())
        elif request.type == RequestType.show_groups:
            if UserAuthentication.auth_exists(request.auth_token):
                user = UserAuthentication.find_auth(request.auth_token).user
                user_groups = Group.find_groups_by_user(user=user)
                user_group_names = list(map(lambda group: group.name, user_groups))
                response = Response(data={"groups": user_group_names})
                self.socket.send(response.to_json())
        elif request.type == RequestType.show_chats:
            pass
        elif request.type == RequestType.send_private_message:
            pass
        elif request.type == RequestType.send_group_message:
            pass
        elif request.type == RequestType.enter_group:
            pass
