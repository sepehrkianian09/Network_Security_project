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
        pass

    def get_connection(self, id: ID_TYPE) -> "Socket":
        return self.pool_map[id]

    def remove_connection(self, id: ID_TYPE):
        pass
