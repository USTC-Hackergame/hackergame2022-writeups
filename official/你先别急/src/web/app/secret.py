import hashlib

secret_key = "<redacted>"
captcha_key = "<redacted>"

def sha256(msg):
    return hashlib.sha256(msg.encode()).hexdigest()

def flag_func(token):
    return f"flag{{JiJi{sha256('sqlinject_114212'+token)[:10]}}}"
