import os
import sys
import sympy
import secrets
import subprocess
from flag import flag1, flag2

SRC = './temp/code.c'
BIN = './temp/temp_bin'
DATA = './data'


def randprime(a, b):
    n = secrets.randbelow(b - a) + a
    return sympy.nextprime(n)


def generate_data(bits=512):
    p = randprime(2 ** (bits - 1), 2 ** bits)
    q = randprime(2 ** (bits - 1), 2 ** bits)
    if q < p:
        p, q = q, p
    return p, q


res_map = {
    'CE': 'Compile Error',
    'TLE': 'Time Limit Exceeded',
    'RE': 'Runtime Error',
    'WA': 'Wrong Answer',
    'AC': 'Accepted'
}


def check_excutable(path, input, ans, timeout):
    if not os.path.isfile(path):
        return 'CE'

    try:
        p = subprocess.run(
            ["su", "runner", "-c", path],
            input=input,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=timeout
        )
    except subprocess.TimeoutExpired:
        return 'TLE'

    if p.returncode != 0:
        return 'RE'

    try:
        output = p.stdout.decode()
    except UnicodeDecodeError:
        return 'WA'

    lines = output.strip().split('\n')
    return 'AC' if lines == ans else 'WA'


if __name__ == "__main__":
    # 生成动态测试数据
    N = 5
    inpaths = []
    outpaths = []

    os.makedirs(DATA, mode=0o700, exist_ok=True)

    for i in range(N):
        inpaths.append(os.path.join(DATA, f'dynamic{i}.in'))
        outpaths.append(os.path.join(DATA, f'dynamic{i}.out'))

        p, q = generate_data()
        n = p * q

        with open(inpaths[i], 'w') as f:
            f.write(f'{n}\n')
        with open(outpaths[i], 'w') as f:
            f.write(f'{p}\n{q}\n')

        os.chmod(inpaths[i], 0o700)
        os.chmod(outpaths[i], 0o700)

    with open(os.path.join(DATA, 'problem.txt'), 'r') as f:
        print(f.read())

    # 提示用户输入代码
    print("请输入你的代码（以两个空行作为结尾）：\n")

    code1 = []
    while True:
        try:
            line = input()
        except EOFError:
            break
        code1.append(line)

        if len(code1) >= 2 and code1[-1] == '' and code1[-2] == '':
            break

    with open(SRC, "w") as fd1:
        fd1.write('\n'.join(code1))

    p = subprocess.run(
        ["gcc", "-w", "-O2", SRC, "-o", BIN],
        stdout=sys.stdout,
        stdin=subprocess.DEVNULL,
        stderr=subprocess.STDOUT
    )

    # 测试静态数据
    with open(os.path.join(DATA, 'static.in'), 'rb') as f:
        instr = f.read()
    with open(os.path.join(DATA, 'static.out'), 'r') as f:
        ans = f.read().strip().split('\n')
    res = check_excutable(BIN, instr, ans, 0.5)

    print('静态数据测试：', res_map[res])
    if res == 'AC':
        print(flag1, flush=True)
    else:
        exit(0)
    print('\n')

    # 测试动态数据
    for i in range(N):
        with open(inpaths[i], 'rb') as f:
            instr = f.read()
        with open(outpaths[i], 'r') as f:
            ans = f.read().strip().split('\n')
        res = check_excutable(BIN, instr, ans, 0.5)
        if res != 'AC':
            break

    print(f'动态数据测试 ({i+1}/{N})：{res_map[res]}')
    if res == 'AC':
        print(flag2, flush=True)
