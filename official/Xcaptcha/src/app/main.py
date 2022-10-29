from flask import Flask, request, make_response, render_template, session, redirect, url_for
import socket
import os
import base64
import OpenSSL
import time

from secret import secret_key, flag_func

app = Flask(__name__)
app.secret_key = secret_key

app.config["MAX_CONTENT_LENGTH"] = 2 * 1024 * 1024

with open("./cert.pem") as f:
    cert = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, f.read())

@app.before_request
def check():
    if request.path.startswith('/static/'):
        return
    if request.args.get('token'):
        try:
            token = request.args.get('token')
            id, sig = token.split(":", 1)
            sig = base64.b64decode(sig, validate=True)
            OpenSSL.crypto.verify(cert, sig, id.encode(), "sha256")
            session['token'] = token
        except Exception:
            session['token'] = None
        return redirect(url_for('index'))
    if session.get("token") is None:
        return make_response(render_template("error.html"), 403)


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html", failed=False)

@app.route("/xcaptcha", methods=["GET", "POST"])
def xcaptcha():
    if request.method == "GET":
        # generate 3 random large number addition challenges
        challenges = []
        for i in range(3):
            a = int.from_bytes(os.urandom(16), byteorder="big")
            b = int.from_bytes(os.urandom(16), byteorder="big")
            challenges.append((a, b))
        # get current time
        now = time.time_ns()
        # append and sign
        text = str(now)
        for i in challenges:
            text += f",{i[0]},{i[1]}"
        # This is INSECURE! Do not use this in production!
        session["text"] = text
        return render_template("xcaptcha.html", 
            expr1=f"{challenges[0][0]}+{challenges[0][1]}", 
            expr2=f"{challenges[1][0]}+{challenges[1][1]}", 
            expr3=f"{challenges[2][0]}+{challenges[2][1]}", 
        )
    else:
        now = time.time_ns()
        try:
            expr1 = int(request.form.get("captcha1", ""))
            expr2 = int(request.form.get("captcha2", ""))
            expr3 = int(request.form.get("captcha3", ""))
        except ValueError:
            return render_template("index.html", failed=True, failed_reason="输入的验证码不符合要求")

        text = session["text"].split(",")
        past = int(text[0])

        if past >= now:
            return render_template("index.html", failed=True, failed_reason="检测到时空穿越")
        if now - past > 1000000000:  # 10**9
            return render_template("index.html", failed=True, failed_reason="超过 1 秒限制")
        expr1_expected = int(text[1]) + int(text[2])
        expr2_expected = int(text[3]) + int(text[4])
        expr3_expected = int(text[5]) + int(text[6])

        if expr1 != expr1_expected or expr2 != expr2_expected or expr3 != expr3_expected:
            return render_template("index.html", failed=True, failed_reason="计算结果错误")
        
        return render_template("success.html", flag=flag_func(session['token']))
