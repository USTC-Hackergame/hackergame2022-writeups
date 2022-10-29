from flask import Flask, request, make_response, render_template, session, redirect, url_for
import socket
import os
import base64
import OpenSSL
import hashlib
import json
import matplotlib.image
import io
import numpy as np
import traceback

from secret import secret_key, get_flag
from info import tags

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


def sha256(msg: bytes):
    return hashlib.sha256(msg).hexdigest()


def get_user_id():
    return session['token'].split(":", 1)[0]


gt_imgs = []
for i in range(10):
    # read RGB values
    gt_imgs.append(matplotlib.image.imread(f"./static/images/{i}.png")[:,:,:3])

def calc_error(gen_img_b64):
    # gen_img_b64: list of base64 encoded png
    global gt_imgs
    # gt_imgs: list of numpy array

    assert len(gen_img_b64) == 10
    # read RGB values
    gen_imgs = [matplotlib.image.imread(io.BytesIO(base64.b64decode(ib)))[:,:,:3] for ib in gen_img_b64]

    # calculate error
    error = []
    for i in range(10):
        error.append(np.mean((gt_imgs[i] - gen_imgs[i]) ** 2))

    return error

@app.route("/", methods=["GET", "POST"])
def index():
    images = []
    for i in range(10):
        images.append({
            "tags": tags[i],
            "gen": "",
            "refid": i
        })
    if request.method == "POST":
        token = session['token']
        if request.files["file"].filename == "":
            return render_template('index.html', result="你似乎没有选择需要上传的模型。")
        file = request.files["file"].read()

        # SECURITY: check file size, < 1M
        if len(file) > 1024 * 1024:
            return render_template('index.html', result="你的模型太大了。")

        print(f"get upload from {get_user_id()}, {sha256(file)}")


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

        # SECURITY ISSUE: limit the max length of buf
        # send: max 1M
        # receive: max 1M
        limitation = 512 * 1024
        if buf == b"Base64 of binary: ":
            s.sendall(base64.b64encode(file) + b"\n")
            buf = b""
            while limitation > 0:
                data = s.recv(limitation)
                if not data:
                    break
                buf += data
                limitation -= len(data)
        buf = buf.decode()

        if buf.startswith("Player connection rate"):
            return render_template('index.html', result="连接过于频繁，请稍等一会再尝试。", images=images)
        if buf.strip() == "Killed":
            return render_template('index.html', result="加载并运行模型过程中出错（超时）。", images=images)
        try:
            obj = json.loads(buf) # SECURITY ISSUE: maybe malicious data
            gen_imgs_b64 = obj["gen_imgs_b64"]

            for i in range(10):
                images[i]["gen"] = "data:image/png;charset=utf-8;base64," + gen_imgs_b64[i]

            errors = calc_error(gen_imgs_b64)

            threshold = 0.0005
            threshold_almost = 0.05
            max_error = float(np.max(errors))
            if max_error <= threshold:
                result = get_flag(token)
            else:
                error_str = ["{:.5f}".format(float(e)) for e in errors]
                error_str = ", ".join(error_str)

                if max_error <= threshold_almost:
                    result = "最大误差：{:.5f} > {}，还差一点点。".format(max_error, threshold)
                else:
                    result = "最大误差：{:.5f} > {}，没有达到要求。".format(max_error, threshold)

                result += "每张图片的误差（loss 值）：{}".format(error_str)

            return render_template('index.html', result=result, images=images)
        except:
            print(buf, "buf")
            traceback.print_exc()
            return render_template('index.html', result="加载并运行模型过程中出错。", images=images)
    else:
        return render_template('index.html', result='', images=images)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=10123, debug=True)
