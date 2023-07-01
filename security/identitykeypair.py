import json

from security.util.enhancedJSONEncoder import EnhancedJSONEncoder
from .state.state_proto_types import IdentityKeyPairStructure
from .identitykey import IdentityKey
from .ecc.curve import Curve


class IdentityKeyPair:
    def __init__(self, identityKeyPublicKey=None, ecPrivateKey=None, serialized=None):
        if serialized:
            if type(serialized) == bytes:
                serialized = serialized.decode("utf-8")
            data = json.loads(serialized)
            structure = IdentityKeyPairStructure(**data)
            self.publicKey = IdentityKey(bytearray(structure.public_key), offset=0)
            self.privateKey = Curve.decodePrivatePoint(bytearray(structure.private_key))
        else:
            self.publicKey = identityKeyPublicKey
            self.privateKey = ecPrivateKey

    def getPublicKey(self):
        return self.publicKey

    def getPrivateKey(self):
        return self.privateKey

    def serialize(self):
        structure = IdentityKeyPairStructure()
        structure.public_key = self.publicKey.serialize()
        structure.private_key = self.privateKey.serialize()
        return json.dumps(structure, cls=EnhancedJSONEncoder)
