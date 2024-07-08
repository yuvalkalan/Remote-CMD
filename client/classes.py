import socket
import protocol
from .constants import *


class Client(protocol.ConnectionProtocol):
    def __init__(self, code, password):
        super(Client, self).__init__()
        self._server_ip, self._port = protocol.decode_address(code)
        self._server_ip += protocol.NGROK_URL_ENDING
        self._password = password
        self._frame = None
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._running = False

    @property
    def running(self):
        return self._running

    @running.setter
    def running(self, other):
        self._running = other

    def start(self):
        self._socket.connect((self._server_ip, self._port))
        self.send(protocol.ClientCodes.SET_PASSWORD, self._password)
        self._running = True

    def stop(self):
        self._running = False
