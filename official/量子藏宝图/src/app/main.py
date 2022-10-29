from flask import Flask, session, request, redirect,\
                  url_for, render_template, make_response
from secret import get_flag, verify_token, get_01_flag_str
from config import debug, port, qkd_key_len_required, output_dir

from Crypto.Random import random
import os
import uuid
import subprocess
import logging


app = Flask(__name__)
app.config["SECRET_KEY"] = "<redacted>"
app.config["DEBUG"] = debug
app.config["Port"] = port
app.config["SESSION_COOKIE_NAME"] = "quantum_session"


uuid_namespace = uuid.UUID("6ba94efc-d3e8-4243-8fd4-0fe23a45fc84")

if debug:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)

logging.info("starting server")
logging.info(f"output_dir: {output_dir}")
logging.info(f"debug: {debug}, {type(debug)}")
logging.info(f"key len: {qkd_key_len_required}")


@app.before_request
def session_init():
    if request.path.startswith('/static/'):
        return
    if request.args.get('token'):
        try:
            token = request.args.get('token')
            assert (verify_token(token))
            session['token'] = token
        except Exception:
            session['token'] = None
        return redirect(url_for('login'))

    if session.get("token") is None:
        return make_response(render_template("error.html"), 403)


@app.route('/', methods=['GET'])
def index():
    return render_template("index.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "GET":
        return render_template("index.html")

    alice_basis = request.form.get('alice_basis', '')
    alice_result = request.form.get('alice_result', '')

    if alice_basis == '' or alice_result == '':
        qkd_state_clean()
        return render_template("index.html", fail_msg="输入内容不能为空")

    alice_basis = alice_basis.strip().lower()
    alice_result = alice_result.strip().lower()
    for c in alice_basis:
        if c not in "x+":
            qkd_state_clean()
            return render_template("index.html", fail_msg="制备基底只能为 'x' 或 '+'")
    for c in alice_result:
        if c not in "01":
            qkd_state_clean()
            return render_template("index.html", fail_msg="量子态只能为 '0' 或 '1'")
    if len(alice_basis) != len(alice_result):
        qkd_state_clean()
        return render_template("index.html", fail_msg="制备基底和量子态长度不一致")

    session["alice_basis"] = alice_basis
    session["alice_result"] = alice_result

    if session.get("bob_basis") is None:
        session["bob_basis"] = "".join([random.choice("x+")
                                        for _ in range(len(alice_basis))])

    return render_template("index.html", alice_basis=alice_basis,
                           alice_result=alice_result,
                           bob_basis=session["bob_basis"])


@app.route("/check_key", methods=["POST"])
def check_key():
    alice_basis = request.form.get('alice_basis', '')
    alice_result = request.form.get('alice_result', '')
    bob_basis = request.form.get('bob_basis', '')
    bob_result = request.form.get('bob_result', '')

    if alice_basis != session["alice_basis"] or \
       alice_result != session["alice_result"] or \
       bob_basis != session["bob_basis"]:
        qkd_state_clean()
        return render_template("index.html", fail_msg="参数错误")

    if bob_result == '':
        return render_template("index.html", alice_basis=alice_basis,
                               alice_result=alice_result,
                               bob_basis=session["bob_basis"],
                               fail_msg="密钥不能为空")

    if len(bob_result) < qkd_key_len_required:
        return render_template("index.html", alice_basis=alice_basis,
                               alice_result=alice_result,
                               bob_basis=session["bob_basis"],
                               fail_msg=f"密钥长度小于 {qkd_key_len_required} 位")

    bob_result = bob_result.strip().lower()

    correct_secret_key = ""
    for i in range(len(alice_basis)):
        if alice_basis[i] == bob_basis[i]:
            correct_secret_key += alice_result[i]

    if bob_result != correct_secret_key:
        return render_template("index.html", alice_basis=alice_basis,
                               alice_result=alice_result,
                               bob_basis=session["bob_basis"],
                               fail_msg="密码错误")
    session["login_succ"] = '1'
    return redirect(url_for("get_map"))


@app.route("/get_map", methods=["GET"])
def get_map():
    if not session.get("login_succ") or session.get("login_succ") != '1':
        return redirect(url_for("login"))

    map_uuid = session.get("uuid")
    if map_uuid is None:
        try:
            map_uuid = gen_new_map()
            session["uuid"] = map_uuid
        except Exception as e:
            logging.info(e)
            return render_template("map.html",
                                   fail_msg="宝藏图产生错误，请刷新页面。\
如果多次刷新不成功，请联系管理员。")

    map_file_name = get_map_file_name(map_uuid)

    if not os.path.exists(map_file_name):
        session["uuid"] = None
        return render_template("map.html",
                               fail_msg="宝藏图文件不存在，请刷新页面。")

    return render_template("map.html", map_uuid=map_uuid,
                           map_file_name=map_file_name)


@app.route("/clean_qkd", methods=["GET"])
def clean_qkd():
    qkd_state_clean()
    return redirect(url_for("login"))


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


def qkd_state_clean():
    token = session.get("token", "")
    logging.debug(f"clean qkd state for {token}")
    session.pop("alice_basis", None)
    session.pop("alice_result", None)
    session.pop("bob_basis", None)


def get_map_file_name(uuid):
    return f"{output_dir}{uuid}.png"


def gen_new_map():
    token = session["token"]
    map_uuid = str(uuid.uuid5(uuid_namespace, token))
    map_file_name = get_map_file_name(map_uuid)
    logging.info(f"generate map for {token}: {map_file_name}")
    logging.info(f"flag: {get_flag(token)} bin: {get_01_flag_str(token)}")
    p = subprocess.run(f"python map.py {token} ./{map_file_name}",
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                       shell=True)
    logging.info(f"generation result: {p.returncode}")
    logging.info(f"Output: {p.stdout.decode('utf-8')}")
    logging.info(f"Error: {p.stderr.decode('utf-8')}")
    p.check_returncode()
    return map_uuid


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    app.run(port=app.config["Port"], debug=app.config["DEBUG"])
