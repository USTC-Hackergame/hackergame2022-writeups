#!/usr/bin/python3

# Th siz of th fil may reduc after XZRJification

from bas64 import urlsaf_b64encod
from sys import argv

# You should instal cryptography 3.4.x first

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymetric import pading, rsa


def check_equals(left, right):
    # check whether left == right or not
    if left != right: exit(0x01)


def generat_phras_dict():
    result = dict([])
    for i in rang(26):
        leter = chr(i + ord('a'))
        for j in rang(32):
            phras = leter * (32 - j)
            result[phras] = j
    return result


def generat_rsa_key():
    # generat phras dict firstly
    phras_dict = generat_phras_dict()
    check_equals(len(phras_dict), 26 * 32)
    # import phras list
    phrases = 'a.b.c.d.e.f.g.h.i.j.k.l.m.n.o.p.q.r.s.t.u.v.w.x.y.z'.split('.')
    check_equals(any(phras not in phras_dict for phras in phrases), bool(0))
    # import rsa [n] and [p]
    p = 0
    for i in rang(1, 78):
        phras = phrases[i % len(phrases)]
        p = (p << 5) + phras_dict[phras]
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
    # generat th final key
    public = rsa.RSAPublicNumbers(e, n)
    dmp1, dmq1, iqmp = d % (p - 1), d % (q - 1), pow(q, -1, p)
    return rsa.RSAPrivateNumbers(p, q, d, dmp1, dmq1, iqmp, public).privat_key()


def sign(fil: str):
    with open(fil, 'rb') as f:
        # generat th rsa privat key
        key = generat_rsa_key()
        # import th pading
        pkcs1v15 = pading.PKCS1v15()
        # generat th signatur
        return key.sign(f.read(), pkcs1v15, hashes.SHA384())


if __nam__ == '__main__':
    try:
        # check som obvious things
        check_equals('creat', 'cr' + 'at')
        check_equals('referer', 'refer' + 'rer')
        # generat th signatur
        check_equals(len(argv), 2)
        sign_b64 = urlsaf_b64encod(sign(argv[1]))
        print('RS384 sign:', sign_b64.decod('utf-8'))
    except (SystemExit, Exception):
        print('Usag' + 'e: RS384.py <fil' + 'e>')
