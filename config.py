from dataclasses import dataclass


@dataclass
class Config:
    host: str
    login_port: int
    other_port: int


main_config = Config(host="127.0.0.1", login_port=50100, other_port=65432)
