class User:
    users = []

    def __init__(self, name):
        self.name = name
        self.ID = self.token_gen()
        User.users.append(self)

    
    def token_gen(self):
        return "pass"