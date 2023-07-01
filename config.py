from dataclasses import dataclass
import socket
import rsa

from rsa import PublicKey, PrivateKey


@dataclass
class Config:
    host: str
    login_port: int
    other_port: int
    server_public: "PublicKey"
    server_private: "PrivateKey"
    alice_public: "PublicKey"
    alice_private: "PrivateKey"


server_public, server_private = rsa.newkeys(512)
alice_public, alice_private = rsa.newkeys(512)
main_config = Config(
    host=socket.gethostname(),
    login_port=9000,
    other_port=9001,
    server_public=server_public,
    server_private=server_private,
    alice_public=alice_public,
    alice_private=alice_private,
)
