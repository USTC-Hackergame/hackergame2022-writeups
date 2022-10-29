# pip install captcha==0.4
# Reference env: Debian 10 (buster) + Python 3.10.4

from captcha.image import ImageCaptcha
import random


def generate_captcha(riskness: int):

    digits = "0123456789"
    letters = "abcdefghijkmnpqrtuvwxy" + "ABCDEFGHJKLMNPQRTVWXY"

    def rstr(alphabet, length):
        return "".join(random.choice(alphabet) for _ in range(length))

    riskness_lut = {
        # (digits, letters)
        1: (9, 0),
        2: (8, 1),
        3: (7, 2),
        4: (6, 3),
        5: (5, 4),
        6: (4, 5),
        7: (3, 6),
        8: (2, 7),
        9: (0, 9),
    }

    cap_str = ""

    cap_str += rstr(digits, riskness_lut[riskness][0])
    cap_str += rstr(letters, riskness_lut[riskness][1])

    ImageCaptcha(width=160 * 2).write(cap_str, f"./test-{riskness}.png")


if __name__ == "__main__":
    # Example:
    # Simple-1
    generate_captcha(1)
    # OP-9
    generate_captcha(9)
