import base64
import json
import os

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
        signature = rsa.sign(message.encode('utf-8'), self.private_key, 'SHA-256')
        result = base64.b64encode(signature).decode()
        return json.dumps({'message': message, 'sign': result})

    def check_hash(self, message: MESSAGE_TYPE):
        data = json.loads(message)
        if not (data.get('message') and data.get('sign')):
            raise Exception()

        if rsa.verify(bytes(data['message'], 'utf-8'), base64.b64decode(bytes(data['sign'], 'utf-8')), self.remote_pub_key) != 'SHA-256':
            raise Exception()
        return data['message']

    def encrypt(self, message: MESSAGE_TYPE) -> MESSAGE_TYPE:
        from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
        from cryptography.hazmat.backends import default_backend
        from cryptography.hazmat.primitives import padding
        key = os.urandom(32)
        iv = os.urandom(16)
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        encryptor = cipher.encryptor()
        padder = padding.PKCS7(128).padder()
        padded_plaintext = padder.update(bytes(message, 'utf-8')) + padder.finalize()
        ct = encryptor.update(padded_plaintext) + encryptor.finalize()
        key = base64.b64encode(key).decode()
        iv = base64.b64encode(iv).decode()
        spec = {'key': key, 'iv': iv}
        spec = bytes(json.dumps(spec), 'utf-8')
        x = {
            'key': base64.b64encode(rsa.encrypt(spec, self.remote_pub_key)).decode(),
            'message': base64.b64encode(ct).decode()
        }
        return json.dumps(x)

    def decrypt(self, message: MESSAGE_TYPE) -> MESSAGE_TYPE:
        from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
        from cryptography.hazmat.backends import default_backend
        from cryptography.hazmat.primitives import padding
        x = json.loads(message)
        spec = rsa.decrypt(base64.b64decode(bytes(x['key'], 'utf-8')), self.private_key).decode()
        spec = json.loads(spec)
        key = base64.b64decode(bytes(spec['key'], 'utf-8'))
        iv = base64.b64decode(bytes(spec['iv'], 'utf-8'))
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        result = decryptor.update(base64.b64decode(bytes(x['message'], 'utf-8'))) + decryptor.finalize()
        unpadder = padding.PKCS7(128).unpadder()
        plaintext = unpadder.update(result) + unpadder.finalize()
        plaintext = plaintext.decode()
        return plaintext

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
