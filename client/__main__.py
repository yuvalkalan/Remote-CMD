from .classes import *
from threading import Thread
from queue import Queue


def terminal_thread(client: Client):
    while client.running:
        command = input('command: ')
        client.send(protocol.ClientCodes.SEND_COMMAND, command)


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
    terminal.join()
