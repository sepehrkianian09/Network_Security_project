import threading
from sockets.interfaces import Socket
from sockets.network import NetworkSocket

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)


class Client:
    def __init__(self, socket: "Socket") -> None:
        self.socket = socket
        self.sent_messages: str = ""

    def run(self):
        read_thread = threading.Thread(target=self.read_messages, args=())
        write_thread = threading.Thread(target=self.write_messages, args=())
        read_thread.start()
        write_thread.start()
        write_thread.join()
        read_thread.join()
        print(f"sent_messages: {self.sent_messages}")

    def read_messages(self):
        while True:
            read_message = self.socket.receive(1024)
            # print(f"read Message: {read_message}")
            if read_message == "stop":
                break
            self.sent_messages += read_message

    def write_messages(self):
        while True:
            read_line = input()
            self.socket.send(read_line)
            if read_line == "stop":
                break


if __name__ == "__main__":
    socket = NetworkSocket()
    with socket:
        socket.connect(HOST=HOST, PORT=PORT)
        Client(socket=socket).run()
