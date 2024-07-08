from .classes import *


def main():
    code = input('enter server code: ')
    password = input('enter password: ')
    client = Client(code, password)
    client.start()
    print('connected!')
    while client.running:
        while client.have_data():
            key, value = client.receive()
            if key == protocol.CONN_QUIT:
                client.stop()
                break
            elif key == protocol.ServerCodes.SEND_RESPONSE:
                print(value)
