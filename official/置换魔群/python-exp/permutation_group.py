from random import SystemRandom
from math import lcm, factorial
from sympy import factorint
from sympy.ntheory.modular import crt

secure_prng = SystemRandom()
shuffle = secure_prng.shuffle
randint = secure_prng.randint
sample = secure_prng.sample


class permutation_element():
    p = None
    permutation_list = None  # fromat : [1,3,2,4]
    standard_tuple = None  # format : [(1),(2,3),(4)]

    def __init__(self, p, permutation_list):
        # make sure that permutation_list is a valid permutation for [1,2,3,..,p]
        self.p = p
        assert len(permutation_list) == p, "Bad list"
        self.permutation_list = permutation_list
        self.standard_tuple = self.to_standard(permutation_list)

    def __str__(self, standard=False) -> str:
        if standard:
            return str(self.standard_tuple)
        else:
            return str(self.permutation_list)

    def to_standard(self, perm_list):
        # [1,3,2,4] -> [(1),(2,3),(4)]
        standard_res = [[1]]
        i = 0
        remained = list(range(1, self.p+1))
        while True:
            if standard_res[-1][0] == perm_list[i]:
                remained.remove(perm_list[i])
                if len(remained) == 0:
                    break
                standard_res.append([remained[0]])
                i = remained[0] - 1
            else:
                standard_res[-1].append(perm_list[i])
                remained.remove(perm_list[i])
                i = perm_list[i] - 1
        return [tuple(i) for i in standard_res]

    def __mul__(self, other):
        assert self.p == other.p, "not in the same group"
        res = []
        for i in range(self.p):
            # res.append(other.permutation_list[self.permutation_list[i]-1])
            res.append(self.permutation_list[other.permutation_list[i]-1])
        return permutation_element(self.p, res)

    def __pow__(self, e: int):
        # fast exp
        res = permutation_element(self.p, list(range(1, self.p+1)))
        b = self
        if e == 0:
            # x^0 = identity for all x in A_n
            return res
        while e != 0:
            if e & 1 == 1:
                res = res * b
            e >>= 1
            b = b*b
        return res

    def __call__(self, ls):
        # ls: list or tuple, shuffle `ls` with our permutation_list
        assert len(ls) == self.p
        res = [None]*self.p
        try:
            for i in range(self.p):
                res[i] = ls[self.permutation_list[i]]
        except:
            print("Something wrong")
            return None
        return res

    def __eq__(self, other):
        return self.permutation_list == other.permutation_list

    def order(self):
        res = 1
        for i in self.standard_tuple:
            res = lcm(res, len(i))
        return res

    def log(self, base):
        # g = base, y.log(g) -> x such that base^x = y
        # make sure x exists, not fully checked
        standard_tuple_g = base.standard_tuple
        standard_tuple_y = self.standard_tuple
        crt_mods = []
        crt_consts = []

        for subgroup in standard_tuple_g:
            sub_order = len(subgroup)
            if sub_order == 1:
                # not infor for dlp
                continue
            for sg in standard_tuple_y:
                # match sg[0] and sg[1] of y's sub-element to _index0 _index1 in subgroup of g's sub-element
                # the subgroup dl is exactly _index1 - _index0
                sg_length = len(sg)
                if sg[0] in subgroup:
                    _index0 = subgroup.index(sg[0])
                else:
                    continue
                if sg_length == 1:
                    # dl = 0
                    crt_mods.append(sub_order)
                    crt_consts.append(0)
                    break
                elif sub_order % sg_length == 0:
                    if sg[1] in subgroup:
                        _index1 = subgroup.index(sg[1])
                    else:
                        print("[+] No discrete logarithm")
                        return None
                    crt_mods.append(sub_order)
                    crt_consts.append((_index1-_index0) % sub_order)
                    break
                else:
                    print("[-] No discrete logarithm")
                    return None
        return crt(crt_mods, crt_consts)[0]


class permutation_group():
    p = None

    def __init__(self, p) -> None:
        self.p = p

    def __call__(self, perm_list):
        return permutation_element(self.p, perm_list)

    def order(self):
        assert self.p < 1000000, "Order too large"
        return factorial(self.p)

    def random_element(self):
        L = list(range(1, self.p+1))
        shuffle(L)
        return permutation_element(self.p, L)

    def identity(self):
        return permutation_element(self.p, list(range(1, self.p+1)))

    def random_order_element(self, order):
        n = self.p
        factors = list(factorint(order).items())
        tuple_len = [p ** e for p, e in factors]
        assert sum(tuple_len) <= n, "impossible order"
        remained = list(range(1, n+1))
        result = [0]*n
        for tl in tuple_len:
            sub = sample(remained, tl)
            for i in range(tl):
                result[sub[i]-1] = sub[(i+1) % tl]
            remained = [x for x in remained if x not in sub]

        while result.count(0) != 0:
            sub = sample(list(remained), 1)
            result[sub[0]-1] = sub[0]
            remained = [x for x in remained if x not in sub]
        L = sorted(result)
        for i in range(1, n+1):
            assert int(i) == int(L[i-1]), f"{i}"
        return result


def test_discrete_log():
    Sp = permutation_group(1900)
    for _ in range(15):
        base = Sp.random_element()
        x = randint(1, base.order())
        y = base**x
        assert y.log(base) == x
    print("[+] Discrete logarithm is OK")


if __name__ == "__main__":
    test_discrete_log()
