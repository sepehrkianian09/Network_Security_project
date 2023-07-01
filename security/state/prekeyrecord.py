import json

from .state_proto_types import PreKeyRecordStructure
from ..ecc.curve import Curve
from ..ecc.eckeypair import ECKeyPair
from security.util.enhancedJSONEncoder import EnhancedJSONEncoder


class PreKeyRecord:
    def __init__(self, _id=None, ecKeyPair=None, serialized=None):
        self.structure = PreKeyRecordStructure()
        if serialized:
            if type(serialized) == bytes:
                serialized = serialized.decode("utf-8")
            data = json.loads(serialized)
            self.structure = PreKeyRecordStructure(**data)
        else:
            self.structure.id = _id
            self.structure.public_key = ecKeyPair.getPublicKey().serialize()
            self.structure.private_key = ecKeyPair.getPrivateKey().serialize()

    def getId(self):
        return self.structure.id

    def getKeyPair(self):
        publicKey = Curve.decodePoint(bytearray(self.structure.public_key), 0)
        privateKey = Curve.decodePrivatePoint(bytearray(self.structure.private_key))
        return ECKeyPair(publicKey, privateKey)

    def serialize(self):
        return json.dumps(self.structure, cls=EnhancedJSONEncoder)
