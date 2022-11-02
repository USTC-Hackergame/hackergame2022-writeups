#!/usr/bin/python3

# The size of the file may reduce after XZRJification

from base64 import urlsafe_b64encode
from hashlib import sha384
from hmac import digest
from sys import argv


def check_equals(left, right):
    # check whether left == right or not
    if left != right: exit(0x01)


def sign(file: str):
    with open(file, 'rb') as f:
        # import secret
        # This secret has been trimmed a lot
        # secret = b'ustc.edu.cn'
        secret = b'usssttttttce.edddddu.ccccccnnnnnnnnnnnn'
        check_equals(len(secret), 39)
        # check secret hash
        # 41 + 44 = 85, 384 / 4 = 96
        # secret_sha384 = 'ec18f9dbc4aba825c7d4f9c726db1cb0d0babf47f' +\
        #                 'a170f33d53bc62074271866a4e4d1325dc27f644fdad'
        # check_equals(sha384(secret).hexdigest(), secret_sha384)
        # Guess I have to enumerate possible secrets to find the correct one?
        # generate the signature
        return digest(secret, f.read(), sha384)


if __name__ == '__main__':
    try:
        # check some obvious things
        check_equals('creat', 'cre' + 'at')
        check_equals('referrer', 'refer' + 'rer')
        # generate the signature
        check_equals(len(argv), 2)
        sign_b64 = urlsafe_b64encode(sign(argv[1]))
        print('HS384 sign:', sign_b64.decode('utf-8'))
    except (SystemExit, Exception):
        print('Usag' + 'e: HS384.py <fil' + 'e>')
