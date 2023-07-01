import json

from .state_proto_types import SignedPreKeyRecordStructure
from ..ecc.curve import Curve
from ..ecc.eckeypair import ECKeyPair
from security.util.enhancedJSONEncoder import EnhancedJSONEncoder


class SignedPreKeyRecord:
    def __init__(self, _id=None, timestamp=None, ecKeyPair=None, signature=None, serialized=None):
        self.structure = SignedPreKeyRecordStructure()
        if serialized:
            if type(serialized) == bytes:
                serialized = serialized.decode("utf-8")
            data = json.loads(serialized)
            self.structure = SignedPreKeyRecordStructure(**data)
        else:
            self.structure.id = _id
            self.structure.public_key = ecKeyPair.getPublicKey().serialize()
            self.structure.private_key = ecKeyPair.getPrivateKey().serialize()
            self.structure.signature = signature
            self.structure.timestamp = timestamp

    def getId(self):
        return self.structure.id

    def getTimestamp(self):
        return self.structure.timestamp

    def getKeyPair(self):
        publicKey = Curve.decodePoint(bytearray(self.structure.public_key), 0)
        privateKey = Curve.decodePrivatePoint(bytearray(self.structure.private_key))

        return ECKeyPair(publicKey, privateKey)

    def getSignature(self):
        return self.structure.signature

    def serialize(self):
        return json.dumps(self.structure, cls=EnhancedJSONEncoder)
