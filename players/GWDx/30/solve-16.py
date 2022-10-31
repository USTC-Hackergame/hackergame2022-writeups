import json
import itertools
from icecream import ic
import time


class Board:
    def __init__(self):
        self.b = [[i * 4 + j for j in range(4)] for i in range(4)]

    def _blkpos(self):
        for i in range(4):
            for j in range(4):
                if self.b[i][j] == 15:
                    return (i, j)

    def reset(self):
        for i in range(4):
            for j in range(4):
                self.b[i][j] = i * 4 + j

    def move(self, moves):
        for m in moves:
            i, j = self._blkpos()
            if m == 'L':
                self.b[i][j] = self.b[i][j - 1]
                self.b[i][j - 1] = 15
            elif m == 'R':
                self.b[i][j] = self.b[i][j + 1]
                self.b[i][j + 1] = 15
            elif m == 'U':
                self.b[i][j] = self.b[i - 1][j]
                self.b[i - 1][j] = 15
            else:
                self.b[i][j] = self.b[i + 1][j]
                self.b[i + 1][j] = 15

    def __bool__(self):
        for i in range(4):
            for j in range(4):
                if self.b[i][j] != i * 4 + j:
                    return True
        return False


def run(bitlength, inputString):
    board = Board()
    filename = f'chals/b{bitlength}.json'
    with open(filename) as f:
        branches = json.load(f)
    assert len(branches) == bitlength**2

    for i in range(len(branches)):
        if inputString[branches[i][0]] == '1':
            board.move(branches[i][1])
        else:
            board.move(branches[i][2])
    return board


startTime = time.time()


def main():
    bitlength = 16
    # generate 0000, ..., 1111
    allPossibleInputs = [''.join(x) for x in itertools.product('01', repeat=bitlength)]
    count = 0
    for inputString in allPossibleInputs:
        board = run(bitlength, inputString)
        if board:
            ic(inputString)
        count += 1
        duration = time.time() - startTime
        if count % 1000 == 0:
            ic(count, duration)


main()
