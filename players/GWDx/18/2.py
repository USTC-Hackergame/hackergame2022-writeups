from Crypto.Util.number import long_to_bytes, bytes_to_long
from Crypto.Util.Padding import pad, unpad
from magic_box import *
from icecream import ic
import binascii
from Crypto.Cipher import AES, DES
from pwn import *


def calc(targetString, index):
    algo = 'DES'
    mode = 'CBC'

    blocksize = 8

    padPass = targetString[:(index + 1) * blocksize]
    times = len(padPass) // blocksize

    key = iv = bytes.fromhex('1234567812345678')

    # init
    # P = padPass
    # C[index] = padPass[index]
    P = [iv] + [padPass[j * blocksize:(j + 1) * blocksize] for j in range(times)]
    C = [iv] + [padPass[j * blocksize:(j + 1) * blocksize] for j in range(times)]

    # c[i] = P[i+1] ^ f-1(c[i+1])
    for i in reversed(range(times)):
        magicBoxECB = Magic_box(algo, 'ECB', key)
        reverseF = magicBoxECB.auto_dec(C[i + 1])
        C[i] = bytes([P[i + 1][j] ^ reverseF[j] for j in range(blocksize)])

    iv = C[0]
    keys = key + iv

    magic_box = Magic_box(algo, mode, keys)
    encrypt = magic_box.auto_enc(padPass)
    # ic(binascii.hexlify(encrypt))
    # ic(binascii.hexlify(padPass))
    assert encrypt[index * blocksize:(index + 1) * blocksize] == targetString[index * blocksize:(index + 1) * blocksize]

    passHex = binascii.hexlify(keys)
    return passHex


blocksize = 8
blockNum = 10

targetHex = 'd09297eecd6da9e2dec6b1e0ed29eaf2801c6128b92cdd7b9700c5da77fd22b5e2b556ebec6596d8de1bf9c14a9031bf25e149a2f513d32191b24cbbdb018a47e9658fc7ac503f3067ae929fc40e667d'
targetString = binascii.unhexlify(targetHex)

for i in range(blockNum):
    partTargetString = targetString
    keys = calc(partTargetString, i).decode()
    print(keys)
