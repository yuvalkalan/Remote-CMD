import time
from .classes import *
from threading import Thread


def terminal_thread(client: Client):
    while not client.path:
        pass
    while client.running:
        while not client.send_mode:
            pass
        command = input(f'{client.path}>')
        client.send(protocol.ClientCodes.SEND_COMMAND, command)
        client.send_mode = False


def main():
    code = input('enter server code: ')
    password = input('enter password: ')
    client = Client(code, password)
    client.start()
    print('connected!')
    terminal = Thread(target=terminal_thread, args=[client])
    terminal.start()
    while client.running:
        while client.have_data():
            key, value = client.receive()
            if key == protocol.CONN_QUIT:
                client.stop()
                break
            elif key == protocol.ServerCodes.SEND_RESPONSE:
                print(value)
            elif key == protocol.ServerCodes.SET_PATH:
                client.path = value
                time.sleep(0.1)
                client.send_mode = True
    terminal.join()
