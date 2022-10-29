import hashlib
import OpenSSL
import base64

flag = "flag{%s}"

with open("cert.pem") as f:
    cert = OpenSSL.crypto.load_certificate(
        OpenSSL.crypto.FILETYPE_PEM, f.read())


def get_flag(token):
    return flag % hashlib.sha256(
        ('braket2022-wjeDQpVm'+token).encode()).hexdigest()[:10]


def get_01_flag_str(token: str):
    flag = get_flag(token)
    print(flag)
    flag_01 = "".join(['{:08b}'.format(ord(c)) for c in flag])
    return flag_01


def verify_token(token):
    try:
        id, sig = token.split(":", 1)
        sig = base64.b64decode(sig, validate=True)
        OpenSSL.crypto.verify(cert, sig, id.encode(), "sha256")
    except Exception:
        return False
    return True
