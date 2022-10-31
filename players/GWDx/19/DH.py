from permutation_group import permutation_element, permutation_group
from random import SystemRandom
import re
from icecream import ic
from sympy.ntheory.modular import crt
from pwn import *


def s2n(x):
    return [int(x) for x in re.findall(r"\-?\d+\.?\d*", x)]


secure_prng = SystemRandom()
sample = secure_prng.sample
randint = secure_prng.randint

# solve Congruence equation


def solve(n, raw, ans):
    eqns = set()
    # for each tuple in result
    # find it in raw
    # add an equation
    # x mod rawTupleOrder = position[1] - position[0] in resultTuple
    for i in range(len(ans.standard_tuple)):
        resultTuple = ans.standard_tuple[i]
        element0 = resultTuple[0]
        if len(resultTuple) > 1:
            element1 = resultTuple[1]
        else:
            element1 = element0
        for j in range(len(raw.standard_tuple)):
            rawTuple = raw.standard_tuple[j]
            if element0 in rawTuple:
                position0 = rawTuple.index(element0)
                position1 = rawTuple.index(element1)
                eqns.add((len(rawTuple), (position1 - position0) % len(rawTuple)))
                break
        else:
            raise Exception("Not found")

    ic(eqns)
    # solve eqns, use CRT
    allMod = []
    allRem = []
    for mod, rem in eqns:
        allMod.append(mod)
        allRem.append(rem)
    # ic(allMod)
    # ic(allRem)
    ans = crt(allMod, allRem)[0]
    ic(ans)

    return ans


def test():
    n = 10
    An = permutation_group(n)
    raw = An.random_element()
    ic(raw.standard_tuple)
    # while g.order() < 2**32:
    #     # prevent bruteforcing
    #     g = An.random_element()
    secret = randint(1, raw.order())
    ic(raw.order())
    ic(secret)
    for i in range(2, 10):
        ic((raw**i).standard_tuple)

    # for i in range(2 * raw.order()):
    #     if raw**i == raw:
    #         ic(i)
    result = raw**secret
    ans = solve(n, raw, result)
    assert ans == secret

    ic(result.standard_tuple)
    print(f"[+] DH public key: n = {n}, g = {raw}")
    print(f"[+] my public key = {result} ")
    print(f"[+] Prove that you own the secret: ")
    ans = int(input("> your answer: "))
    if ans == secret:
        print("Good job")
    else:
        print("Bad")


def communicate():
    r = remote('202.38.93.111', 10114)
    r.sendlineafter(
        'Please input your token: ',
        '1:MEUCIQC24dB6B24/LDr2O+4cifbzOEFDbkXg3hJIqTXuuvpa1QIgbzMM/F0uUmYIudtM6qEDvOpEHbtTZjSjTWMcA5zhnos= ')

    r.sendlineafter('> your choice:', '2')
    r.recvlines(2)
    for i in range(15):
        ic(i)
        allRecv = b''.join(r.recvlines(3)).decode()
        # n = 1524, g = [1, 2, ..., ]
        # my public key = [1, 2, ..., ]
        print(allRecv)
        g = re.findall(r"g = \[.*?\]", allRecv)[0]
        pub = re.findall(r"my public key = \[.*?\]", allRecv)[0]
        g = s2n(g)
        pub = s2n(pub)
        n = len(g)

        ic(n)

        raw = permutation_element(n, g)
        result = permutation_element(n, pub)

        ans = solve(n, raw, result)
        r.sendline(str(ans))

        receive5 = r.recvline().decode()
        print(receive5, end='')

    r.interactive()


test()
# communicate()
