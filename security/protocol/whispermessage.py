import hmac
import hashlib
import json

from .ciphertextmessage import CiphertextMessage
from security.util.enhancedJSONEncoder import EnhancedJSONEncoder
from ..util.byteutil import ByteUtil
from ..ecc.curve import Curve
from . import whisper_proto_types as whisperprotos
from security.exceptions.legacymessageexception import LegacyMessageException
from security.exceptions.invalidmessageexception import InvalidMessageException
from security.exceptions.invalidkeyexception import InvalidKeyException


class WhisperMessage(CiphertextMessage):
    MAC_LENGTH = 8

    def __init__(self, messageVersion=None, macKey=None, ECPublicKey_senderRatchetKey=None,
                 counter=None, previousCounter=None, ciphertext=None, senderIdentityKey=None,
                 receiverIdentityKey=None, serialized=None):
        self.serialized = ""
        if serialized:
            try:
                assert type(serialized) in (str, bytes), "Expected serialized %s, got %s" % (str, type(serialized))
                messageParts = ByteUtil.split(serialized, 1, len(serialized) - 1 - WhisperMessage.MAC_LENGTH,
                                              WhisperMessage.MAC_LENGTH)
                version = messageParts[0][0]
                message = messageParts[1]
                mac = messageParts[2]

                if ByteUtil.highBitsToInt(version) <= self.__class__.UNSUPPORTED_VERSION:
                    raise LegacyMessageException("Legacy message %s" % ByteUtil.highBitsToInt(version))

                if ByteUtil.highBitsToInt(version) > self.__class__.CURRENT_VERSION:
                    raise InvalidMessageException("Unknown version: %s" % ByteUtil.highBitsToInt(version))

                if type(message) == bytes:
                    message = message.decode("utf-8")
                data = json.loads(message)
                whisperMessage = whisperprotos.WhisperMessage(**data)

                if not whisperMessage.ciphertext or whisperMessage.counter is None or not whisperMessage.ratchet_key:
                    raise InvalidMessageException("Incomplete message")

                self.serialized = serialized
                self.senderRatchetKey = Curve.decodePoint(bytearray(whisperMessage.ratchet_key), 0)
                self.messageVersion = ByteUtil.highBitsToInt(version)
                self.counter = whisperMessage.counter
                self.previousCounter = whisperMessage.previous_counter
                self.ciphertext = whisperMessage.ciphertext
            except InvalidKeyException as e:
                raise InvalidMessageException(e)
        else:
            version = ByteUtil.intsToByteHighAndLow(messageVersion, self.__class__.CURRENT_VERSION)
            message = whisperprotos.WhisperMessage()
            message.ratchet_key = ECPublicKey_senderRatchetKey.serialize()
            message.counter = counter
            message.previous_counter = previousCounter
            message.ciphertext = ciphertext
            message = json.dumps(message, cls=EnhancedJSONEncoder)
            mac = self.getMac(messageVersion, senderIdentityKey, receiverIdentityKey, macKey,
                              ByteUtil.combine(version, bytes(message, 'utf-8')))
            self.serialized = bytes(ByteUtil.combine(version, bytes(message, 'utf-8'), mac))
            self.senderRatchetKey = ECPublicKey_senderRatchetKey
            self.counter = counter
            self.previousCounter = previousCounter
            self.ciphertext = ciphertext
            self.messageVersion = messageVersion

    def getSenderRatchetKey(self):
        return self.senderRatchetKey

    def getMessageVersion(self):
        return self.messageVersion

    def getCounter(self):
        return self.counter

    def getBody(self):
        return self.ciphertext

    def verifyMac(self, messageVersion, senderIdentityKey, receiverIdentityKey, macKey):
        parts = ByteUtil.split(self.serialized,
                               len(self.serialized) - self.__class__.MAC_LENGTH,
                               self.__class__.MAC_LENGTH)
        ourMac = self.getMac(messageVersion, senderIdentityKey, receiverIdentityKey, macKey, parts[0])
        theirMac = parts[1]

        if ourMac != theirMac:
            raise InvalidMessageException("Bad Mac!")

    def getMac(self, messageVersion, senderIdentityKey, receiverIdentityKey, macKey, serialized):
        mac = hmac.new(macKey, digestmod=hashlib.sha256)
        if messageVersion >= 3:
            mac.update(senderIdentityKey.getPublicKey().serialize())
            mac.update(receiverIdentityKey.getPublicKey().serialize())

        mac.update(bytes(serialized))
        fullMac = mac.digest()
        return ByteUtil.trim(fullMac, self.__class__.MAC_LENGTH)

    def serialize(self):
        return self.serialized

    def getType(self):
        return CiphertextMessage.WHISPER_TYPE

    def isLegacy(self, message):
        return message is not None and \
                len(message) >= 1 and \
                ByteUtil.highBitsToInt(message[0]) <= CiphertextMessage.UNSUPPORTED_VERSION
