import sys
import hmac
import base64


def sign(filename) -> None:
    secret = b"usssttttttce.edddddu.ccccccnnnnnnnnnnnn"
    m = hmac.new(secret, None, "sha384")

    with open(filename, "rb") as f:
        while data := f.read(64 * 1024):
            m.update(data)

    print(base64.urlsafe_b64encode(m.digest()).decode())


if __name__ == "__main__":
    sign(sys.argv[1])
