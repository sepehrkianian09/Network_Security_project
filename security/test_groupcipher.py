import unittest

from .inmemorysenderkeystore import InMemorySenderKeyStore
from security.groups.groupsessionbuilder import GroupSessionBuilder
from security.util.keyhelper import KeyHelper
from security.groups.groupcipher import GroupCipher
from security.exceptions.duplicatemessagexception import DuplicateMessageException
from security.exceptions.nosessionexception import NoSessionException
from security.groups.senderkeyname import SenderKeyName
from security.protocoladdress import ProtocolAddress
from security.protocol.senderkeydistributionmessage import SenderKeyDistributionMessage

SENDER_ADDRESS = ProtocolAddress("myuser", 1)
GROUP_SENDER = SenderKeyName("test group", SENDER_ADDRESS)


class GroupCipherTest(unittest.TestCase):

    def test_noSession(self):
        aliceStore = InMemorySenderKeyStore()
        bobStore = InMemorySenderKeyStore()

        aliceSessionBuilder = GroupSessionBuilder(aliceStore)
        bobSessionBuilder   = GroupSessionBuilder(bobStore)

        aliceGroupCipher = GroupCipher(aliceStore, GROUP_SENDER)
        bobGroupCipher = GroupCipher(bobStore, GROUP_SENDER)

        sentAliceDistributionMessage = aliceSessionBuilder.create(GROUP_SENDER)
        receivedAliceDistributionMessage = SenderKeyDistributionMessage(serialized=sentAliceDistributionMessage.serialize())

        ciphertextFromAlice = aliceGroupCipher.encrypt(b"salam khobi?")

        try:
            plaintextFromAlice = bobGroupCipher.decrypt(ciphertextFromAlice)
            raise AssertionError("Should be no session!")
        except NoSessionException as e:
            pass

    def test_basicEncryptDecrypt(self):
        aliceStore = InMemorySenderKeyStore()
        bobStore = InMemorySenderKeyStore()

        aliceSessionBuilder = GroupSessionBuilder(aliceStore)
        bobSessionBuilder = GroupSessionBuilder(bobStore)

        aliceGroupCipher = GroupCipher(aliceStore, GROUP_SENDER)
        bobGroupCipher = GroupCipher(bobStore, GROUP_SENDER)

        sentAliceDistributionMessage = aliceSessionBuilder.create(GROUP_SENDER)
        receivedAliceDistributionMessage = SenderKeyDistributionMessage(serialized=sentAliceDistributionMessage.serialize())

        bobSessionBuilder.process(GROUP_SENDER, receivedAliceDistributionMessage)

        ciphertextFromAlice = aliceGroupCipher.encrypt(b"salam khobi?")
        plaintextFromAlice = bobGroupCipher.decrypt(ciphertextFromAlice)

        self.assertEqual(plaintextFromAlice, b"salam khobi?")

    def test_basicRatchet(self):
        aliceStore = InMemorySenderKeyStore()
        bobStore = InMemorySenderKeyStore()

        aliceSessionBuilder = GroupSessionBuilder(aliceStore)
        bobSessionBuilder = GroupSessionBuilder(bobStore)

        aliceGroupCipher = GroupCipher(aliceStore, "groupWithBobInIt")
        bobGroupCipher   = GroupCipher(bobStore, "groupWithBobInIt::aliceUserName")

        aliceGroupCipher = GroupCipher(aliceStore, GROUP_SENDER)
        bobGroupCipher   = GroupCipher(bobStore, GROUP_SENDER)

        sentAliceDistributionMessage = aliceSessionBuilder.create(GROUP_SENDER)
        receivedAliceDistributionMessage = SenderKeyDistributionMessage(serialized=sentAliceDistributionMessage.serialize())

        bobSessionBuilder.process(GROUP_SENDER, receivedAliceDistributionMessage)

        ciphertextFromAlice  = aliceGroupCipher.encrypt(b"alo")
        ciphertextFromAlice2 = aliceGroupCipher.encrypt(b"alo 2")
        ciphertextFromAlice3 = aliceGroupCipher.encrypt(b"alo 3")

        plaintextFromAlice = bobGroupCipher.decrypt(ciphertextFromAlice)

        try:
            bobGroupCipher.decrypt(ciphertextFromAlice)
            raise AssertionError("Should have ratcheted forward!")
        except DuplicateMessageException as dme:
            # good
            pass

        plaintextFromAlice2 = bobGroupCipher.decrypt(ciphertextFromAlice2)
        plaintextFromAlice3 = bobGroupCipher.decrypt(ciphertextFromAlice3)

        self.assertEqual(plaintextFromAlice, b"alo")
        self.assertEqual(plaintextFromAlice2, b"alo 2")
        self.assertEqual(plaintextFromAlice3, b"alo 3")

    def test_outOfOrder(self):
        aliceStore = InMemorySenderKeyStore()
        bobStore   = InMemorySenderKeyStore()

        aliceSessionBuilder = GroupSessionBuilder(aliceStore)
        bobSessionBuilder   = GroupSessionBuilder(bobStore)

        aliceGroupCipher = GroupCipher(aliceStore, "groupWithBobInIt")
        bobGroupCipher   = GroupCipher(bobStore, "groupWithBobInIt::aliceUserName")

        aliceGroupCipher = GroupCipher(aliceStore, GROUP_SENDER)
        bobGroupCipher = GroupCipher(bobStore, GROUP_SENDER)

        sentAliceDistributionMessage = aliceSessionBuilder.create(GROUP_SENDER)
        receivedAliceDistributionMessage = SenderKeyDistributionMessage(serialized=sentAliceDistributionMessage.serialize())

        bobSessionBuilder.process(GROUP_SENDER, receivedAliceDistributionMessage)

        ciphertexts = []
        for i in range(0, 100):
            ciphertexts.append(aliceGroupCipher.encrypt(b"ok doroste"))
        while len(ciphertexts) > 0:
            index = KeyHelper.getRandomSequence(2147483647) % len(ciphertexts)
            ciphertext = ciphertexts.pop(index)
            plaintext = bobGroupCipher.decrypt(ciphertext)
            self.assertEqual(plaintext, b"ok doroste")
