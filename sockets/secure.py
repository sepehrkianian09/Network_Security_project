import base64
import hashlib
import json

import rsa

from config import main_config
from key_holder import KeyHolder
from sockets.interfaces import DecoratorSocket, Socket

MESSAGE_TYPE = str


class SecureSocket(DecoratorSocket):
    def __init__(self, key_holder: KeyHolder, public_key, private_key, remote_pub_key, socket: "Socket") -> None:
        super().__init__(socket)
        self.__key_holder = key_holder
        self.public_key = public_key
        self.private_key = private_key
        self.remote_pub_key = remote_pub_key

    def append_hash(self, message: MESSAGE_TYPE) -> MESSAGE_TYPE:
        private_key = main_config.alice_private
        h = hashlib.sha256(message.encode('utf-8'))
        signature = rsa.encrypt(bytes(h.hexdigest()), private_key)
        result = base64.b64encode(signature).decode()
        return json.dumps({'message': message, 'sign': result})

    def check_hash(self, message: MESSAGE_TYPE):
        data = json.loads(message)
        if not (data.get('message') and data.get('sign')):
            raise Exception()
        h = hashlib.sha256(data['message'].encode('utf-8')).hexdigest()
        received_hash = rsa.decrypt(bytes(data['sign']), self.remote_pub_key)
        received_hash = base64.b64encode(received_hash).decode()
        if received_hash != h:
            raise Exception()
        return data['message']

    def encrypt(self, message: MESSAGE_TYPE) -> MESSAGE_TYPE:
        return base64.b64encode(rsa.encrypt(bytes(message), self.remote_pub_key)).decode()

    def decrypt(self, message: MESSAGE_TYPE) -> MESSAGE_TYPE:
        return base64.b64encode(rsa.decrypt(bytes(message), self.private_key)).decode()

    def send(self, message: MESSAGE_TYPE):
        message = self.append_hash(message)
        print(message)
        message = self.encrypt(message)
        print(message)
        super().send(message)

    def receive(self, message_size) -> MESSAGE_TYPE:
        message = super().receive(message_size=message_size)
        print(message)
        message = self.decrypt(message)
        print(message)
        message = self.check_hash(message)
        print(message)
        return message
