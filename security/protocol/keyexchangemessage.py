import json

from .ciphertextmessage import CiphertextMessage
from security.util.enhancedJSONEncoder import EnhancedJSONEncoder
from ..util.byteutil import ByteUtil
from . import whisper_proto_types as whisperprotos
from security.exceptions.legacymessageexception import LegacyMessageException
from security.exceptions.invalidversionexception import InvalidVersionException
from security.exceptions.invalidmessageexception import InvalidMessageException
from security.exceptions.invalidkeyexception import InvalidKeyException
from ..ecc.curve import Curve
from ..identitykey import IdentityKey


class KeyExchangeMessage:
    INITIATE_FLAG = 0x01
    RESPONSE_FLAG = 0X02
    SIMULTANEOUS_INITIATE_FLAG = 0x04

    def __init__(self, messageVersion=None, sequence=None, flags=None, baseKey=None,
                 baseKeySignature=None, ratchetKey=None, identityKey=None, serialized=None):

        if serialized:
            try:
                parts = ByteUtil.split(serialized, 1, len(serialized) - 1)
                self.version = ByteUtil.highBitsToInt(parts[0][0])
                self.supportedVersion = ByteUtil.lowBitsToInt(parts[0][0])
                if self.version < CiphertextMessage.CURRENT_VERSION:
                    raise LegacyMessageException("Unsupportmessageed legacy version: %s" % self.version)
                if self.version > CiphertextMessage.CURRENT_VERSION:
                    raise InvalidVersionException("Unkown version: %s" % self.version)

                m = bytes(parts[1])
                if type(m) == bytes:
                    m = m.decode("utf-8")
                data = json.loads(m)
                message = whisperprotos.KeyExchangeMessage(**data)

                if (not message.id or not message.base_key or
                        not message.ratchet_key or not message.identity_key or
                        not message.base_key_signature):
                    raise InvalidMessageException("Some required fields are missing!")

                self.sequence = message.id >> 5
                self.flags = message.id & 0x1f
                self.serialized = serialized
                self.baseKey = Curve.decodePoint(bytearray(message.base_key), 0)
                self.baseKeySignature = message.base_key_signature
                self.ratchetKey = Curve.decodePoint(bytearray(message.ratchet_key), 0)
                self.identityKey = IdentityKey(message.identity_key, 0)

            except InvalidKeyException as e:
                raise InvalidMessageException(e)
        else:
            self.supportedVersion = CiphertextMessage.CURRENT_VERSION
            self.version = messageVersion
            self.sequence = sequence
            self.flags = flags
            self.baseKey = baseKey
            self.baseKeySignature = baseKeySignature
            self.ratchetKey = ratchetKey
            self.identityKey = identityKey

            version = [ByteUtil.intsToByteHighAndLow(self.version, self.supportedVersion)]
            keyExchangeMessage = whisperprotos.KeyExchangeMessage()
            keyExchangeMessage.id = (self.sequence << 5) | self.flags
            keyExchangeMessage.base_key = baseKey.serialize()
            keyExchangeMessage.ratchet_key = ratchetKey.serialize()
            keyExchangeMessage.identity_key = identityKey.serialize()

            if messageVersion >= 3:
                keyExchangeMessage.base_key_signature = baseKeySignature

            self.serialized = ByteUtil.combine(version, bytes(json.dumps(keyExchangeMessage, cls=EnhancedJSONEncoder), 'utf-8'))

    def getVersion(self):
        return self.version

    def getBaseKey(self):
        return self.baseKey

    def getBaseKeySignature(self):
        return self.baseKeySignature

    def getRatchetKey(self):
        return self.ratchetKey

    def getIdentityKey(self):
        return self.identityKey

    def hasIdentityKey(self):
        return True

    def getMaxVersion(self):
        return self.supportedVersion

    def isResponse(self):
        return ((self.flags & self.__class__.RESPONSE_FLAG) != 0)

    def isInitiate(self):
        return (self.flags & self.__class__.INITIATE_FLAG) != 0

    def isResponseForSimultaneousInitiate(self):
        return (self.flags & self.__class__.SIMULTANEOUS_INITIATE_FLAG) != 0

    def getFlags(self):
        return self.flags

    def getSequence(self):
        return self.sequence

    def serialize(self):
        return self.serialized
