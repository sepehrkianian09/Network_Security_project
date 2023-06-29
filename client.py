from sockets.network import NetworkSocket

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)


def main():
    with NetworkSocket() as socket:
        socket.connect(HOST=HOST, PORT=PORT)
        socket.send("What?")
        print(socket.receive(1000))


if __name__ == "__main__":
    main()
