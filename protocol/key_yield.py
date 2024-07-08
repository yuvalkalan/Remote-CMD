KEY_SIZE = 2


def _next_key():
    i = 0
    while True:
        yield i
        i += 1


next_key = _next_key()

CONN_QUIT = (next(next_key)).to_bytes(KEY_SIZE, 'little')
