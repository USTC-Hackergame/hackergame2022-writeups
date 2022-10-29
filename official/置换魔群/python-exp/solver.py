import operator
from Crypto.Util.number import *
from sympy import primerange, factorint,prod
from tqdm import tqdm
from pwn import *
import pickle
from math import lcm
import re
from permutation_group import permutation_element,permutation_group
from random import sample
from sympy.ntheory.modular import crt

s2n = lambda x: [int(x) for x in re.findall(r"\-?\d+\.?\d*",x)]
factor = lambda x: list(factorint(x).items())

# modified from [A000793](http://oeis.org/A000793)
# compute terms a(0)..a(2*N) with items < N
def aupton_2n(N): 
    V = [1 for j in range(2*N+1)]
    for i in primerange(2, N+1):
        for j in range(2*N, i-1, -1):
            hi = V[j]
            pp = i
            while pp <= j:
                hi = max((pp if j == pp else V[j-pp]*pp), hi)
                pp *= i
            V[j] = hi
    return V


'''
Wikipedia subset sum approximation algorithm
http://en.wikipedia.org/wiki/Subset_sum_problem#Polynomial_time_approximate_algorithm
'''
def approx_with_accounting_and_duplicates(x_list, s):
    c = .01              # fraction error (constant)
    N = len(x_list)      # number of values

    S = [(0, [])]
    for x in sorted(x_list):
        T = []
        for y, y_list in S:
            T.append((x + y, y_list + [x]))
        U = T + S
        U = sorted(U, key=operator.itemgetter(0))
        y, y_list = U[0]
        S = [(y, y_list)]

        for z, z_list in U:
            lower_bound = (float(y) + c * float(s) / float(N))
            if lower_bound < z <= s:
                y = z
                S.append((z, z_list))

    return sorted(S, key=operator.itemgetter(0))[-1]


def split_2n(n, order):
    num_set = set([p ** e for p, e in list(factorint(order).items())])
    target_sum = n
    sum1, prime_list1 = approx_with_accounting_and_duplicates(
        num_set, target_sum)
    prime_list2 = num_set - set(prime_list1)
    sum2 = sum(prime_list2)
    if sum1 <= target_sum and sum2 <= target_sum:
        return prod(prime_list1), prod(prime_list2)
    else:
        print("[+] no solution")
        return None


def Landu_expand(n, all_solu=False):
    order = aupton_2n(n)
    if not all_solu:
        return split_2n(n, order[-1])
    res = [1, 1]
    for i in tqdm(range(2, 2*n+1, 2)):
        res.append(split_2n(i, order[i]))
    return res


io =  remote("202.38.93.111",10114)
token = "819:MEQCIF5Ohbnr1w9u3xhZE6fM8qZjDjbi7BgIa0ammpOdASt6AiBaFF4YoiOD1eYhB+dP8wrcqYJTF8MIplFGIO3Y29Xffw=="
io.sendlineafter(b"Please input your token: ",token.encode())

def solve1():
    io.sendlineafter(b"> your choice: ", b"1")
    for _ in range(15):
        io.recvuntil(b"[+] RSA public key: ")
        n,e = s2n(io.recvline().decode().strip())
        G = permutation_group(n)
        io.recvline()
        enc = G(s2n(io.recvline().decode().strip()))
        phi = enc.order()
        s = enc**(inverse(e,phi))
        io.sendlineafter(b"> your answer: ",str(s.permutation_list).encode())
        print(io.recvline())
    print(io.recvline())
    
# solve1()   

def solve2():
    io.sendlineafter(b"> your choice: ", b"2")
    for _ in range(15):
        io.recvuntil(b"DH public key: ")
        PubKey = s2n(io.recvline().decode().strip())
        n,g = PubKey[0],PubKey[1:]
        G = permutation_group(n)
        g = G(g)
        Y = G(s2n(io.recvline().decode().strip()))
        secret = Y.log(g) 
        print(f"[+] crack secrete: {secret}")
        io.sendlineafter(b"> your answer: ",str(secret).encode())
        print(io.recvline())
    print(io.recvline())
    
def random_perm(n,order):
    factors = factor(order)
    tuple_len = [p**e for p,e in factors]
    remained = list(range(1,n+1))
    result = [0]*n
    for tl in tuple_len:
        sub = sample(remained,tl)
        for i in range(tl):
            result[sub[i]-1]=sub[(i+1)%tl]
        remained = [x for x in remained if x not in sub]
        
    while result.count(0)!=0:
        sub = sample(list(remained),1)
        result[sub[0]-1]=sub[0]
        remained = [x for x in remained if x not in sub]
    L = sorted(result)
    for i in range(1,n+1):
        assert int(i) == int(L[i-1]),f"{i}"
    return result
        
    
def solve3():
    io.sendlineafter(b"> your choice: ", b"3")
    for _ in range(15):
        io.recvuntil(b"DH public key: ")
        n = s2n(io.recvline().decode().strip())[0]
        G = permutation_group(n)
        secret_bound = s2n(io.recvline().decode().strip())[0]
        # order1,order2 = max_order_element_combine(n,2)
        order1,order2 = Landu_expand(n)
        print(f"[+] crack with probability {int(lcm(order1,order2))/int(secret_bound)}")
        # g1 = random_perm(n,order1)
        # g2 = random_perm(n,order2)
        g1 = G.random_order_element(order1)
        g2 = G.random_order_element(order2)
        io.sendlineafter(b"(a list): ",str(g1).encode())  
        Y1 = s2n(io.recvline().decode().strip())[1:]
        io.sendlineafter(b"(a list): ",str(g2).encode())
        Y2 = s2n(io.recvline().decode().strip())[1:]
        Y1,g1,Y2,g2 = G(Y1),G(g1),G(Y2),G(g2)
        dlp1 = Y1.log(g1)
        dlp2 = Y2.log(g2)
        assert g1**dlp1 == Y1
        assert g2**dlp2 == Y2
        recovered_secrert = crt([order1,order2],[dlp1,dlp2])[0]
        io.sendlineafter(b"> your answer: ",str(recovered_secrert).encode())
        print(io.recvline())
    print(io.recvline())


solve1()
solve2()
solve3()