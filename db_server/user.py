class User:
    users = []

    def __init__(self, user_name: str, password: str):
        self.user_name = user_name
        self.password = password

    @classmethod
    def get_user(cls, user_name: str) -> "User":
        # TODO
        return cls.users[0]

    def check_password(self, password: str) -> bool:
        return True

    def save(self):
        self.users.append(self)


class UserAuthentication:
    user_auths = []

    def __generate_unique_random_auth(self) -> str:
        return ""

    def __init__(self, user: "User") -> None:
        self.user = user
        self.auth = self.__generate_unique_random_auth()

    def save(self):
        self.__save(self)

    @classmethod
    def __save(cls, self: "UserAuthentication"):
        cls.user_auths.append(self)

    @classmethod
    def find_auth(cls, auth: str) -> "UserAuthentication":
        return cls.user_auths[0]

    @classmethod
    def auth_exists(cls, auth: str) -> bool:
        return True

    @classmethod
    def remove_auth(cls, auth: str):
        cls.user_auths.pop(0)
