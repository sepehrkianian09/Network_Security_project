from security.state.identitykeystore import IdentityKeyStore
from security.ecc.curve import Curve
from security.identitykey import IdentityKey
from security.util.keyhelper import KeyHelper
from security.identitykeypair import IdentityKeyPair


class InMemoryIdentityKeyStore(IdentityKeyStore):
    def __init__(self):
        self.trustedKeys = {}
        identityKeyPairKeys = Curve.generateKeyPair()
        self.identityKeyPair = IdentityKeyPair(IdentityKey(identityKeyPairKeys.getPublicKey()),
                                               identityKeyPairKeys.getPrivateKey())
        self.localRegistrationId = KeyHelper.generateRegistrationId()

    def getIdentityKeyPair(self):
        return self.identityKeyPair

    def getLocalRegistrationId(self):
        return self.localRegistrationId

    def saveIdentity(self, recepientId, identityKey):
        self.trustedKeys[recepientId] = identityKey

    def isTrustedIdentity(self, recepientId, identityKey):
        if recepientId not in self.trustedKeys:
            return True
        return self.trustedKeys[recepientId] == identityKey
