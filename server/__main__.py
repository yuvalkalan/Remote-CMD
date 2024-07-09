import subprocess

import protocol.ServerCodes
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
                    output = ''
                    if value:
                        command = f'cd {client.path} && ' + value + ' && cd'
                        result = subprocess.run(command, shell=True, capture_output=True, text=True)
                        if result.stderr:
                            output = result.stderr
                        else:
                            result = result.stdout.strip().rsplit('\n', maxsplit=1)
                            if len(result) == 1:
                                new_dir = result[0]
                            else:
                                output, new_dir = result
                            # print(f'output = {output}', f'new_dir = {new_dir}', sep='\n')
                            client.path = new_dir
                    client.send(protocol.ServerCodes.SEND_RESPONSE, output)
                    client.send(protocol.ServerCodes.SET_PATH, client.path)
                elif key == protocol.ClientCodes.GET_PATH:
                    client.send(protocol.ServerCodes.SET_PATH, client.path)
        return ok

    log.append('start server')
    server: Server = Server()
    server.start()
    client: ServerConnection = server.accept()
    log.append(f'connect new client - {client.address}')
    while server.running:
        data_ok = handle_data()
        if not data_ok:
            log.append(f'remove {client.address}! waiting for other connection...')
            client = server.accept()
            log.append(f'connect new client - {client.address}')
    server.stop()

