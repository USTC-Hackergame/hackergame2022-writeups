import  hashlib
secret_key = "<redacted>"

def get_flag(token):
    flag = "flag{Torch.Load.Is.Dangerous-%s}"
    return flag % hashlib.sha256(('j0h8ej1s3hd86g13'+token).encode()).hexdigest()[:10]
