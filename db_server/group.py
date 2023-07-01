from typing import TYPE_CHECKING, List, Optional


if TYPE_CHECKING:
    from db_server.user import User


class Group:
    groups: List["Group"] = []

    def __init__(self, name: str, owner: "User", members: List["User"] = []):
        self.name = name
        self.admin = owner
        self.members = members

    def add_member(self, member: "User"):
        self.members.append(member)

    def save(self):
        self.groups.append(self)

    @classmethod
    def find_group_by_name(cls, group_name: str) -> Optional["Group"]:
        for group in cls.groups:
            if group.name == group_name:
                return group
        return None

    @classmethod
    def find_groups_by_user(cls, user: "User") -> List["Group"]:
        groups_by_user = []
        for group in Group.groups:
            # Owner is in members.
            for user_iterate in group.members:
                if user.name == user_iterate.name:
                    groups_by_user.append(group)
        return groups_by_user
