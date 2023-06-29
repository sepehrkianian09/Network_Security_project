import threading
from client import main as client_main
from server import main as server_main

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)

if __name__ == "__main__":
    client_thread = threading.Thread(target=client_main, args=[(HOST, PORT)])
    server_thread = threading.Thread(target=server_main, args=[(HOST, PORT)])
    server_thread.start()
    client_thread.start()
    client_thread.join()
    server_thread.join()
