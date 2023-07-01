from typing import TYPE_CHECKING, List


if TYPE_CHECKING:
    from db_server.user import User


class Group:
    groups = []

    def __init__(self, name: str, owner: "User", members: List["User"] = []):
        self.name = name
        self.owner = owner
        self.members = members

    def save(self):
        self.groups.append(self)

    @classmethod
    def find_groups_by_user(cls, user: "User") -> List["Group"]:
        groups_by_user = []
        for group in Group.groups:
            #Owner is in members.
            for user_iterate in group.members:
                if user.name == user_iterate.name:
                    groups_by_user.append(group)
        return groups_by_user
