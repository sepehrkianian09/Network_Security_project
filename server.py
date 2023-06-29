from sockets.interfaces import Socket
from sockets.network import NetworkSocket

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)


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


if __name__ == "__main__":
    with NetworkSocket() as socket:
        socket.bind(HOST=HOST, PORT=PORT)
        socket.listen()
        connection, address = socket.accept()
        connection = NetworkSocket(connection)
        with connection:
            Server(connection).run()
