from .key_yield import next_key, KEY_SIZE


SEND_RESPONSE = (next(next_key)).to_bytes(KEY_SIZE, 'little')
