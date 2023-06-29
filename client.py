import threading
from sockets.network import NetworkSocket

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)
socket = NetworkSocket()

sent_messages = ""


def read_messages():
    global sent_messages
    while True:
        read_message = socket.receive(1024)
        if read_message == "":
            break
        sent_messages += read_message


def write_messages():
    while True:
        read_line = input()
        if read_line == "stop":
            break
        else:
            socket.send(read_line)


def main():
    global sent_message
    with socket:
        socket.connect(HOST=HOST, PORT=PORT)
        read_thread = threading.Thread(target=read_messages, args=())
        write_thread = threading.Thread(target=write_messages, args=())
        read_thread.start()
        write_thread.start()
        write_thread.join()
        print(f"sent_messages: {sent_messages}")
    read_thread.join()


if __name__ == "__main__":
    main()
