import json

from . import whisper_proto_types as whisperprotos
from .ciphertextmessage import CiphertextMessage
from ..ecc.curve import Curve
from security.util.enhancedJSONEncoder import EnhancedJSONEncoder
from security.exceptions.invalidmessageexception import InvalidMessageException
from security.exceptions.legacymessageexception import LegacyMessageException
from ..util.byteutil import ByteUtil


class SenderKeyDistributionMessage(CiphertextMessage):
    def __init__(self, id=None, iteration=None, chainKey=None, signatureKey=None, serialized=None):

        assert bool(id is not None and iteration is not None and chainKey is not None and signatureKey is not None) \
               ^ bool(serialized), "Either pass arguments or serialized data"

        if serialized:
            try:
                messageParts = ByteUtil.split(serialized, 1, len(serialized) - 1)
                version = messageParts[0][0]
                message = messageParts[1]

                if ByteUtil.highBitsToInt(version) < 3:
                    raise LegacyMessageException("Legacy message: %s" % ByteUtil.highBitsToInt(version))

                if ByteUtil.highBitsToInt(version) > self.__class__.CURRENT_VERSION:
                    raise InvalidMessageException("Unknown version: %s" % ByteUtil.highBitsToInt(version))

                if type(message) == bytes:
                    message = message.decode("utf-8")
                data = json.loads(message)
                distributionMessage = whisperprotos.SenderKeyDistributionMessage(**data)

                if distributionMessage.id is None or distributionMessage.iteration is None \
                        or distributionMessage.chain_key is None or distributionMessage.signing_key is None:
                    raise InvalidMessageException("Incomplete message")

                self.serialized = serialized

                self.id = distributionMessage.id
                self.iteration = distributionMessage.iteration
                self.chainKey = distributionMessage.chain_key
                self.signatureKey = Curve.decodePoint(bytearray(distributionMessage.signing_key), 0)

            except Exception as e:
                raise InvalidMessageException(e)
        else:
            version = [ByteUtil.intsToByteHighAndLow(self.__class__.CURRENT_VERSION, self.__class__.CURRENT_VERSION)]
            self.id = id
            self.iteration = iteration
            self.chainKey = chainKey
            self.signatureKey = signatureKey
            message = whisperprotos.SenderKeyDistributionMessage()
            message.id = id
            message.iteration = iteration
            message.chain_key = bytes(chainKey)
            message.signing_key = signatureKey.serialize()
            message = json.dumps(message, cls=EnhancedJSONEncoder)
            self.serialized = bytes(ByteUtil.combine(version, bytes(message, 'utf-8')))

    def serialize(self):
        return self.serialized

    def getType(self):
        return self.__class__.SENDERKEY_DISTRIBUTION_TYPE

    def getIteration(self):
        return self.iteration

    def getChainKey(self):
        return self.chainKey

    def getSignatureKey(self):
        return self.signatureKey

    def getId(self):
        return self.id
