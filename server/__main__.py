from .classes import *
from .constants import *


def main():
    def handle_data():
        ok = True
        while client.have_data():
            key, value = client.receive()
            try:
                log.append(f'got new msg from {client.address}; key = {key}, value = {value}')
            except ValueError:
                ok = False
                break
            if ok:
                if not client.got_password and key != protocol.ClientCodes.SET_PASSWORD:
                    ok = False
                    break
                elif key == protocol.CONN_QUIT:
                    ok = False
                    break
                elif key == protocol.ClientCodes.SET_PASSWORD:
                    if value == SERVER_PASSWORD:
                        client.got_password = True
                        log.append(f'correct password from {client.address}')
                    else:
                        log.append(f'incorrect password from {client.address}')
                        ok = False
                elif key == protocol.ClientCodes.SEND_COMMAND:
                    pass #TODO
        return ok

    server: Server = Server()
    server.start()

    client: ServerConnection = server.accept()
    while server.running:
        data_ok = handle_data()
        if not data_ok:
            log.append(f'remove {client.address}! waiting for other connection...')
            client = server.accept()
    server.stop()

