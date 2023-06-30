import json
from messaging import Request
from sockets.interfaces import DecoratorSocket


class MessageSocket(DecoratorSocket):
    def send(self, message: Request):
        super().send(message.to_json())

    def receive(self, message_size) -> Request:
        return Request.schema().loads(super().receive(message_size))
