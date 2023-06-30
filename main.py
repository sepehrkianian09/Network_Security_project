import threading
from client import main as client_main
from server import main as server_main
from thread_pool import ThreadPool

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)

if __name__ == "__main__":
    ThreadPool(
        threads=[
            threading.Thread(target=server_main, args=[(HOST, PORT)]),
            threading.Thread(target=client_main, args=[(HOST, PORT)]),
        ]
    ).run()
