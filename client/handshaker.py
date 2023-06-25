from client.key_holder import KeyHolder


class HandShaker:
    def __init__(self, socket, key_holder: KeyHolder) -> None:
        self.__socket = socket
        self.__key_holder = key_holder

    def start_handshaking(self):
        pass
