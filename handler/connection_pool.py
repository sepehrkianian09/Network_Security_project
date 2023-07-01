from typing import Dict, List, Optional
from sockets.interfaces import Socket


ID_TYPE = str


class ConnectionPool:
    __instance__: Optional["ConnectionPool"] = None

    @classmethod
    def instance(cls) -> "ConnectionPool":
        if not cls.__instance__:
            cls.__instance__ = cls()
        return cls.__instance__

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

    def get_connected_ids(self) -> List[ID_TYPE]:
        return list(self.pool_map.keys())
