from sockets.network import NetworkSocket

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)


def main():
    with NetworkSocket() as socket:
        socket.bind(HOST=HOST, PORT=PORT)
        socket.listen()
        connection, address = socket.accept()
        connection = NetworkSocket(connection)
        with connection:
            received_message = connection.receive(1024)
            print(f"received message {received_message}")
            connection.send(received_message)

if __name__ == "__main__":
    main()