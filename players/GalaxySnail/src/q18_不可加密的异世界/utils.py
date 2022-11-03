from Crypto.Cipher import AES


def xor(x, y):
    return bytes(a ^ b for a, b in zip(x, y))


def aes_dec_block(key, msg):
    assert len(key) == len(msg) == 16
    return AES.new(key, AES.MODE_ECB).decrypt(msg)
