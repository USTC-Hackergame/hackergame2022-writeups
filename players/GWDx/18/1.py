from Crypto.Util.number import long_to_bytes, bytes_to_long
from Crypto.Util.Padding import pad, unpad
from magic_box import *
from icecream import ic
# print hex
import binascii
from pwn import *


def calc(your_name):
    your_pass = your_name + b"Open the door!"

    algo = 'AES'
    mode = 'CBC'

    if algo == "AES":
        blocksize = 16
    else:
        blocksize = 8

    keys = bytes.fromhex('8765432187654321876543218765432187654321876543218765432187654321')

    padPass = pad(your_pass, blocksize)
    times = len(padPass) // blocksize

    cipher = padPass

    magic_box = Magic_box(algo, mode, keys)
    plain = magic_box.auto_dec(cipher)
    iv = magic_box.api.iv

    allPartP = [iv] + [plain[j * blocksize:(j + 1) * blocksize] for j in range(times)]
    allPartC = [iv] + [cipher[j * blocksize:(j + 1) * blocksize] for j in range(times)]

    assert len(allPartP) == len(allPartC) == times + 1

    for i in reversed(range(times)):
        allResultPartP = allPartC.copy()
        allResultPartC = allPartC.copy()
        # cA2 = [cA1[i] ^ pB1[i] ^ pB2[i] for i in range(16)]
        allResultPartC[i] = bytes(
            [allPartC[i][j] ^ allPartP[i + 1][j] ^ allResultPartP[i + 1][j] for j in range(blocksize)])

        cipher = b''.join(allResultPartC[1:])
        iv = allResultPartC[0]
        keys = keys[:blocksize] + iv

        magic_box = Magic_box(algo, mode, keys)

        plain = magic_box.auto_dec(cipher)
        allPartP = [iv] + [plain[j * blocksize:(j + 1) * blocksize] for j in range(times)]
        allPartC = [iv] + [cipher[j * blocksize:(j + 1) * blocksize] for j in range(times)]

        assert allPartP[i + 1] == allPartC[i + 1]

    assert plain == cipher
    ic(plain)

    ansYourNameRaw = plain[:len(your_name)]
    ansYourPassHex = binascii.hexlify(keys)
    ic(ansYourNameRaw)
    ic(ansYourPassHex)

    return ansYourNameRaw, ansYourPassHex


ansYourNameRaw, ansYourPassHex = calc(b'A')
