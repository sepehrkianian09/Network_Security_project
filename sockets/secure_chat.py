from messaging import Request
from security.ecc.curve import Curve
from security.identitykey import IdentityKey
from security.identitykeypair import IdentityKeyPair
from security.state.sessionrecord import SessionRecord
from sockets.interfaces import DecoratorSocket, Socket


class SecureChatSocket(DecoratorSocket):

    def __init__(self, __socket: "Socket", is_alice: bool) -> None:
        super().__init__(__socket)
        session_record = SessionRecord()
        identity_key_pair = Curve.generateKeyPair()
        identity_key = IdentityKeyPair(IdentityKey(identity_key_pair.getPublicKey()), identity_key_pair.getPrivateKey())
        base_key = Curve.generateKeyPair()
        ephemeral_key = Curve.generateKeyPair()
        if is_alice:
            self.__socket__.send()
        else:
            pass

    def __encrypt__(self, content: str) -> str:
        return ""

    def __decrypt__(self, content: str) -> str:
        return ""

    def send(self, message: Request):
        content = message.data['content']
        content = self.__encrypt__(content)
        message.data['content'] = content
        super(SecureChatSocket, self).send(message)

    def receive(self, message_size) -> Request:
        message = super(SecureChatSocket, self).receive(message_size)
        content = message.data['content']
        content = self.__decrypt__(content)
        message.data['content'] = content
        return message
