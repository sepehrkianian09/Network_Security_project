import json

from .senderkeystate import SenderKeyState
from security.util.enhancedJSONEncoder import EnhancedJSONEncoder
from security.exceptions.invalidkeyidexception import InvalidKeyIdException
from ...state.state_proto_types import SenderKeyRecordStructure


class SenderKeyRecord:
    def __init__(self, serialized=None):
        self.senderKeyStates = []

        if serialized:
            if type(serialized) == bytes:
                serialized = serialized.decode("utf-8")
            data = json.loads(serialized)
            senderKeyRecordStructure = SenderKeyRecordStructure(**data)

            for structure in senderKeyRecordStructure.sender_key_states:
                self.senderKeyStates.append(SenderKeyState(senderKeyStateStructure=structure))


    def isEmpty(self):
        return len(self.senderKeyStates) == 0

    def getSenderKeyState(self, keyId=None):
        if keyId is None:
            if len(self.senderKeyStates):
                return self.senderKeyStates[0]
            else:
                raise InvalidKeyIdException("No key state in record")
        else:
            for state in self.senderKeyStates:
                if state.getKeyId() == keyId:
                    return state
            raise InvalidKeyIdException("No keys for: %s" % keyId)

    def addSenderKeyState(self, id, iteration, chainKey, signatureKey):
        self.senderKeyStates.append(SenderKeyState(id, iteration, chainKey, signatureKey))

    def setSenderKeyState(self, id, iteration, chainKey, signatureKey):
        del self.senderKeyStates[:]
        self.senderKeyStates.append(SenderKeyState(id, iteration, chainKey, signatureKeyPair=signatureKey))

    def serialize(self):
        recordStructure = SenderKeyRecordStructure()

        for senderKeyState in self.senderKeyStates:
            recordStructure.sender_key_states.extend([senderKeyState.getStructure()])

        return json.dumps(recordStructure, cls=EnhancedJSONEncoder)
