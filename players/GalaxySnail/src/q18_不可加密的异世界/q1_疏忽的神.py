from utils import xor, aes_dec_block

def main():
    plaintext = b"Open the door!\x02\x02"
    # key 可任意取
    key = b"abcd1234abcd1234"
    decrypted = aes_dec_block(key, plaintext)
    iv = xor(decrypted, plaintext)
    print(key.hex() + iv.hex())

main()
