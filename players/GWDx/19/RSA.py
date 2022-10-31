from permutation_group import permutation_element, permutation_group
from math import factorial
import re
from icecream import ic
from pwn import *
import gmpy2


def s2n(x):
    return [int(x) for x in re.findall(r"\-?\d+\.?\d*", x)]


r = remote('202.38.93.111', 10114)
r.sendlineafter('Please input your token: ',
                '1:MEUCIQC24dB6B24/LDr2O+4cifbzOEFDbkXg3hJIqTXuuvpa1QIgbzMM/F0uUmYIudtM6qEDvOpEHbtTZjSjTWMcA5zhnos= ')

# send 1
r.sendlineafter('> your choice:', '1')
r.recvlines(2)
for i in range(15):
    ic(i)
    receive1 = r.recvline().decode()
    receive2 = r.recvline().decode()
    receive3 = r.recvline().decode()
    receive4 = r.recvline().decode()
    print(receive1 + receive2 + receive3 + receive4, end='')
    # print(receive)
    n = int(re.findall(r'n = (\d+)', receive1)[0])
    e = 65537
    # ic(n)
    rawPublic = re.findall(r'\[(?:\d|\s|,)+\]', receive3)[0]
    publicList = s2n(rawPublic)
    assert len(publicList) == n

    public = permutation_element(n, publicList)
    # ic(totalPermutation)
    # evaluate mod-1
    ans = gmpy2.invert(e, public.order())
    secret = public**ans

    # ic(secret.permutation_list)
    r.sendline(str(secret.permutation_list))

    receive5 = r.recvline().decode()
    print(receive5, end='')

r.interactive()
