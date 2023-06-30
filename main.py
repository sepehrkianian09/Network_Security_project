import threading
from client import main as client_main
from server import main as server_main
from thread_pool import ThreadPool
from config import main_config

if __name__ == "__main__":
    ThreadPool(
        threads=[
            threading.Thread(target=lambda: server_main(main_config)),
            threading.Thread(target=lambda: client_main(main_config)),
        ]
    ).run()
