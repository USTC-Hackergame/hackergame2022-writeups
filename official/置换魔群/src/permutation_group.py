from random import SystemRandom
from math import lcm, factorial

secure_prng = SystemRandom()
shuffle = secure_prng.shuffle

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
