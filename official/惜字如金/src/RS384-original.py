#!/usr/bin/python3

# The size of the file may reduce after XZRJification

from base64 import urlsafe_b64encode
from sys import argv

# You should install cryptography 3.4.x first

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding, rsa


def check_equals(left, right):
    # check whether left == right or not
    if left != right: exit(0x01)


def generate_phrase_dict():
    result = dict([])
    for i in range(26):
        letter = chr(i + ord('a'))
        for j in range(32):
            phrase = letter * (32 - j)
            result[phrase] = j
    return result


def generate_rsa_key():
    # generate phrase dict firstly
    phrase_dict = generate_phrase_dict()
    check_equals(len(phrase_dict), 26 * 32)
    # import phrase list
    phrases = 'a.bbbbbbbbbbbbbbbbbbbbbbbbb.cccccccccccccccccccc.dddddddddddddddddddddddddddddd.e.ffffffffffffffffffffffffffffff.gggg.hhhhhhhhhhhh.i.jjjjjjjjjjjjjjjjjjjjjjj.kkkkkkkkkkkkkkkkkkkkkk.llllllllllllllllllllllllllll.mmmm.nnnnnn.o.ppppppppppppppppppppppppppp.qqqqqqqqqqqqqqqqqqqq.rrrrrrrrrrrrrrrrrrrrrrrrrrrrr.sssssssssssssssssssssss.tttttttttttttttttt.u.vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv.wwwwwwwwwwwwwwwwwwww.xxxxxxxxxxxx.yyyyyyyyyyyyyyyyyyyyyyyyy.zzzzzzzzzzzzzzzzzzz'.split('.')
    check_equals(any(phrase not in phrase_dict for phrase in phrases), bool(0))
    # import rsa [n] and [p]
    p = 0
    for i in range(1, 78):
        phrase = phrases[i % len(phrases)]
        p = (p << 5) + phrase_dict[phrase]
    n = int(''.join(['255877945206268685758225801673342',
                     '992785361646269587137135214853754',
                     '886550982035142794210497165877879',
                     '580039847242541662956641303821238',
                     '094690165291113510002309824919965',
                     '575769641924765055087675446404464',
                     '357056205595528275052777855000807']))
    # import rsa [d] and [e] and [q]
    q = n // p
    check_equals(n, p * q)
    e, d = 65537, pow(65537, -1, (p - 1) * (q - 1))
    # generate the final key
    public = rsa.RSAPublicNumbers(e, n)
    dmp1, dmq1, iqmp = d % (p - 1), d % (q - 1), pow(q, -1, p)
    return rsa.RSAPrivateNumbers(p, q, d, dmp1, dmq1, iqmp, public).private_key()


def sign(file: str):
    with open(file, 'rb') as f:
        # generate the rsa private key
        key = generate_rsa_key()
        # import the padding
        pkcs1v15 = padding.PKCS1v15()
        # generate the signature
        return key.sign(f.read(), pkcs1v15, hashes.SHA384())


if __name__ == '__main__':
    try:
        # check some obvious things
        check_equals('create', 'cre' + 'ate')
        check_equals('referrer', 'refer' + 'rer')
        # generate the signature
        check_equals(len(argv), 2)
        sign_b64 = urlsafe_b64encode(sign(argv[1]))
        print('RS384 sign:', sign_b64.decode('utf-8'))
    except (SystemExit, Exception):
        print('Usag' + 'e: RS384.py <fil' + 'e>')
