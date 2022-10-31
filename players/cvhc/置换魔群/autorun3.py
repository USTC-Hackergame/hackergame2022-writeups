import re
import itertools
import sys
from pwn import remote
from permutation_group import permutation_element
from sympy import nextprime
from sympy.ntheory.modular import crt


def get_mod_equations(g, y):
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

    #result, _ = crt(all_m, all_v)
    #return result
    return all_m, all_v


def get_perm_elem_from_partition(parts):
    lo = 1
    res = []

    for length in parts:
        hi = lo + length - 1

        for i in range(lo, hi):
            res.append(i + 1)

        res.append(lo)
        lo = hi + 1

    return permutation_element(len(res), res)


def partition_n(n):
    plist1 = []
    plist2 = []
    sum1 = sum2 = 0

    p = 1

    while True:
        p = nextprime(p)

        if sum1 < sum2:
            if sum1 <= n - p:
                plist1.append(p)
                sum1 += p
        else:
            if sum2 <= n - p:
                plist2.append(p)
                sum2 += p

        if min(sum1, sum2) > n - p:
            break

    if n > sum(plist1):
        plist1.append(n - sum(plist1))

    if n > sum(plist2):
        plist2.append(n - sum(plist2))

    return plist1, plist2


conn = remote("202.38.93.111", 10114)

conn.recvuntil(b'Please input your token: ')
conn.sendline(sys.argv[1].encode())

conn.recvuntil(b"> your choice: ")
conn.sendline(b"3")

for i in range(15):
    conn.recvuntil(b"[+] DH public key: ")
    data = conn.recvline()
    n, = [int(x) for x in re.findall(rb'\b\d+\b', data)]

    gl = [get_perm_elem_from_partition(x) for x in partition_n(n)]

    conn.recvuntil(b"[+] The upper bound for my private key is ")
    data = conn.recvline()
    upper_bound, = [int(x) for x in re.findall(rb'\b\d+\b', data)]

    print(f"n = {n}")
    print(f"upper_bound = {upper_bound}")
    #assert math.lcm(gl[0].order(), gl[1].order()) > upper_bound

    all_m, all_v = [], []

    for r, g in enumerate(gl):
        conn.recvuntil(f"> your generator {r} (a list):".encode())

        data = str(g).encode()
        conn.sendline(data)

        conn.recvuntil(f"[+] The public key {r} : ".encode())
        data = conn.recvline()
        y_list = [int(x) for x in re.findall(rb'\b\d+\b', data)]
        y = permutation_element(n, y_list)

        m, v = get_mod_equations(g, y)
        all_m.extend(m)
        all_v.extend(v)

    secret, _ = crt(all_m, all_v)

    conn.recvuntil(b'> your answer: ')
    conn.sendline(str(secret).encode())
    print(conn.recv())
    break  # failed...

#print(conn.recvline().decode())
#conn.close()
