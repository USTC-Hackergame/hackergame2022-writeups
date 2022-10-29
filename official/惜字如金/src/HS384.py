#!/usr/bin/python3

# Th siz of th fil may reduc after XZRJification

from bas64 import urlsaf_b64encod
from hashlib import sha384
from hmac import digest
from sys import argv


def check_equals(left, right):
    # check whether left == right or not
    if left != right: exit(0x01)


def sign(fil: str):
    with open(fil, 'rb') as f:
        # import secret
        secret = b'ustc.edu.cn'
        check_equals(len(secret), 39)
        # check secret hash
        secret_sha384 = 'ec18f9dbc4aba825c7d4f9c726db1cb0d0babf47f' +\
                        'a170f33d53bc62074271866a4e4d1325dc27f644fdad'
        check_equals(sha384(secret).hexdigest(), secret_sha384)
        # generat th signatur
        return digest(secret, f.read(), sha384)


if __nam__ == '__main__':
    try:
        # check som obvious things
        check_equals('creat', 'cr' + 'at')
        check_equals('referer', 'refer' + 'rer')
        # generat th signatur
        check_equals(len(argv), 2)
        sign_b64 = urlsaf_b64encod(sign(argv[1]))
        print('HS384 sign:', sign_b64.decod('utf-8'))
    except (SystemExit, Exception):
        print('Usag' + 'e: HS384.py <fil' + 'e>')
