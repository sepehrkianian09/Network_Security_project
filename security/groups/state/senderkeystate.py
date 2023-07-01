from ...state import state_proto_types as storageprotos
from ..ratchet.senderchainkey import SenderChainKey
from ..ratchet.sendermessagekey import SenderMessageKey
from ...ecc.curve import Curve


class SenderKeyState:
    def __init__(self, id=None, iteration=None, chainKey=None,
                 signatureKeyPublic=None, signatureKeyPrivate=None,
                 signatureKeyPair=None, senderKeyStateStructure=None):
        assert (bool(id) and bool(iteration) and bool(chainKey)) or \
               (bool(senderKeyStateStructure) ^ bool(signatureKeyPublic or signatureKeyPair)) or \
               (bool(signatureKeyPublic) ^ bool(signatureKeyPair)), "Missing required arguments"

        if senderKeyStateStructure:
            self.senderKeyStateStructure = senderKeyStateStructure
        else:
            if signatureKeyPair:
                signatureKeyPublic = signatureKeyPair.getPublicKey()
                signatureKeyPrivate = signatureKeyPair.getPrivateKey()

            self.senderKeyStateStructure = storageprotos.SenderKeyStateStructure()
            senderChainKeyStructure = storageprotos.SenderKeyStateStructureSenderChainKey()
            senderChainKeyStructure.iteration = iteration
            senderChainKeyStructure.seed = chainKey
            self.senderKeyStateStructure.sender_chain_key = senderChainKeyStructure

            signingKeyStructure = storageprotos.SenderKeyStateStructureSenderSigningKey()
            signingKeyStructure.public = signatureKeyPublic.serialize()

            if signatureKeyPrivate:
                signingKeyStructure.private = signatureKeyPrivate.serialize()

            self.senderKeyStateStructure.sender_key_id = id
            self.senderChainKey = senderChainKeyStructure
            self.senderKeyStateStructure.sender_signing_key = signingKeyStructure.copy()

    def getKeyId(self):
        return self.senderKeyStateStructure.sender_key_id

    def getSenderChainKey(self):
        return SenderChainKey(self.senderKeyStateStructure.sender_chain_key.iteration,
                              bytearray(self.senderKeyStateStructure.sender_chain_key.seed))

    def setSenderChainKey(self, chainKey):
        self.senderKeyStateStructure.sender_chain_key.iteration = chainKey.getIteration()
        self.senderKeyStateStructure.sender_chain_key.seed = chainKey.getSeed()

    def getSigningKeyPublic(self):
        return Curve.decodePoint(bytearray(self.senderKeyStateStructure.sender_signing_key.public), 0)

    def getSigningKeyPrivate(self):
        return Curve.decodePrivatePoint(self.senderKeyStateStructure.sender_signing_key.private)

    def hasSenderMessageKey(self, iteration):
        for senderMessageKey in self.senderKeyStateStructure.sender_message_keys:
            if senderMessageKey.iteration == iteration:
                return True

        return False

    def addSenderMessageKey(self, senderMessageKey):
        smk = storageprotos.SenderKeyStateStructureSenderMessageKey()
        smk.iteration = senderMessageKey.iteration
        smk.seed = senderMessageKey.seed
        self.senderKeyStateStructure.sender_message_keys.extend([smk])

    def removeSenderMessageKey(self, iteration):
        keys = self.senderKeyStateStructure.sender_message_keys
        result = None

        for i in range(0, len(keys)):
            senderMessageKey = keys[i]
            if senderMessageKey.iteration == iteration:
                result = senderMessageKey
                del keys[i]
                break

        if result is not None:
            return SenderMessageKey(result.iteration, bytearray(result.seed))

        return None

    def getStructure(self):
        return self.senderKeyStateStructure
