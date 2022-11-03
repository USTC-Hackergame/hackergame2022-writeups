import sys
import re
import ast
import itertools
import subprocess

from permutation_group import permutation_group, permutation_element
from chinese_remainder import chinese_remainder_theorem


def solve(n: int, encrypted: permutation_element) -> list[int]:
    e = 65537

    new_std = []
    for loop in encrypted.standard_tuple:
        length = len(loop)
        print(f"{length = },\t{e % length = }")
        steps = e % length

        if length == 1:
            new_std.append(loop)
            continue

        ## for (A, B, C, D, E), steps=2, solve where B is:
        # >>> 2 * 3 % 5
        # 1
        # >>> 2 * 3 == 5 * 1 + 1 == 6
        # True
        # >>> chinese_remainder_theorem(2, 0, 5, 1)
        # 6
        ## so B is on index 3 == 6 // 2
        ## (A, C, E, B, D)
        index = chinese_remainder_theorem(steps, 0, length, 1) // steps

        new_loop = []
        i = 0
        while len(new_loop) < length:
            new_loop.append(loop[i])
            i = (i + index) % length

        new_std.append(tuple(new_loop))

    secret_list = [None] * n
    for loop in new_std:
        for i, j in itertools.pairwise(loop + (loop[0],)):
            secret_list[i-1] = j

    return secret_list


def main():
    for i in range(15):
        # n = input("n: ")
        encrypted = ast.literal_eval(input(f"{i:2d} encrypted: ").strip())
        result = solve(len(encrypted),
                       permutation_element(len(encrypted), encrypted))
        print("-" * 60)
        print(result)
        print()


if __name__ == "__main__":
    main()
