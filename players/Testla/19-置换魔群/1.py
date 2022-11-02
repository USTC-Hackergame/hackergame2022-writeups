import itertools
import pwn

from math import lcm
from permutation_group import permutation_element, permutation_group


def extended_gcd(a: int, b: int):
    swapped = False
    if a < b:
        a, b = b, a
        swapped = True
    old_r, r = a, b
    old_s, s = 1, 0
    old_t, t = 0, 1
    while r != 0:
        q = old_r // r
        old_r, r = r, old_r - q * r
        old_s, s = s, old_s - q * s
        old_t, t = t, old_t - q * t
    if swapped:
        return old_t, old_s, old_r, s, t
    else:
        return old_s, old_t, old_r, t, s

# print(extended_gcd(5, 14))
# exit()


def main() -> None:
    token = b'<Redacted>'
    e = 65537

    pwn.context(log_level='debug')
    c = pwn.remote('202.38.93.111', 10114)
    c.sendlineafter(b'Please input your token: ', token)
    print('sent token')
    choice = b'1'
    c.sendlineafter(b'> your choice: ', choice)
    for _ in range(15):
        c.recvuntil(b'[+] my encrypted secret is here: \n')
        # print(c.recvlines(2))
        s = c.recvline().decode()
        print(s)
        l = eval(s)
        elem = permutation_element(len(l), l)
        tuple_lengths = [len(t) for t in elem.standard_tuple]
        m = lcm(*tuple_lengths)
        print(f'{m=}')
        # This is too slow
        # k = next(k for k in itertools.count(1) if e * k % m == 1)
        # https://en.wikipedia.org/wiki/Extended_Euclidean_algorithm
        k = extended_gcd(e, m)[0]
        if k < 0:
            k += m
        print(f'{k=}')
        ans = str(elem ** k)
        print('sending answer')
        print(ans)
        c.sendline(ans.encode())
        # print(c.recvlines(2))
    print(c.recvall())
    return


if __name__ == "__main__":
    main()
