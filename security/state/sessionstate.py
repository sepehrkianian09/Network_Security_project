from . import state_proto_types as storageprotos
from ..identitykeypair import IdentityKey, IdentityKeyPair
from ..ratchet.rootkey import RootKey
from ..kdf.hkdf import HKDF
from ..ecc.curve import Curve
from ..ecc.eckeypair import ECKeyPair
from ..ratchet.chainkey import ChainKey
from ..kdf.messagekeys import MessageKeys


class SessionState:
    def __init__(self, session=None):
        if session is None:
            self.sessionStructure = storageprotos.SessionStructure()
            self.sessionStructure.sender_chain = storageprotos.SessionStructureChain()
            self.sessionStructure.sender_chain.chain_key = storageprotos.SessionStructureChainChainKey()
        elif session.__class__ == SessionState:
            self.sessionStructure = session.sessionStructure.copy()
        else:
            self.sessionStructure = session

    def getStructure(self):
        return self.sessionStructure

    def getAliceBaseKey(self):
        return self.sessionStructure.alice_base_key

    def setAliceBaseKey(self, alice_base_key):
        self.sessionStructure.alice_base_key = alice_base_key

    def setSessionVersion(self, version):
        self.sessionStructure.session_version = version

    def getSessionVersion(self):
        session_version = self.sessionStructure.session_version
        return 2 if session_version == 0 else session_version

    def setRemoteIdentityKey(self, identity_key):
        self.sessionStructure.remote_identity_public = identity_key.serialize()

    def setLocalIdentityKey(self, identity_key):
        self.sessionStructure.local_identity_public = identity_key.serialize()

    def getRemoteIdentityKey(self):
        if self.sessionStructure.remote_identity_public is None:
            return None
        return IdentityKey(self.sessionStructure.remote_identity_public, 0)

    def getLocalIdentityKey(self):
        return IdentityKey(self.sessionStructure.local_identity_public, 0)

    def getPreviousCounter(self):
        return self.sessionStructure.previous_counter

    def setPreviousCounter(self, previous_counter):
        self.sessionStructure.previous_counter = previous_counter

    def getRootKey(self):
        return RootKey(HKDF.createFor(self.getSessionVersion()), self.sessionStructure.root_key)

    def setRootKey(self, root_key):
        self.sessionStructure.root_key = root_key.getKeyBytes()

    def getSenderRatchetKey(self):
        return Curve.decodePoint(bytearray(self.sessionStructure.sender_chain.sender_ratchet_key), 0)

    def getSenderRatchetKeyPair(self):
        public_key = self.getSenderRatchetKey()
        private_key = Curve.decodePrivatePoint(self.sessionStructure.sender_chain.sender_ratchet_key_private)

        return ECKeyPair(public_key, private_key)

    def hasReceiverChain(self, ECPublickKey_senderEphemeral):
        return self.getReceiverChain(ECPublickKey_senderEphemeral) is not None

    def hasSenderChain(self):
        return self.sessionStructure.sender_chain is not None

    def getReceiverChain(self, ECPublickKey_senderEphemeral):
        receiver_chains = self.sessionStructure.receiver_chains
        index = 0
        for receiver_chain in receiver_chains:
            chain_sender_ratchet_key = Curve.decodePoint(bytearray(receiver_chain.sender_ratchet_key), 0)
            if chain_sender_ratchet_key == ECPublickKey_senderEphemeral:
                return receiver_chain, index

            index += 1

    def getReceiverChainKey(self, ECPublicKey_senderEphemeral):
        receiver_chain_and_index = self.getReceiverChain(ECPublicKey_senderEphemeral)
        receiver_chain = receiver_chain_and_index[0]
        if receiver_chain is None:
            return None

        return ChainKey(HKDF.createFor(self.getSessionVersion()),
                        receiver_chain.chain_key.key,
                        receiver_chain.chain_key.index)

    def addReceiverChain(self, ECPublickKey_senderRatchetKey, chainKey):
        senderRatchetKey = ECPublickKey_senderRatchetKey

        chain = storageprotos.SessionStructureChain()
        chain.sender_ratchet_key = senderRatchetKey.serialize()
        chain.chain_key = storageprotos.SessionStructureChainChainKey()
        chain.chain_key.key = chainKey.key
        chain.chain_key.index = chainKey.index

        self.sessionStructure.receiver_chains.extend([chain])

        if len(self.sessionStructure.receiver_chains) > 5:
            del self.sessionStructure.receiver_chains[0]

    def setSenderChain(self, ECKeyPair_senderRatchetKeyPair, chainKey):
        senderRatchetKeyPair = ECKeyPair_senderRatchetKeyPair

        self.sessionStructure.sender_chain.sender_ratchet_key = senderRatchetKeyPair.getPublicKey().serialize()
        self.sessionStructure.sender_chain.sender_ratchet_key_private = senderRatchetKeyPair.getPrivateKey().serialize()
        self.sessionStructure.sender_chain.chain_key.key = chainKey.key
        self.sessionStructure.sender_chain.chain_key.index = chainKey.index

    def getSenderChainKey(self):
        chainKeyStructure = self.sessionStructure.sender_chain.chain_key
        return ChainKey(HKDF.createFor(self.getSessionVersion()),
                        chainKeyStructure.key, chainKeyStructure.index)

    def setSenderChainKey(self, ChainKey_nextChainKey):
        nextChainKey = ChainKey_nextChainKey

        self.sessionStructure.sender_chain.chain_key.key = nextChainKey.getKey()
        self.sessionStructure.sender_chain.chain_key.index = nextChainKey.getIndex()

    def hasMessageKeys(self, ECPublickKey_senderEphemeral, counter):
        senderEphemeral = ECPublickKey_senderEphemeral
        chainAndIndex = self.getReceiverChain(senderEphemeral)
        chain = chainAndIndex[0]
        if chain is None:
            return False

        messageKeyList = chain.message_keys
        for messageKey in messageKeyList:
            if messageKey.index == counter:
                return True

        return False

    def removeMessageKeys(self, ECPublicKey_senderEphemeral, counter):
        senderEphemeral = ECPublicKey_senderEphemeral
        chainAndIndex = self.getReceiverChain(senderEphemeral)
        chain = chainAndIndex[0]
        if chain is None:
            return None

        messageKeyList = chain.message_keys
        result = None

        for i in range(0, len(messageKeyList)):
            messageKey = messageKeyList[i]
            if messageKey.index == counter:
                result = MessageKeys(messageKey.cipher_key, messageKey.mac_key, messageKey.iv, messageKey.index)
                del messageKeyList[i]
                break

        self.sessionStructure.receiver_chains[chainAndIndex[1]] = chain.copy()

        return result

    def setMessageKeys(self, ECPublicKey_senderEphemeral, messageKeys):
        senderEphemeral = ECPublicKey_senderEphemeral
        chainAndIndex = self.getReceiverChain(senderEphemeral)
        chain = chainAndIndex[0]
        messageKeyStructure = storageprotos.SessionStructureChainMessageKey()
        messageKeyStructure.cipher_key = messageKeys.getCipherKey()
        messageKeyStructure.mac_key = messageKeys.getMacKey()
        messageKeyStructure.index = messageKeys.getCounter()
        messageKeyStructure.iv = messageKeys.getIv()
        chain.message_keys.append(messageKeyStructure)

        self.sessionStructure.receiver_chains[chainAndIndex[1]] = chain.copy()

    def setReceiverChainKey(self, ECPublicKey_senderEphemeral, chainKey):
        senderEphemeral = ECPublicKey_senderEphemeral
        chainAndIndex = self.getReceiverChain(senderEphemeral)
        chain = chainAndIndex[0]
        chain.chain_key.key = chainKey.getKey()
        chain.chain_key.index = chainKey.getIndex()
        self.sessionStructure.receiver_chains[chainAndIndex[1]] = chain.copy()

    def setPendingKeyExchange(self, sequence, ourBaseKey, ourRatchetKey, ourIdentityKey):
        structure = storageprotos.SessionStructurePendingKeyExchange()
        structure.sequence = sequence
        structure.local_base_key = ourBaseKey.getPublicKey().serialize()
        structure.local_base_key_private = ourBaseKey.getPrivateKey().serialize()
        structure.local_ratchet_key = ourRatchetKey.getPublicKey().serialize()
        structure.local_ratchet_key_private = ourRatchetKey.getPrivateKey().serialize()
        structure.local_identity_key = ourIdentityKey.getPublicKey().serialize()
        structure.local_identity_key_private = ourIdentityKey.getPrivateKey().serialize()

        self.sessionStructure.pending_key_exchange = structure

    def getPendingKeyExchangeSequence(self):
        return self.sessionStructure.pending_key_exchange.sequence

    def getPendingKeyExchangeBaseKey(self):
        publicKey = Curve.decodePoint(bytearray(self.sessionStructure.pending_key_exchange.local_base_key), 0)
        privateKey = Curve.decodePrivatePoint(self.sessionStructure.pending_key_exchange.local_base_key_private)
        return ECKeyPair(publicKey, privateKey)

    def getPendingKeyExchangeRatchetKey(self):
        publicKey = Curve.decodePoint(bytearray(self.sessionStructure.pending_key_exchange.local_ratchet_key), 0)
        privateKey = Curve.decodePrivatePoint(self.sessionStructure.pending_key_exchange.local_ratchet_key_private)
        return ECKeyPair(publicKey, privateKey)

    def getPendingKeyExchangeIdentityKey(self):
        publicKey = IdentityKey(bytearray(self.sessionStructure.pending_key_exchange.local_identity_key), 0)

        privateKey = Curve.decodePrivatePoint(self.sessionStructure.pending_key_exchange.local_identity_key_private)
        return IdentityKeyPair(publicKey, privateKey)

    def hasPendingKeyExchange(self):
        return self.sessionStructure.pending_key_exchange is not None

    def setUnacknowledgedPreKeyMessage(self, preKeyId, signedPreKeyId, baseKey):
        self.sessionStructure.pending_pre_key = storageprotos.SessionStructurePendingPreKey()
        self.sessionStructure.pending_pre_key.signed_pre_key_id = signedPreKeyId
        self.sessionStructure.pending_pre_key.base_key = baseKey.serialize()

        if preKeyId is not None:
            self.sessionStructure.pending_pre_key.pre_key_id = preKeyId

    def hasUnacknowledgedPreKeyMessage(self):
        return self.sessionStructure.pending_pre_key is not None

    def getUnacknowledgedPreKeyMessageItems(self):
        preKeyId = None
        if self.sessionStructure.pending_pre_key.pre_key_id is not None:
            preKeyId = self.sessionStructure.pending_pre_key.pre_key_id

        return SessionState.UnacknowledgedPreKeyMessageItems(preKeyId,
                                                             self.sessionStructure.pending_pre_key.signed_pre_key_id,
                                                             Curve.decodePoint(bytearray(self.sessionStructure.pending_pre_key.base_key), 0))

    def clearUnacknowledgedPreKeyMessage(self):
        self.sessionStructure.pending_pre_key = None

    def setRemoteRegistrationId(self, registrationId):
        self.sessionStructure.remote_registration_id = registrationId

    def getRemoteRegistrationId(self):
        return self.sessionStructure.remote_registration_id

    def setLocalRegistrationId(self, registrationId):
        self.sessionStructure.local_registration_id = registrationId

    def getLocalRegistrationId(self):
        return self.sessionStructure.local_registration_id

    def serialize(self):
        return self.sessionStructure.__dict__()

    class UnacknowledgedPreKeyMessageItems:
        def __init__(self, preKeyId, signedPreKeyId, baseKey):
            self.preKeyId = preKeyId
            self.signedPreKeyId = signedPreKeyId
            self.baseKey = baseKey

        def getPreKeyId(self):
            return self.preKeyId

        def getSignedPreKeyId(self):
            return self.signedPreKeyId

        def getBaseKey(self):
            return self.baseKey
