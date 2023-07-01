import json

from . import whisper_proto_types as whisperprotos
from .ciphertextmessage import CiphertextMessage
from .whispermessage import WhisperMessage
from ..ecc.curve import Curve
from security.util.enhancedJSONEncoder import EnhancedJSONEncoder
from ..identitykey import IdentityKey
from security.exceptions.invalidkeyexception import InvalidKeyException
from security.exceptions.invalidmessageexception import InvalidMessageException
from security.exceptions.invalidversionexception import InvalidVersionException
from security.exceptions.legacymessageexception import LegacyMessageException
from ..util.byteutil import ByteUtil


class PreKeyWhisperMessage(CiphertextMessage):
    def __init__(self, messageVersion=None, registrationId=None, preKeyId=None,
                 signedPreKeyId=None, ecPublicBaseKey=None, identityKey=None,
                 whisperMessage=None, serialized=None):
        if serialized:
            try:
                self.version = ByteUtil.highBitsToInt(serialized[0])
                if self.version > CiphertextMessage.CURRENT_VERSION:
                    raise InvalidVersionException("Unknown version %s" % self.version)

                if self.version < CiphertextMessage.CURRENT_VERSION:
                    raise LegacyMessageException("Legacy version: %s" % self.version)

                message = serialized[1:]
                if type(message) == bytes:
                    message = message.decode("utf-8")
                data = json.loads(message)
                preKeyWhisperMessage = whisperprotos.PreKeyWhisperMessage(**data)

                if preKeyWhisperMessage.signed_pre_key_id is None or \
                        not preKeyWhisperMessage.base_key or \
                        not preKeyWhisperMessage.identity_key or \
                        not preKeyWhisperMessage.message:
                    raise InvalidMessageException("Incomplete message")

                self.serialized = serialized
                self.registrationId = preKeyWhisperMessage.registration_id
                self.preKeyId = preKeyWhisperMessage.pre_key_id
                if preKeyWhisperMessage.signed_pre_key_id is not None:
                    self.signedPreKeyId = preKeyWhisperMessage.signed_pre_key_id
                else:
                    self.signedPreKeyId = -1

                self.baseKey = Curve.decodePoint(bytearray(preKeyWhisperMessage.base_key), 0)

                self.identityKey = IdentityKey(Curve.decodePoint(bytearray(preKeyWhisperMessage.identity_key), 0))
                self.message = WhisperMessage(serialized=preKeyWhisperMessage.message)
            except (InvalidKeyException, LegacyMessageException) as e:
                raise InvalidMessageException(e)

        else:
            self.version = messageVersion
            self.registrationId = registrationId
            self.preKeyId = preKeyId
            self.signedPreKeyId = signedPreKeyId
            self.baseKey = ecPublicBaseKey
            self.identityKey = identityKey
            self.message = whisperMessage

            builder = whisperprotos.PreKeyWhisperMessage()
            builder.signed_pre_key_id = signedPreKeyId
            builder.base_key = ecPublicBaseKey.serialize()
            builder.identity_key = identityKey.serialize()
            builder.message = whisperMessage.serialize()
            builder.registration_id = registrationId

            if preKeyId is not None:
                builder.pre_key_id = preKeyId

            versionBytes = ByteUtil.intsToByteHighAndLow(self.version, self.__class__.CURRENT_VERSION)
            messageBytes = json.dumps(builder, cls=EnhancedJSONEncoder)
            self.serialized = bytes(ByteUtil.combine(versionBytes, bytes(messageBytes, 'utf-8')))

    def getMessageVersion(self):
        return self.version

    def getIdentityKey(self):
        return self.identityKey

    def getRegistrationId(self):
        return self.registrationId

    def getPreKeyId(self):
        return self.preKeyId

    def getSignedPreKeyId(self):
        return self.signedPreKeyId

    def getBaseKey(self):
        return self.baseKey

    def getWhisperMessage(self):
        return self.message

    def serialize(self):
        return self.serialized

    def getType(self):
        return CiphertextMessage.PREKEY_TYPE
