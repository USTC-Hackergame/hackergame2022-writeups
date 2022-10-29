from Crypto.Cipher import AES, DES

algos = ["AES", "DES"]
modes = ["ECB", "CBC", "OFB", "CFB"]

aes_mapping_mode = {
    "ECB": AES.MODE_ECB,
    "CBC": AES.MODE_CBC,
    "OFB": AES.MODE_OFB,
    "CFB": AES.MODE_CFB,
}

des_mapping_mode = {
    "ECB": DES.MODE_ECB,
    "CBC": DES.MODE_CBC,
    "OFB": DES.MODE_OFB,
    "CFB": DES.MODE_CFB,
}


def crc128(data, poly=0x883ddfe55bba9af41f47bd6e0b0d8f8f):
    crc = (1 << 128) - 1

    for b in data:
        crc ^= b
        for _ in range(8):
            crc = (crc >> 1) ^ (poly & -(crc & 1))

    return crc ^ ((1 << 128) - 1)


'''
Unencryptable World of symmetric cryptography
'''


class Magic_box():
    api = None
    mode = None
    key = None
    IV = None

    def __init__(self, algo, mode, keys):
        if algo == "AES":
            try:
                if len(keys) == 16:
                    assert mode == "ECB"
                    self.api = AES.new(keys[:16], aes_mapping_mode[mode])
                elif len(keys) == 32:
                    self.api = AES.new(
                        keys[:16], aes_mapping_mode[mode], keys[16:])
                else:
                    assert False, "Invalid parameters"
            except:
                assert False, "Invalid parameters"

        elif algo == "DES":
            try:
                if len(keys) == 8:
                    assert mode == "ECB"
                    self.api = DES.new(keys[:8], des_mapping_mode[mode])
                elif len(keys) == 16:
                    self.api = DES.new(
                        keys[:8], des_mapping_mode[mode], keys[8:])
                else:
                    assert False, "Invalid parameters"
            except:
                assert False, "Invalid parameters"

        else:
            assert False, "Not implemented error"

    def auto_dec(self, msg):
        return self.api.decrypt(msg)

    def auto_enc(self, msg):
        return self.api.encrypt(msg)
