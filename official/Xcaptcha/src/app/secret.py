import hashlib

secret_key = "<redacted>"

def sha256(msg):
    return hashlib.sha256(msg.encode()).hexdigest()

def flag_func(token):
    return f"flag{{head1E55_br0w5er_and_ReQuEsTs_areallyour_FR1ENd_{sha256('webautomatic_1'+token)[:10]}}}"
