from dataclasses import dataclass
import socket


@dataclass
class Config:
    host: str
    login_port: int
    other_port: int


main_config = Config(host=socket.gethostname(), login_port=9000, other_port=9001)
