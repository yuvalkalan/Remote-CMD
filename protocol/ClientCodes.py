from .key_yield import next_key, KEY_SIZE


SERVER_CONN_QUIT = (next(next_key)).to_bytes(KEY_SIZE, 'little')
SEND_COMMAND = (next(next_key)).to_bytes(KEY_SIZE, 'little')
SET_PASSWORD = (next(next_key)).to_bytes(KEY_SIZE, 'little')
