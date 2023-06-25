from client.message_receiver import MessageListener, MessageReceiver
from client.message_sender import MessageSender


class Client(MessageListener):
    def __init__(
        self, message_sender: MessageSender, message_receiver: MessageReceiver
    ) -> None:
        self.__message_sender = message_sender
        message_receiver.start_broadcasting_received_messages(self)

    def listen(self, message):
        pass

    def run(self):
        pass
