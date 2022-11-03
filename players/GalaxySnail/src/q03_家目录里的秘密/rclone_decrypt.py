import base64

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


# https://github.com/rclone/rclone/blob/v1.60.0/fs/config/obscure/obscure.go
KEY = bytes([
    0x9c, 0x93, 0x5b, 0x48, 0x73, 0x0a, 0x55, 0x4d,
    0x6b, 0xfd, 0x7c, 0x63, 0xc8, 0x86, 0xa9, 0x2b,
    0xd3, 0x90, 0x19, 0x8e, 0xb8, 0x12, 0x8a, 0xfb,
    0xf4, 0xde, 0x16, 0x2b, 0x8b, 0x95, 0xf6, 0x38,
])
# https://pkg.go.dev/crypto/aes#pkg-constants
AES_BLOCKSIZE = 16


def main():
    password = input().strip()
    password = base64.urlsafe_b64decode(password)
    iv = password[:AES_BLOCKSIZE]
    ciphertext = password[AES_BLOCKSIZE:]

    cipher = Cipher(algorithms.AES(KEY), modes.CTR(iv))
    decryptor = cipher.decryptor()
    plaintext = decryptor.update(ciphertext) + decryptor.finalize()
    print(plaintext)


if __name__ == "__main__":
    main()
