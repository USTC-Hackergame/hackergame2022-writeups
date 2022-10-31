#!/usr/bin/env python3

import shelve
import re
import subprocess
from urllib.request import urlretrieve
import difflib
from pwn import remote


def get_features(objdump_output):
    lineiter = iter(objdump_output.split('\n'))

    for line in lineiter:
        if line.endswith(' <.text>:'):
            break

    feature_table = {0: []}
    cur_offset = 0

    for line in lineiter:
        if len(line) == 0:
            break

        parts = line.split('\t')
        offset = int(parts[0][:-1].strip(), 16)

        if len(parts) != 3:
            continue

        if ' ' in parts[2]:
            instr, ops = parts[2].split(maxsplit=1)
        else:
            instr = parts[2]
            ops = ""

        if "#" in ops:
            ops, comment = ops.split("#")
            ops = ops.strip()
        else:
            comment = ""

        if instr == "endbr64":
            feature_table[offset] = []
            cur_offset = offset

        if instr.startswith("j") or instr in ["cmp", "test", "call"] or comment:
            ops = re.sub(r"\b(0x)?[0-9a-f]+", "", ops)
            comment = re.sub(r"0x[0-9a-f]+", "0x", comment)
            s = "\t".join([instr, ops, comment])
            feature_table[cur_offset].append(s)

    return feature_table


def analyze(offset1, objdump_out1, objdump_out2):
    feature_table1 = get_features(objdump_out1)
    feature_table2 = get_features(objdump_out2)

    if offset1 not in feature_table1:
        return "0000"

    ft1 = feature_table1[offset1]
    scores = dict()

    for offset2, ft2 in feature_table2.items():
        pos = 0
        scores[offset2] = 0
        score_weight = 1.0

        for item in ft2:
            matches = difflib.get_close_matches(item, ft1[pos:])

            if len(matches) == 0:
                break
            else:
                selected_match = min(ft1[pos:].index(i) for i in matches)

            ratio = difflib.SequenceMatcher(None, item, ft1[pos + selected_match]).ratio()
            scores[offset2] += ratio * score_weight
            score_weight *= 0.8
            if score_weight < 0.1:
                break

            pos += selected_match + 1

    offset2, _ = max(scores.items(), key=lambda x: x[1])
    return hex(offset2)


"""
objdump_out1 = subprocess.check_output(["objdump", "-d", "bin1"]).decode()
objdump_out2 = subprocess.check_output(["objdump", "-d", "bin2"]).decode()
answer = analyze(0x69aa, objdump_out1, objdump_out2)
print(answer)
quit()
"""

conn = remote("202.38.93.111", 12400)
conn.recvuntil(b'Please input your token: ')
conn.send(b'1293:MEYCIQCMylj8ebhRzVZlxNe+KLpDC+Qy5etISN1KOd5mfeJGtwIhAKaGf307hVOcJwMjnMWG2gdpP771YM5NC578/FFyHmwO\n')
conn.recvuntil(b'3. Easy\n')
#conn.send(b'1\n')
conn.send(b'2\n')
conn.recvuntil(b'(y/N)\n')
#conn.send(b'y\n')
conn.send(b'N\n')

data = conn.recvuntil(b'Please input the timestamp: ')
timestamp = int(re.search(rb'\[\d+, (\d+)\]', data).group(1))
print("Timestmap:", timestamp)
conn.send(str(timestamp).encode() + b'\n')

conn.recvline()
conn.recvline()

with shelve.open('cache') as db:  # 
    for i in range(1, 101):
        conn.recvuntil(f'{i} of 100\n'.encode())
        #print(conn.recvline())

        data = conn.recvline()
        url1 = data.decode().strip().rsplit(' ', 1)[-1]

        data = conn.recvline()
        url2 = data.decode().strip().rsplit(' ', 1)[-1]

        data = conn.recvline()
        offset = re.search(r'at 0x([0-9A-Fa-f]+)', data.decode()).group(1)

        print(url1)
        print(url2)
        print(offset)

        if (answer := db.get(url1 + url2 + offset)) is None:
            urlretrieve(url1, "bin1")
            urlretrieve(url2, "bin2")

            objdump_out1 = subprocess.check_output(["objdump", "-d", "bin1"]).decode()
            objdump_out2 = subprocess.check_output(["objdump", "-d", "bin2"]).decode()

            answer = analyze(int(offset, 16), objdump_out1, objdump_out2)
            db[url1 + url2 + offset] = answer

        conn.recvuntil(b'(in hex): \n')
        conn.send(answer.encode() + b"\n")
        print(i, answer)
        #print(conn.recvline())
        #__import__("time").sleep(2)

print(conn.recv())
