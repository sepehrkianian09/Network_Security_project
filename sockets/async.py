from sockets.interfaces import ConcurrentSocket, DecoratorSocket, MessageListener


class AsyncSocket(DecoratorSocket, ConcurrentSocket):
    def start_broadcasting_received_messages(self, listener: MessageListener):
        return super().start_broadcasting_received_messages(listener)