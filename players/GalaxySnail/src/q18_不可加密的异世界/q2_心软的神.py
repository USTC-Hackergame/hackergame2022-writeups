from utils import xor, aes_dec_block

def main():
    key = b"abcd1234abcd1234"  # key 是任意的

    # 反向操作 OFB 模式，确保加密结果是全零，这样明文和密文就是一致的
    for i in range(10):
        data = aes_dec_block(key, bytes(16))
        for j in range(i):
            data = aes_dec_block(key, data)
        iv = data
        input(key.hex() + iv.hex())

if __name__ == "__main__":
    main()
