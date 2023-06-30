import threading
from typing import List


class ThreadPool:
    def __init__(self, threads: List[threading.Thread]) -> None:
        self.threads = threads

    def run(self):
        for thread in self.threads:
            thread.start()
        for thread in self.threads:
            thread.join()
