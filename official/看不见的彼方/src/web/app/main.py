from flask import Flask, request, make_response, render_template, session, redirect, url_for
import socket
import os
import base64
import OpenSSL
import hashlib

from secret import secret_key

app = Flask(__name__)
app.secret_key = secret_key

app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024

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


def sha256(msg: bytes):
    return hashlib.sha256(msg).hexdigest()


def get_user_id():
    return session['token'].split(":", 1)[0]


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        token = session['token']
        if request.files["file1"].filename == "" or request.files["file2"].filename == "":
            return render_template('index.html', result="你似乎没有选择所有需要上传的文件。")
        file1 = request.files["file1"].read()
        file2 = request.files["file2"].read()
        if type(file1) is str:
            # not sure how "file" is opened so just be careful
            file1 = file1.encode()
        if type(file2) is str:
            file2 = file2.encode()
        print(f"get upload from {get_user_id()}, {sha256(file1)}, {sha256(file2)}")
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((os.environ["nc_host"], int(os.environ["nc_port"])))

        buf = b""
        while True:
            buf += s.recv(4096)
            if buf == b"Please input your token: ":
                break
        s.sendall(token.encode() + b"\n")

        buf = b""
        while True:
            buf += s.recv(4096)
            if not b"Base64 of binary:".startswith(buf):
                break

        if buf == b"Base64 of binary: ":
            s.sendall(base64.b64encode(file1) + b"@" + base64.b64encode(file2) + b"\n")
            buf = b""
            while True:
                data = s.recv(4096)
                if not data:
                    break
                buf += data
        return render_template('index.html', result=buf.decode())
    else:
        return render_template('index.html', result='')