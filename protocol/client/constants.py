from enum import Enum, auto


class Codes(Enum):
    SERVER_CONN_QUIT = auto()
    SEND_COMMAND = auto()
    SET_PASSWORD = auto()
