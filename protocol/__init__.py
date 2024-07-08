import math
import socket
from typing import *
import pickle
import select
from .constants import *


class ConnectionProtocol:
    def __init__(self):
        self._socket: Optional[socket.socket] = None

    def _get_length_of_msg(self):
        try:
            received = self._socket.recv(DATA_LENGTH)
            if received == b'':
                return 0
            return int.from_bytes(received, 'little')
        except Exception as e:
            print(f'cant get length! {e}')
            return 0

    def send(self, key, value=None):
        try:
            data = key + pickle.dumps(value)
            length = len(data).to_bytes(DATA_LENGTH, 'little')
            self._socket.sendall(length + data)
        except Exception as e:
            print(f'cant send! {e}')

    def receive(self):
        try:
            length = self._get_length_of_msg()
            if length == 0:
                return CONN_QUIT, None
            data = self._socket.recv(length)
            while len(data) < length:
                data += self._socket.recv(length - len(data))
            key, value = data[:KEY_SIZE], data[KEY_SIZE:length]
            value = pickle.loads(value)
            return key, value
        except Exception as e:
            print(f'cant receive! {e}')
            return CONN_QUIT, None

    def have_data(self):
        r, _, _ = select.select([self._socket], [], [], 0)
        return self._socket in r


def encode_address(address: Tuple[str, int]) -> str:
    """
    address --> code
    :param address: כתובת רשת (אי-די ופורט)
    :return: קוד אי-די ופורט בבסיס 36
    """
    def encode_id(ngrok_id):
        id_decimal = sum([ord(ngrok_id[i]) * (256 ** (len(ngrok_id) - i - 1)) for i in range(len(ngrok_id))])
        # הפיכת המספר הדצימלי למספר בבסיס 36
        code = ''
        while id_decimal != 0:
            code = chr(id_decimal % 36 + (ord('0') if id_decimal % 36 < 10 else ord('a') - 10)) + code
            id_decimal //= 36
        return code

    def encode_port(port):
        code = ''
        while port != 0:
            code = chr(port % 36 + (ord('0') if port % 36 < 10 else ord('a') - 10)) + code
            port //= 36
        return code

    # הפיכת קוד האי-פי למספר דצימלי
    server_id, server_port = address
    server_id = encode_id(server_id)
    server_port = encode_port(server_port)
    return f'{server_id}:{server_port}'


def decode_address(code: str) -> Tuple[str, int]:
    """
    decoding address (code --> address)
    :param code: קוד השרת בבסיס 36
    :return: כתובת אי-פי של השרת
    """

    def char_value(char: str) -> int:
        """
        ממיר תו מבסיס 36 למספר דצימלי
        convert char --> base36(char)
        :param char: תו להמיר
        :return: ערך מספרי של התו לפי בסיס 36
        """
        char = char.lower()
        return ord(char) - (ord('0') if ord('0') <= ord(char) <= ord('9') else ord('a') - 10)

    def decode_ip(id_code: str) -> str:
        number = sum([char_value(id_code[i]) * (36 ** (len(id_code) - i - 1)) for i in range(len(id_code))])
        # ממיר מבסיס 10 אל מחרוזת
        number_bytes = number.to_bytes(math.ceil(number.bit_length()/8), 'big', signed=False)
        return ''.join([chr(item) for item in number_bytes])

    def decode_port(port_code: str) -> int:
        return sum([char_value(port_code[i]) * (36 ** (len(port_code) - i - 1)) for i in range(len(port_code))])

    server_id, server_port = code.split(':')
    return decode_ip(server_id), decode_port(server_port)
