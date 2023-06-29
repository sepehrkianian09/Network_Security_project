from .client import Client
from ..key_holder import SecureKeyHolder
from message_passing.message_receiver import SecureMessageReceiver
from message_passing.message_sender import SecureMessageSender
from handshaking.client import HandShaker
from ..sockets.interfaces import create_socket


def main():
    socket = create_socket()
    key_holder = SecureKeyHolder()
    handshaker = HandShaker(socket, key_holder)
    handshaker.start_handshaking()
    message_sender = SecureMessageSender(socket, key_holder)
    message_receiver = SecureMessageReceiver(socket, key_holder)
    client = Client(message_sender=message_sender, message_receiver=message_receiver)
    client.run()
