import json

from .ciphertextmessage import CiphertextMessage
from security.util.enhancedJSONEncoder import EnhancedJSONEncoder
from ..util.byteutil import ByteUtil
from security.exceptions.legacymessageexception import LegacyMessageException
from security.exceptions.invalidmessageexception import InvalidMessageException
from security.exceptions.invalidkeyexception import InvalidKeyException
from ..ecc.curve import Curve
from . import whisper_proto_types as whisperprotos


class SenderKeyMessage(CiphertextMessage):
    SIGNATURE_LENGTH = 64

    def __init__(self, keyId=None, iteration=None, ciphertext=None, signatureKey=None, serialized=None):
        assert bool(keyId is not None and iteration is not None and ciphertext is not None and
                    signatureKey is not None) ^ bool(serialized), "Either pass arguments or serialized data"

        if serialized:
            try:
                messageParts = ByteUtil.split(serialized, 1, len(serialized) - 1 - self.__class__.SIGNATURE_LENGTH,
                                              self.__class__.SIGNATURE_LENGTH)

                version = messageParts[0][0]
                message = messageParts[1]
                signature = messageParts[2]

                if ByteUtil.highBitsToInt(version) < 3:
                    raise LegacyMessageException("Legacy message: %s" % ByteUtil.highBitsToInt(version))

                if ByteUtil.highBitsToInt(version) > self.__class__.CURRENT_VERSION:
                    raise InvalidMessageException("Unknown version: %s" % ByteUtil.highBitsToInt(version))

                if type(message) == bytes:
                    message = message.decode("utf-8")
                data = json.loads(message)
                senderKeyMessage = whisperprotos.SenderKeyMessage(**data)

                if senderKeyMessage.id is None or senderKeyMessage.iteration is None or \
                        senderKeyMessage.ciphertext is None:
                    raise InvalidMessageException("Incomplete message")

                self.serialized = serialized
                self.messageVersion = ByteUtil.highBitsToInt(version)

                self.keyId = senderKeyMessage.id
                self.iteration = senderKeyMessage.iteration
                self.ciphertext = senderKeyMessage.ciphertext
            except Exception as e:
                raise InvalidMessageException(e)
        else:
            version = [ByteUtil.intsToByteHighAndLow(self.__class__.CURRENT_VERSION, self.__class__.CURRENT_VERSION)]

            message = whisperprotos.SenderKeyMessage()
            message.id = keyId
            message.iteration = iteration
            message.ciphertext = ciphertext
            message = json.dumps(message, cls=EnhancedJSONEncoder)

            signature = self.getSignature(signatureKey, ByteUtil.combine(version, bytes(message, 'utf-8')))

            self.serialized = bytes(ByteUtil.combine(version, bytes(message, 'utf-8'), signature))
            self.messageVersion = self.__class__.CURRENT_VERSION
            self.keyId = keyId
            self.iteration = iteration
            self.ciphertext = ciphertext


    def getKeyId(self):
        return self.keyId

    def getIteration(self):
        return self.iteration

    def getCipherText(self):
        return self.ciphertext

    def verifySignature(self, signatureKey):
        try:
            parts = ByteUtil.split(self.serialized,
                                   len(self.serialized) - self.__class__.SIGNATURE_LENGTH,
                                   self.__class__.SIGNATURE_LENGTH)

            if not Curve.verifySignature(signatureKey, parts[0], parts[1]):
                raise InvalidMessageException("Invalid signature!")
        except InvalidKeyException as e:
            raise InvalidMessageException(e)

    def getSignature(self, signatureKey, serialized):
        try:
            return Curve.calculateSignature(signatureKey, serialized)
        except InvalidKeyException as e:
            raise AssertionError(e)

    def serialize(self):
        return self.serialized

    def getType(self):
        return CiphertextMessage.SENDERKEY_TYPE
