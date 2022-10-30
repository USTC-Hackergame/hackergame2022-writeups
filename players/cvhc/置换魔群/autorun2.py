import re
import sys
from pwn import remote
from permutation_group import permutation_element
from sympy.ntheory.modular import crt


def calc(g, y):
    all_v = []
    all_m = []

    for subp in g.standard_tuple:
        n_mapping = dict()
        res2 = []

        for i, n in enumerate(subp, start=1):
            n_mapping[n] = i
            res2.append(y.permutation_list[n - 1])

        res1 = list(range(2, len(subp) + 1))
        res1.append(1)

        res2 = [n_mapping[i] for i in res2]

        p1 = permutation_element(len(subp), res1)
        p2 = permutation_element(len(subp), res2)

        acc = p1

        for i in range(p1.order()):
            if acc == p2:
                all_v.append(i + 1)
                all_m.append(p1.order())

            acc = acc * p1

    result, _ = crt(all_m, all_v)
    return result


conn = remote("202.38.93.111", 10114)

conn.recvuntil(b'Please input your token: ')
conn.sendline(sys.argv[1].encode())

conn.recvuntil(b"> your choice: ")
conn.sendline(b"2")

for i in range(15):
    conn.recvuntil(b"[+] DH public key: ")
    data = conn.recvline()
    n, *g_list = [int(x) for x in re.findall(rb'\b\d+\b', data)]

    conn.recvuntil(b"[+] my public key = ")
    data = conn.recvline()
    y_list = [int(x) for x in re.findall(rb'\b\d+\b', data)]

    g = permutation_element(n, g_list)
    y = permutation_element(n, y_list)
    secret = calc(g, y)
    print(secret)

    conn.sendline(str(secret).encode())
    conn.recvuntil(b"> your answer: Good job\n")

print(conn.recvline().decode())
conn.close()
