class Group:
    def __init__(self, name, owner, members):
        self.name = name
        self.owner = owner
        self.members = members
        self.ID = self.token_gen()



    def token_gen(self):
        return "pass"