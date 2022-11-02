import json
import typing

from permutation_group import permutation_element


def padded_binary(x: int, bit_length: int) -> str:
    binary = bin(x)[2:]
    return '0' * (bit_length - len(binary)) + binary


class Board(object):
    def __init__(self) -> None:
        self.data = [list(range(r + 1, r + 4 + 1)) for r in range(0, 16, 4)]
        self.hole_pos = 3, 3

    def execute_move(self, c: str) -> None:
        directions = {
            'U': (-1, 0),
            'L': (0, -1),
            'R': (0, 1),
            'D': (1, 0),
        }
        direction = directions[c]
        new_pos = self.hole_pos[0] + direction[0], self.hole_pos[1] + direction[1]
        assert 0 <= new_pos[0] < 4
        assert 0 <= new_pos[1] < 4
        # That's quite long!
        self.data[self.hole_pos[0]][self.hole_pos[1]], self.data[new_pos[0]][new_pos[1]] = self.data[new_pos[0]][new_pos[1]], self.data[self.hole_pos[0]][self.hole_pos[1]]
        self.hole_pos = new_pos

    def execute_moves(self, s: str) -> None:
        for c in s:
            self.execute_move(c)
        assert self.hole_pos == (3, 3)

    def is_scrambled(self) -> bool:
        for row in range(4):
            for col in range(4):
                if self.data[row][col] != row * 4 + col + 1:
                    return True
        return False

    def permutation_element(self) -> permutation_element:
        c = []
        for row in self.data:
            c.extend(row)
        c.remove(16)
        return permutation_element(15, c)

# board = Board()
# print(board.is_scrambled())
# board.execute_moves("R")
# board.execute_moves("LUR")
# board.execute_moves("LURD")
# print(board.is_scrambled())
# print(board.permutation_element().standard_tuple)
# exit()

def unified_standard_tuple(p: permutation_element) -> typing.List[typing.Sequence[int]]:
    l = []
    for t in p.standard_tuple:
        if len(t) == 1:
            continue
        l.append(tuple(sorted(t)))
    return sorted(l)


def test(x: int, branches: typing.List[typing.Tuple[int, str, str]], bit_length: int) -> bool:
    binary = list(map(int, padded_binary(x, bit_length)))
    board = Board()
    for bit_pos, moves_1, moves_0 in branches:
        board.execute_moves((moves_0, moves_1)[binary[bit_pos]])
    return board.is_scrambled()


def main() -> None:
    bit_length = 64
    obf = (bit_length > 4)
    filename = f'chals/b{bit_length}{"_obf" if obf else ""}.json'
    with open(filename) as f:
        branches = json.load(f)

    # for bit_pos, moves_1, moves_0 in branches:
    #     board = Board()
    #     board.execute_moves(moves_0)
    #     print(unified_standard_tuple(board.permutation_element()))
    #     board = Board()
    #     board.execute_moves(moves_1)
    #     print(unified_standard_tuple(board.permutation_element()))
    #     print()

    boards = [[Board(), Board()] for _ in range(bit_length)]
    for bit_pos, moves_1, moves_0 in branches:
        boards[bit_pos][0].execute_moves(moves_0)
        boards[bit_pos][1].execute_moves(moves_1)
    for bit_pos in range(bit_length):
        print(unified_standard_tuple(boards[bit_pos][0].permutation_element()))
        print(unified_standard_tuple(boards[bit_pos][1].permutation_element()))
        print()
    # No luck, for 16 only 3 strings are full permuted, all others are
    # different.
    return

    for i in range(2 ** bit_length):
        if i % 1000 == 0:
            print(i)
        # Roughly 10/s!
        if test(i, branches, bit_length):
            print(padded_binary(i, bit_length))
        # 0010111110000110


if __name__ == "__main__":
    main()
