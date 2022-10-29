import json
from flask import (
    Flask,
    request,
    make_response,
    render_template,
    session,
    redirect,
    url_for,
    jsonify,
)
import sqlite3
import base64
import OpenSSL
import traceback
import io
import random
import subprocess
import time
from captcha.image import ImageCaptcha

from secret import secret_key, flag_func, captcha_key, sha256

app = Flask(__name__)
app.secret_key = secret_key

app.config["MAX_CONTENT_LENGTH"] = 2 * 1024 * 1024

with open("./cert.pem") as f:
    cert = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, f.read())


def force_int(s: str, default: int = 0):
    try:
        return int(s)
    except ValueError:
        return default


MAX_RISKNESS = 9


def generate_captcha(riskness: int):
    # randomly generate a captcha, no security purposes

    digits = "0123456789"
    letters = "abcdefghijkmnpqrtuvwxy" + "ABCDEFGHJKLMNPQRTVWXY"
    # digits_o = "6890"

    def rstr(alphabet, length):
        return "".join(random.choice(alphabet) for _ in range(length))

    riskness_lut = {
        # (digits, letters, digits_o)
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
    # cap_str += rstr(digits_o, riskness_lut[riskness][2])

    capimg = io.BytesIO()
    ImageCaptcha(width=160 * 2).write(cap_str, capimg)

    return cap_str, base64.b64encode(capimg.getvalue()).decode()


def assert_no_sql_injection(s: str):
    s = s.lower()
    # avoid some simple (or costly) sql injection
    blocklist = [
        "blob", # randomblob, zeroblob
        "load", # load_extension
        "attach", # attach database
        ";", "\n", "\r",
    ]
    if len(s) > 256:
        raise Exception("SQL too long")

    for b in blocklist:
        if b in s:
            raise Exception("SQL injection detected")

@app.before_request
def check():
    if request.path.startswith("/static/"):
        return
    if request.args.get("token"):
        try:
            token = request.args.get("token")
            id, sig = token.split(":", 1)
            sig = base64.b64decode(sig, validate=True)
            OpenSSL.crypto.verify(cert, sig, id.encode(), "sha256")
            session["token"] = token
        except Exception:
            session["token"] = None
        return redirect(url_for("index"))
    if session.get("token") is None:
        return make_response(render_template("error.html"), 403)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("index.html", showmsg=False)
    else:
        # This is INSECURE! Do not use this in production!
        cap = request.form.get("cap").lower()
        expected_hash = session.get("caphash")
        got_hash = sha256(cap + captcha_key)
        print(cap, expected_hash, got_hash)
        if got_hash != expected_hash:
            return render_template("index.html", showmsg=True, msg="验证码错误")
        return render_template("index.html", showmsg=True, msg="验证码正确")


def check_last_action():
    return True


@app.route("/captcha", methods=["POST"])
def captcha():
    if not check_last_action():
        return jsonify({"status": "error", "msg": "太急了！稍微等一下吧"})
    username = request.form.get("username", "")
    if not username:
        return jsonify({"status": "error", "msg": "username is empty"})
    try:
        assert_no_sql_injection(username)
        sql = f"select riskness from users where username='{username}'"
        proc = subprocess.run(["python3", "./database.py"], input=(f"{session['token']}" + '\n' + f"{sql}" + '\n').encode(),
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=5)
        if proc.returncode != 0:
            print(proc.stderr[:8192].decode())
        x = json.loads(proc.stdout[:8192].decode())

        print(x)
        riskness = force_int(x, MAX_RISKNESS)
        cap_str, img_b64 = generate_captcha(riskness)
        # This is INSECURE! Do not use this in production!
        session['caphash'] = sha256(cap_str.lower() + captcha_key)
        return jsonify({"status": "ok", "result": img_b64})

    except Exception as e:
        traceback.print_exc()
        print(e)
        cap_str, img_b64 = generate_captcha(MAX_RISKNESS)
        # This is INSECURE! Do not use this in production!
        session['caphash'] = sha256(cap_str.lower() + captcha_key)
        return jsonify({"status": "ok", "result": img_b64})


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=11230, debug=True)
