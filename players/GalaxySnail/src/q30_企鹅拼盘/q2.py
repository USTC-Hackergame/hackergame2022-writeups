import sys
import json

from tqdm import tqdm


# BP.py
class Board:
    def __init__(self):
        self.b = [[None] * 4 for i in range(4)]
        self.reset()

    def _blkpos(self):
        for i in range(4):
            for j in range(4):
                if self.b[i][j] == 15:
                    return (i, j)

    def reset(self):
        for i in range(4):
            for j in range(4):
                self.b[i][j] = i*4 + j

    def move(self, moves):
        for m in moves:
            i, j = self._blkpos()
            if m == 'L':
                self.b[i][j] = self.b[i][j-1]
                self.b[i][j-1] = 15
            elif m == 'R':
                self.b[i][j] = self.b[i][j+1]
                self.b[i][j+1] = 15
            elif m == 'U':
                self.b[i][j] = self.b[i-1][j]
                self.b[i-1][j] = 15
            else:
                self.b[i][j] = self.b[i+1][j]
                self.b[i+1][j] = 15

    def __bool__(self):
        for i in range(4):
            for j in range(4):
                if self.b[i][j] != i*4 + j:
                    return True
        return False


def code_iter(bits: int):
    for n in range(1 << bits):
        yield [bool(n & (1 << i)) for i in range(bits)]


def main(jsonfilename, bitlength):
    bitlength = int(bitlength)
    with open(jsonfilename, encoding="utf-8") as f:
        branches = json.load(f)

    board = Board()
    for inbits in tqdm(list(code_iter(bitlength))):
        board.reset()
        for branch in branches:
            if inbits[branch[0]]:
                board.move(branch[1])
            else:
                board.move(branch[2])

        if board:
            print()
            print("".join("1" if bit else "0" for bit in inbits))
            # 0010111110000110
            break


if __name__ == "__main__":
    main(*sys.argv[1:3])
