import random
import string

class User:
    users = []

    def __init__(self, user_name: str, password: str):
        self.user_name = user_name
        self.password = password

    @classmethod
    def get_user(cls, user_name: str) -> "User":
        for user in cls.users:
            if user.name == user_name:
                  return user
        return None
    

    def check_password(self, password: str) -> bool:
        return self.password == password

    def save(self):
        self.users.append(self)


class UserAuthentication:
    user_auths = []

    def __generate_unique_random_auth(self) -> str:
        while True:
            chars = string.ascii_letters + string.digits
            token = ''.join(random.choices(chars, k=16))
            if not self.auth_exists(token):
                return token


    def __init__(self, user: "User") -> None:
        self.user = user
        self.auth = self.__generate_unique_random_auth()

    def save(self):
        self.user_auths.append(self)

    @classmethod
    def find_auth(cls, auth: str) -> "UserAuthentication":
        for user_auth in cls.user_auths:
            if user_auth.auth == auth:
                 return user_auth
        return None

    @classmethod
    def auth_exists(cls, auth: str) -> bool:
        for user_auth in cls.user_auths:
            if user_auth.auth == auth:
                 return True
        return False

    @classmethod
    def remove_auth(cls, auth: str):
        for user_auth in cls.user_auths:
            if user_auth.auth == auth:
                cls.user_auths.remove(user_auth)
