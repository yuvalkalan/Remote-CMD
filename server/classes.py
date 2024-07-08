import socket
import time
from typing import *
import select
from pyngrok import ngrok
import protocol
from .log import log


class Server:
    def __init__(self):
        self._running = False
        self._tunnel = None
        self._create_ngrok_tunnel()
        self._server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server_socket.bind(('0.0.0.0', protocol.PORT))
        self._server_socket.listen()
        self._clients: List[ServerConnection] = []
        self._frame = None

    def _create_ngrok_tunnel(self):
        i = 1
        while not self._tunnel:
            try:
                log.append('init ngrok...')
                self._tunnel = ngrok.connect(protocol.PORT, "tcp")
            except ngrok.PyngrokError:
                log.append(f'cannot start ngrok... retrying ({i})')
                i += 1
                time.sleep(1)
        log.append('successfully start ngrok!')
        url, port = self._tunnel.public_url.replace('tcp://', '').split(':')
        url_id = url.replace(protocol.NGROK_URL_ENDING, '')
        ngrok_ip = socket.gethostbyname(url)
        port = int(port)
        ngrok_code = protocol.encode_address((url_id, port))
        log.append(f"ngrok details: url='{url} (id={url_id})', ip='{ngrok_ip}', port={port}, code={ngrok_code}")

    def start(self):
        self._running = True

    def stop(self):
        self._running = False
        try:
            ngrok.disconnect(self._tunnel.public_url)
        except Exception as e:
            log.append(f'could not stop ngrok! {e}')

    @property
    def running(self):
        return self._running

    @running.setter
    def running(self, other):
        self._running = other

    def accept(self):
        return ServerConnection(self, self._server_socket)

    def have_data(self):
        r, _, _ = select.select([self._server_socket], [], [], 0)
        return self._server_socket in r


class ServerConnection(protocol.ConnectionProtocol):
    def __init__(self, server: Server, sock: socket.socket):
        super(ServerConnection, self).__init__()
        self._server = server
        self._got_password = False
        self._socket, self._address = sock.accept()

    @property
    def _running(self):
        return self._server.running

    @property
    def address(self):
        return self._address

    @property
    def got_password(self):
        return self._got_password

    @got_password.setter
    def got_password(self, value):
        self._got_password = value
