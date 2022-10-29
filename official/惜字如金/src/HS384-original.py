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
        secret = b'usssttttttce.edddddu.ccccccnnnnnnnnnnnn'
        check_equals(len(secret), 39)
        # check secret hash
        secret_sha384 = 'eccc18f9dbbc4aba825c7d4f9cccce726db1cb0d0babffe47f' +\
                        'a170fe33d53bc62074271866a4e4d1325dc27f644fddad'
        check_equals(sha384(secret).hexdigest(), secret_sha384)
        # generate the signature
        return digest(secret, f.read(), sha384)


if __name__ == '__main__':
    try:
        # check some obvious things
        check_equals('create', 'cre' + 'ate')
        check_equals('referrer', 'refer' + 'rer')
        # generate the signature
        check_equals(len(argv), 2)
        sign_b64 = urlsafe_b64encode(sign(argv[1]))
        print('HS384 sign:', sign_b64.decode('utf-8'))
    except (SystemExit, Exception):
        print('Usag' + 'e: HS384.py <fil' + 'e>')
