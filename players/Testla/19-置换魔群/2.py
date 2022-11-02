import itertools
import pwn
import sys
import typing

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


def solve_two_moduli(a: typing.Tuple[int, int], b: typing.Tuple[int, int]) -> typing.Tuple[int, int]:
    ma, mb, r, _, _ = extended_gcd(a[0], b[0])
    # print(f'before {a[0]=} {b[0]=} {ma=} {mb=}')
    if ma < 0:
        ma += b[0]
    if mb < 0:
        mb += a[0]
    # print(f'after {a[0]=} {b[0]=} {ma=} {mb=}')
    new_length = a[0] * b[0]
    new_remainder = (a[1] * mb * b[0] + b[1] * ma * a[0]) % new_length
    # Section "Generalization to non-coprime moduli"
    return new_length // r, new_remainder // r


def sol(g: permutation_element, y: permutation_element) -> int:
    # {(length, remainer)}
    modulis = set()
    for t in g.standard_tuple:
        remainder = t.index(y.permutation_list[t[0] - 1])
        modulis.add((len(t), remainder))
    print(f'{modulis=}')
    ans = modulis.pop()
    while True:
        try:
            m = modulis.pop()
        except KeyError:
            break
        else:
            print(f'{ans=} {m=}')
            ans = solve_two_moduli(ans, m)
            print(f'{ans=}')
    remainder = ans[1]
    return g.order() if remainder == 0 else remainder


# l = [2, 3, 1]
# l = [2, 3, 4, 5, 1]
# l = [2, 1, 4, 5, 3]
# l = [i + 1 for i in range(11)]
# import random
# random.shuffle(l)
# # l = [1, 3, 2, 7, 4, 5, 6]
# l = [2, 1, 10, 11, 9, 6, 7, 5, 8, 4, 3]
# e = permutation_element(len(l), l)
# for i in range(len(l)):
#     a = e ** i
#     print(i, a, a.standard_tuple)
#     # print(sol(e, a))
#     assert(sol(e, a) % e.order() == i % e.order()), f'{sol(e, a)=} {i=}'
# exit()



def main() -> None:
    token = b'<Redacted>'
    e = 65537

    pwn.context(log_level='debug')
    c = pwn.remote('202.38.93.111', 10114)
    if len(sys.argv) > 0:  # Pylance deems code following sendline to be unreachable
        c.sendlineafter(b'Please input your token: ', token)
    print('sent token')
    choice = b'2'
    if len(sys.argv) > 0:  # Pylance deems code following sendline to be unreachable
        c.sendlineafter(b'> your choice: ', choice)
    for _ in range(15):
        c.recvuntil(b'g = ')
        g = eval(c.recvline().decode())
        g = permutation_element(len(g), g)
        c.recvuntil(b'[+] my public key = ')
        y = eval(c.recvline().decode())
        y = permutation_element(len(y), y)
        print(f'{g.order()=}')

        c.sendline(str(sol(g, y)).encode())
    print(c.recvall())


if __name__ == "__main__":
    main()
