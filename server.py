from typing import Tuple
from handshaking.server import ServerHandShaker
from key_holder import SecureKeyHolder
from sockets.interfaces import Socket
from sockets.network import NetworkSocket
from sockets.secure import SecureSocket


class Server:
    def __init__(self, socket: "Socket") -> None:
        self.socket = socket

    def run(self):
        while True:
            received_message = self.socket.receive(1024)
            if received_message:
                self.socket.send(received_message)
            if received_message == "stop":
                break
            else:
                print(f"received message {received_message}")


def main(args: Tuple[str, int]):
    HOST, PORT = args
    key_holder = SecureKeyHolder()
    with NetworkSocket() as socket:
        socket.bind(HOST=HOST, PORT=PORT)
        socket.listen()
        connection, address = socket.accept()
        connection = NetworkSocket(connection)
        with connection:
            handshaker = ServerHandShaker(socket=connection, key_holder=key_holder)
            handshaker.run_handshaking()
            concrete_socket = SecureSocket(key_holder=key_holder, socket=connection)
            Server(concrete_socket).run()


if __name__ == "__main__":
    main(("127.0.0.1", 65432))
