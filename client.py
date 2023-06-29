import threading
from sockets.network import NetworkSocket

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)


sent_message = False


def check_message():
    while not sent_message:
        pass
    print("message checked")


def main():
    global sent_message
    with NetworkSocket() as socket:
        socket.connect(HOST=HOST, PORT=PORT)
        thread = threading.Thread(target=check_message, args=())
        thread.start()
        socket.send("What?")
        socket.receive(1000)
        print("main thread finished")
        sent_message = True


if __name__ == "__main__":
    main()
