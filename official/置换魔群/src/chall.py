from permutation_group import permutation_element, permutation_group
from math import factorial
import pickle
from random import SystemRandom
import re

secure_prng = SystemRandom()
sample = secure_prng.sample
randint = secure_prng.randint


# s2n = lambda x: [int(x) for x in re.findall(r"\-?\d+\.?\d*",x)]
def s2n(x): return [int(x) for x in re.findall(r"\-?\d+\.?\d*", x)]

# n_bounds is a list like [(1,2),(4,6),...,(n,n_bound)] for DH_plus_challenge
# n is the length of the permutation group A_n
# n_bound is the private key's uppper bound for DH_plus_challenge
n_bounds = pickle.load(open("./n_bounds.pickle", "rb"))


def RSA_challenge_for_free():
    print("Since the order of the permutation group can be computed easily, the RSA cryptography is not safe in this gruop.")
    print("Anyway, I decide to give this flag to you for free. Just get it!")

    for _ in range(15):
        n = randint(2**9, 2**10)
        An = permutation_group(n)
        secret = An.random_element()
        e = 65537
        print(f"[+] RSA public key: n = {n}, e = {e}")
        print(f"[+] my encrypted secret is here: ")
        print(secret**e)
        print(f"[+] Prove that you own the secret (a list like [1,2,3]): ")
        ans_list = s2n(input("> your answer: "))
        ans = permutation_element(n, ans_list)
        if ans == secret:
            print("Good job")
        else:
            print("Bad")
            return
    print(open("./flag1", "r").read())


def DH_challenge():
    print("Since permutation group's order is super large, I believe the discrete logarithm problem is hard to solve in this group.")
    print("Therefore I plan to implement the DH protocol in this magic group.")
    print("Now, go and crack my private key!")

    for i in range(15):
        n = randint(2**10, 2**11)
        An = permutation_group(n)
        g = An.random_element()
        while g.order() < 2**32:
            # prevent bruteforcing
            g = An.random_element()
        secret = randint(1, g.order())
        y = g**secret
        print(f"[+] DH public key: n = {n}, g = {g}")
        print(f"[+] my public key = {y} ")
        print(f"[+] Prove that you own the secret: ")
        ans = int(input("> your answer: "))
        if ans == secret:
            print("Good job")
        else:
            print("Bad")
            return
    print(open("./flag2", "r").read())


def DH_plus_challenge():
    print("Seems something wrong? It doesn't matter, I'll make my private key so bbbbbbig!")
    print("You have no way to get it even though you have two chances.")
    print("Now, go and crack my big private key!")

    chall_samples = sample(n_bounds, 15)
    for chall in chall_samples:
        n, pri_bound = chall[0], chall[1]
        secret = randint(1, pri_bound)
        print(f"[+] DH public key: n = {n}")
        print(f"[+] The upper bound for my private key is {pri_bound}")
        print(f"[+] Now you can choose the generator twice!")
        for _ in range(2):
            g = permutation_element(
                n, s2n(input(f"> your generator {_} (a list): ")))
            print(f"[+] The public key {_} : {g**secret}")
        print(f"[+] Prove that you own the secret: ")
        ans = int(input("> your answer: "))
        if ans == secret:
            print("Good job")
        else:
            print("Bad")
            return
    print(open("./flag3", "r").read())


banner = """
Hi, welcome to permutation world. Choose one challenge to solve.
> 1. RSA in permutation group.
> 2. DHKE in permutation group.
> 3. DHKE++ in permutation group.
> other: exit()
"""

while True:
    print(banner)
    try:
        choice = int(input("> your choice: "))
    except:
        print("Must be a digit number")
        continue
    if choice == 1:
        RSA_challenge_for_free()
    elif choice == 2:
        DH_challenge()
    elif choice == 3:
        DH_plus_challenge()
    else:
        exit()
