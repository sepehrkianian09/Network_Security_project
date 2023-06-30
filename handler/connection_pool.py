from typing import Dict
from sockets.interfaces import Socket


ID_TYPE = str


class ConnectionPool:
    __instance__: "ConnectionPool"

    @property
    @classmethod
    def instance(cls) -> "ConnectionPool":
        if cls.__instance__:
            return cls.__instance__
        else:
            return cls()

    def __init__(self) -> None:
        self.pool_map: Dict[ID_TYPE, "Socket"] = {}

    def add_connection(self, id: ID_TYPE, socket: "Socket"):
        if self.contains_connection(id):
            self.remove_connection(id)
        self.pool_map[id] = socket

    def get_connection(self, id: ID_TYPE) -> "Socket":
        if self.contains_connection(id):
            return self.pool_map[id]
        else:
            raise Exception()

    def remove_connection(self, id: ID_TYPE):
        if self.contains_connection(id):
            removed_socket = self.pool_map.pop(id)
            removed_socket.__exit__()

    def contains_connection(self, id: ID_TYPE) -> bool:
        return id in self.pool_map
