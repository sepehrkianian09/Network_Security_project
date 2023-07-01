from security.exceptions.invalidkeyidexception import InvalidKeyIdException
from security.exceptions.invalidkeyexception import InvalidKeyException
from security.exceptions.invalidmessageexception import InvalidMessageException
from security.exceptions.duplicatemessagexception import DuplicateMessageException
from security.exceptions.nosessionexception import NoSessionException
from ..protocol.senderkeymessage import SenderKeyMessage
from ..sessioncipher import AESCipher


class GroupCipher:
    def __init__(self, senderKeyStore, senderKeyName):
        self.senderKeyStore = senderKeyStore
        self.senderKeyName = senderKeyName

    def encrypt(self, paddedPlaintext):
        try:
            record = self.senderKeyStore.loadSenderKey(self.senderKeyName)
            senderKeyState = record.getSenderKeyState()
            senderKey = senderKeyState.getSenderChainKey().getSenderMessageKey()
            ciphertext = self.getCipherText(senderKey.getIv(), senderKey.getCipherKey(), bytearray(paddedPlaintext))

            senderKeyMessage = SenderKeyMessage(senderKeyState.getKeyId(),
                                                senderKey.getIteration(),
                                                ciphertext,
                                                senderKeyState.getSigningKeyPrivate())

            senderKeyState.setSenderChainKey(senderKeyState.getSenderChainKey().getNext())
            self.senderKeyStore.storeSenderKey(self.senderKeyName, record)

            return senderKeyMessage.serialize()
        except InvalidKeyIdException as e:
            raise NoSessionException(e)

    def decrypt(self, senderKeyMessageBytes):
        try:
            record = self.senderKeyStore.loadSenderKey(self.senderKeyName)
            if record.isEmpty():
                raise NoSessionException("No sender key for: %s" % self.senderKeyName)
            senderKeyMessage = SenderKeyMessage(serialized = bytes(senderKeyMessageBytes))
            senderKeyState = record.getSenderKeyState(senderKeyMessage.getKeyId())

            senderKeyMessage.verifySignature(senderKeyState.getSigningKeyPublic())

            senderKey = self.getSenderKey(senderKeyState, senderKeyMessage.getIteration())

            plaintext = self.getPlainText(senderKey.getIv(), senderKey.getCipherKey(), senderKeyMessage.getCipherText())

            self.senderKeyStore.storeSenderKey(self.senderKeyName, record)

            return plaintext
        except (InvalidKeyException, InvalidKeyIdException) as e:
            raise InvalidMessageException(e)

    def getSenderKey(self, senderKeyState, iteration):
        senderChainKey = senderKeyState.getSenderChainKey()

        if senderChainKey.getIteration() > iteration:
            if senderKeyState.hasSenderMessageKey(iteration):
                return senderKeyState.removeSenderMessageKey(iteration)
            else:
                raise DuplicateMessageException("Received message with old counter: %s, %s" %
                                                (senderChainKey.getIteration(), iteration))

        if senderChainKey.getIteration() - iteration > 2000:
            raise InvalidMessageException("Over 2000 messages into the future!")

        while senderChainKey.getIteration() < iteration:
            senderKeyState.addSenderMessageKey(senderChainKey.getSenderMessageKey())
            senderChainKey = senderChainKey.getNext()

        senderKeyState.setSenderChainKey(senderChainKey.getNext())
        return senderChainKey.getSenderMessageKey()

    def getPlainText(self, iv, key, ciphertext):
        try:
            cipher = AESCipher(key, iv)
            plaintext = cipher.decrypt(ciphertext)
            return plaintext
        except Exception as e:
            raise InvalidMessageException(e)

    def getCipherText(self, iv, key, plaintext):
        cipher = AESCipher(key, iv)
        return cipher.encrypt(plaintext)
