from flask import Flask, request, make_response, render_template, session, redirect, url_for
import socket
import os
import base64
import OpenSSL

from secret import secret_key, BOT_SECRET

app = Flask(__name__)
app.secret_key = secret_key

app.config["MAX_CONTENT_LENGTH"] = 2 * 1024 * 1024

with open("./cert.pem") as f:
    cert = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, f.read())

@app.before_request
def check():
    if request.path.startswith('/static/'):
        return
    if request.args.get('bot') == BOT_SECRET:
        session['token'] = "bot"
        return redirect(url_for('bot'))
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


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form['name']
        q1, q2, q3, q4, q5 = request.form['q1'], request.form['q2'], request.form['q3'], request.form['q4'], request.form['q5']
        name = name.strip()
        q1 = q1.strip()
        q2 = q2.strip()
        q3 = q3.strip()
        q4 = q4.strip()
        q5 = q5.strip()
        # expected ans:
        # q1 => 0.8
        # q2 => 1.0
        # q3 => 1.3
        # q4 => 0.1
        # q5 => -1.6
        score = 0
        if q1 == "0.8":
            score += 20
        if q2 == "1.0":
            score += 20
        if q3 == "1.3":
            score += 20
        if q4 == "0.1":
            score += 20
        if q5 == "-1.6":
            score += 20

        return redirect(url_for('share', result=base64.b64encode(f"{score}:{name}".encode()).decode()))
    else:
        return render_template('index.html')

@app.route("/share", methods=["GET"])
def share():
    # check b64 validity and record user-input to console
    result = base64.b64decode(request.args.get('result')).decode()
    score, name = result.split(":", 1)
    print(score, name)

    return render_template('share.html')

@app.route("/bot", methods=["GET"])
def bot():
    # bot landing page
    if session["token"] != "bot":
        return "You are not a bot."
    return "OK"
