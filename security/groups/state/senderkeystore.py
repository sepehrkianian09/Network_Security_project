import abc


class SenderKeyStore(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def storeSenderKey(self, senderKeyId, senderKeyRecord):
        pass

    @abc.abstractmethod
    def loadSenderKey(self, senderKeyId):
        pass
