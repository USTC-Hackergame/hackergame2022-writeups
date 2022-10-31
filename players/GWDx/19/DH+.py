from permutation_group import permutation_element, permutation_group
from math import lcm
from random import SystemRandom
import re
from icecream import ic
import sympy
from sympy.ntheory.modular import crt
from pwn import *


def s2n(x):
    return [int(x) for x in re.findall(r"\-?\d+\.?\d*", x)]


secure_prng = SystemRandom()
sample = secure_prng.sample
randint = secure_prng.randint

# solve Congruence equation

eqns = {}


def addEqn(n, raw, ans):
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
                eqns[len(rawTuple)] = (position1 - position0) % len(rawTuple)
                break
        else:
            raise Exception("Not found")


def solveEqn(n, pri_bound):
    allMod = []
    allRem = []
    global eqns
    ic(str(eqns))
    for mod, rem in eqns.items():
        allMod.append(mod)
        allRem.append(rem)
    ic(pri_bound)
    ic(lcm(*allMod))
    # val = pri_bound / lcm(*allMod), use highest precision
    val = pri_bound / lcm(*allMod)
    ic(val)
    assert val <= 1.5
    ans = crt(allMod, allRem)[0]
    ic(ans)
    eqns = {}
    return ans


def genPrimePermutation(primeList, n):
    # generate a permutation with prime order
    # primeList: list of prime numbers
    # len: length of permutation
    # return: permutation

    result = []
    for prime in primeList:
        currentIndex = len(result) + 1
        # prime = 3
        # [2, 3, 1]
        primePermutation = [i for i in range(currentIndex + 1, currentIndex + prime)] + [currentIndex]
        result += primePermutation
    currentLen = len(result)
    if currentLen < n:
        result += [i for i in range(currentLen + 1, n + 1)]
    ic(len(result))
    assert len(result) == n
    # print(result)
    return permutation_element(n, result)


def selectPrimesGen(primeList, n, notInclude, append):
    total = 0
    for i in range(1000):
        total += primeList[i]
        if total >= n * 2:
            if notInclude:
                two = primeList[:i - 1]
            else:
                two = primeList[:i]
            break
    # ic(two)
    two = two + append
    # reverse sort
    two.sort(reverse=True)
    # print(two)
    # generate two prime list length n
    primeList1 = []
    primeList2 = []
    for i in two:
        sumPrimeList1 = sum(primeList1)
        sumPrimeList2 = sum(primeList2)
        if sumPrimeList1 < sumPrimeList2 and sumPrimeList1 + i <= n:
            add = True
            for j in primeList1:
                if j % i == 0:
                    add = False
            if add:
                primeList1.append(i)
        elif sumPrimeList2 + i <= n:
            add = True
            for j in primeList2:
                if j % i == 0:
                    add = False
            if add:
                primeList2.append(i)
    # ic(str(primeList1))
    # ic(sum(primeList1))
    # ic(str(primeList2))
    # ic(sum(primeList2))
    return primeList1, primeList2


def selectPrimes(primeList, n):
    # get a selectPrimes, lcm max
    allSelectPrimes = [
        selectPrimesGen(primeList, n, True, []),
        selectPrimesGen(primeList, n, False, []),
        selectPrimesGen(primeList, n, True, [64, 49, 27, 25]),
        selectPrimesGen(primeList, n, False, [64, 49, 27, 25]),
        selectPrimesGen(primeList, n, True, [64, 49, 27, 25, 16]),
        selectPrimesGen(primeList, n, False, [64, 49, 27, 25, 16]),
        selectPrimesGen(primeList, n, True, [64, 27, 25]),
        selectPrimesGen(primeList, n, False, [64, 27, 25]),
        selectPrimesGen(primeList, n, True, [64, 27, 25, 16]),
        selectPrimesGen(primeList, n, False, [64, 27, 25, 16]),
        selectPrimesGen(primeList, n, True, [64, 16, 49, 27, 25]),
        selectPrimesGen(primeList, n, False, [64, 16, 49, 27, 25]),
        selectPrimesGen(primeList, n, True, [64, 27, 25]),
        selectPrimesGen(primeList, n, False, [64, 27, 25]),
        selectPrimesGen(primeList, n, True, [64, 27, 25, 16]),
        selectPrimesGen(primeList, n, False, [64, 27, 25, 16]),
        selectPrimesGen(primeList, n, True, [32, 49, 27, 25]),
        selectPrimesGen(primeList, n, False, [32, 49, 27, 25]),
        selectPrimesGen(primeList, n, True, [32, 16, 49, 27, 25]),
        selectPrimesGen(primeList, n, False, [32, 16, 49, 27, 25]),
        selectPrimesGen(primeList, n, True, [32, 27, 25]),
        selectPrimesGen(primeList, n, False, [32, 27, 25]),
        selectPrimesGen(primeList, n, True, [16, 49, 27, 25]),
        selectPrimesGen(primeList, n, False, [16, 49, 27, 25]),
        selectPrimesGen(primeList, n, True, [16, 27, 25]),
        selectPrimesGen(primeList, n, False, [16, 27, 25]),
        selectPrimesGen(primeList, n, True, [8, 49, 27, 25]),
        selectPrimesGen(primeList, n, False, [8, 49, 27, 25]),
        selectPrimesGen(primeList, n, True, [8, 27, 25]),
        selectPrimesGen(primeList, n, False, [8, 27, 25]),
        selectPrimesGen(primeList, n, True, [4, 49, 27, 25]),
        selectPrimesGen(primeList, n, False, [4, 49, 27, 25]),
        selectPrimesGen(primeList, n, True, [4, 27, 25]),
        selectPrimesGen(primeList, n, False, [4, 27, 25]),
        selectPrimesGen(primeList, n, True, [49, 27, 25]),
        selectPrimesGen(primeList, n, False, [49, 27, 25]),
    ]
    allLcm = [lcm(*(x[0] + x[1])) for x in allSelectPrimes]
    # ic(allLcm)
    maxLcm = max(allLcm)
    result = allSelectPrimes[allLcm.index(maxLcm)]

    ic(str(result))
    # delete useless factors
    # if mod 64, then 16 and 8, 4, 2 are useless
    # if mod 49, then 7 is useless
    return result


# use sympy to generate primes
primeList = list(sympy.primerange(1, 1000))
primes1, primes2 = selectPrimes(primeList, 17)

r = remote('202.38.93.111', 10114)
r.sendlineafter('Please input your token: ',
                '1:MEUCIQC24dB6B24/LDr2O+4cifbzOEFDbkXg3hJIqTXuuvpa1QIgbzMM/F0uUmYIudtM6qEDvOpEHbtTZjSjTWMcA5zhnos= ')

r.sendlineafter('> your choice:', '3')
r.recvlines(2)
for i in range(15):
    ic(i)
    allRecv = b'\n'.join(r.recvlines(4)).decode()
    # DH public key: n = 1697
    # The upper bound for my private key is 86687174616060958074047359828774537048339805273814310049489208345302121941
    n = int(re.findall(r"n = (\d+)", allRecv)[0])
    pri_bound = int(re.findall('The upper bound for my private key is (\d+)', allRecv)[0])

    ic(n)

    print(allRecv)

    primeList = list(sympy.primerange(1, 1000))
    primes1, primes2 = selectPrimes(primeList, n)

    ic(lcm(*(primes1 + primes2)))
    raw1 = genPrimePermutation(primes1, n)
    raw2 = genPrimePermutation(primes2, n)

    r.sendline(str(raw1))
    recv1 = r.recvline().decode()

    # The public key 0 : [66, 350, ... ]
    target1 = s2n(re.findall(r"The public key 0 : (\[.*\])", recv1)[0])
    target1 = permutation_element(n, target1)
    ic(raw1.permutation_list[:10])
    ic(target1.permutation_list[:10])

    r.sendline(str(raw2))
    recv2 = r.recvline().decode()
    ic(raw2.permutation_list[:10])
    target2 = s2n(re.findall(r"The public key 1 : (\[.*\])", recv2)[0])
    target2 = permutation_element(n, target2)
    ic(target2.permutation_list[:10])

    addEqn(n, raw1, target1)
    addEqn(n, raw2, target2)

    ans = solveEqn(n, pri_bound)
    r.sendline(str(ans))

    receive5 = r.recvline().decode()
    print(receive5, end='')

r.interactive()
