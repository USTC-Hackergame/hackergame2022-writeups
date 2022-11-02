import pwn
import random
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
    # print(f'{modulis=}')
    ans = modulis.pop()
    while True:
        try:
            m = modulis.pop()
        except KeyError:
            break
        else:
            # print(f'{ans=} {m=}')
            ans = solve_two_moduli(ans, m)
            # print(f'{ans=}')
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


primes = [2]

def gen_primes(n: int) -> None:
    for i in range(3, n + 1):
        if (all(i % prime != 0 for prime in primes)):
            primes.append(i)

gen_primes(1000)


def prime_factors(x: int) -> typing.List[int]:
    l = []
    for prime in primes:
        f = 1
        while x % prime == 0:
            f *= prime
            x //= prime
        if f != 1:
            l.append(f)
        if x == 1:
            break
    return l


Landau = []
with open('b000793-head_4000.txt', 'r') as f:
    for line in f:
        Landau.append(int(line.split()[1]))
# for i in range(27, 30 + 1):
#     print(i, prime_factors(Landau[i]))
# exit()


def find_two_prime_sets(n: int) -> typing.Tuple[typing.List[int], typing.List[int]]:
    for s in range(2 * n, -1, -1):
        a = []
        b = []
        sum_a = 0
        factors = list(sorted(prime_factors(Landau[s])))
        for factor in reversed(factors):
            if sum_a + factor <= n:
                a.append(factor)
                sum_a += factor
            else:
                b.append(factor)
        if sum(b) <= n:
            break
    print(f'{a=}, {sum(a)=}')
    print(f'{b=}, {sum(b)=}')
    return a, b


# find_two_prime_groups(1266)

def make_generator(lengths: typing.Sequence[int], n: int) -> typing.List[int]:
    l = []
    begin = 0
    for length in lengths:
        for i in range(length):
            l.append((i + 1) % length + begin + 1)
        begin += length
    for i in range(len(l), n):
        l.append(i + 1)
    return l

# print(make_generator((2,3,4)))
# a, b = find_two_prime_groups(1266)
# a = permutation_element(1266, make_generator(a, 1266))
# b = permutation_element(1266, make_generator(b, 1266))
# print(a.order() * b.order())
# exit()


def main() -> None:
    token = b'<Redacted>'
    e = 65537

    pwn.context(log_level='debug')
    c = pwn.remote('202.38.93.111', 10114)
    if len(sys.argv) > 0:  # Pylance deems code following sendline to be unreachable
        c.sendlineafter(b'Please input your token: ', token)
    # print('sent token')

    choice = b'3'
    if len(sys.argv) > 0:  # Pylance deems code following sendline to be unreachable
        c.sendlineafter(b'> your choice: ', choice)

    for _ in range(15):
        c.recvuntil(b'n = ')
        n = eval(c.recvline().decode())
        c.recvuntil(b'[+] The upper bound for my private key is ')
        pri_bound = eval(c.recvline().decode())

        g1, g2 = (permutation_element(n, make_generator(ls, n)) for ls in find_two_prime_sets(n))
        product = g1.order() * g2.order()
        print(f'{g1.order()=} {g2.order()=} {product=}')
        # Sometime product >= pri_bound is still false
        assert product * 2 >= pri_bound

        if len(sys.argv) > 0:  # Pylance deems code following sendline to be unreachable
            c.sendline(str(g1).encode())
        c.recvuntil(b'[+] The public key ')
        c.recvuntil(b' : ')
        pub1 = eval(c.recvline().decode())
        pub1 = permutation_element(n, pub1)
        if len(sys.argv) > 0:  # Pylance deems code following sendline to be unreachable
            c.sendline(str(g2).encode())
        c.recvuntil(b'[+] The public key ')
        c.recvuntil(b' : ')
        pub2 = eval(c.recvline().decode())
        pub2 = permutation_element(n, pub2)

        s1 = sol(g1, pub1)
        s2 = sol(g2, pub2)
        ans = solve_two_moduli((g1.order(), s1), (g2.order(), s2))[1]
        if len(sys.argv) > 0:  # Pylance deems code following sendline to be unreachable
            c.sendline(str(ans).encode())

        result = c.recvlines(2)
        print(result)
        result = not result[1].endswith(b'Bad')
        print(result)
        if not result:
            # We lost
            break
    print(c.recvuntil(b'choice'))


if __name__ == "__main__":
    main()
