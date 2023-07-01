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


def load_public_key(filename):
    with open(filename, 'rb') as file:
        return rsa.PublicKey.load_pkcs1(file.read())


def load_private_key(filename):
    with open(filename, 'rb') as file:
        return rsa.PrivateKey.load_pkcs1(file.read())


server_public, server_private = load_public_key('server_public.key'), load_private_key('server_private.key')
alice_public, alice_private = load_public_key('alice_public.key'), load_private_key('alice_private.key')

main_config = Config(
    host=socket.gethostname(),
    login_port=9000,
    other_port=9001,
    server_public=server_public,
    server_private=server_private,
    alice_public=alice_public,
    alice_private=alice_private,
)
