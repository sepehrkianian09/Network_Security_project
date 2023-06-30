import json
from sockets.interfaces import DecoratorSocket


class JsonSocket(DecoratorSocket):
    def send(self, message):
        super().send(json.dumps(message))

    def receive(self, message_size):
        return json.loads(super().receive(message_size))
