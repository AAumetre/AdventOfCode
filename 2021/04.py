from typing import List
from typing import Callable

class Number:
    drawn: bool
    value: int

    def is_drawn(self) -> bool:
        return self.drawn

    def draw(self):
        self.drawn = True

    def val(self) -> int:
        return self.value

    def __init__(self, n):
        self.value = n
        self.drawn = False

class Board:
    numbers: List[List]
    score: int
    row_drawn: List
    col_drawn: List
    last_drawn: int

    def __init__(self, matrix: List[List]):
        self.numbers = []
        self.row_drawn = [0, 0, 0, 0, 0]
        self.col_drawn = [0, 0, 0, 0, 0]
        self.last_drawn = -1
        self.score = 0
        for i in range(len(matrix)):
            self.numbers.append([])
            for j in range(len(matrix[i])):
                self.numbers[i].append( Number(matrix[i][j]) )
    def print_combined(self) -> None:
        for i in range(len(self.numbers)):
            row = []
            for j in range(len(self.numbers[i])):
                value = self.numbers[i][j].val()
                drawn_value = (1 if self.numbers[i][j].is_drawn() else 0)
                row.append(f"({str(value).zfill(2)},{str(drawn_value)})")
            print( row )

    def compute_score(self) -> None:
        sum_unmarked = 0
        for i in range(len(self.numbers)):
            for j in range(len(self.numbers[i])):
                if not self.numbers[i][j].is_drawn():
                    sum_unmarked = sum_unmarked + self.numbers[i][j].val()
        self.score = sum_unmarked*self.last_drawn

    def update_drawn(self, row: int, col:int) -> None:
        self.row_drawn[row] += 1
        self.col_drawn[col] += 1
        for i in range(len(self.row_drawn)):
            if (self.row_drawn[i] == len(self.numbers)) or (self.col_drawn[i] == len(self.numbers)):
                self.compute_score()

    def draw(self, n: int) -> None:
        for i in range(len(self.numbers)):
            for j in range(len(self.numbers[i])):
                if self.numbers[i][j].val() == n:
                    self.numbers[i][j].draw()
                    self.last_drawn = n
                    self.update_drawn(i, j)
                    return

def transform(f: Callable, data: List) -> List:
    return [f(e) for e in data]

def main():
    f = open("04.in", "r")
    numbers_called = transform(lambda x: int(x), f.readline().split(",") )
    # Read all the boards
    board_lines = f.readlines()
    boards = []
    i = 0
    while i < len(board_lines):
        tmp = []
        for j in range(i+1, i+6):
            a_line = board_lines[j].replace("  ", " ")
            if a_line[0] == " ":
                a_line = a_line[1:]
            tmp.append(transform(lambda x: int(x), (a_line).split(" ")))
        boards.append( Board(tmp) )
        i = i+6
    f.close()

    # # Test
    # tmp1=  [[22, 13, 17, 11,  0],
    #         [8, 2, 23, 4, 24],
    #         [21, 9, 14, 16, 7],
    #         [6, 10, 3, 18, 5],
    #         [1, 12, 20, 15, 19]]
    # tmp2 = [[3, 15, 0, 2, 22],
    #         [9, 18, 13, 17, 5],
    #         [19, 8, 7, 25, 23],
    #         [20, 11, 10, 24, 4],
    #         [14, 21, 16, 12,  6]]
    # tmp3 = [[14, 21, 17, 24,  4],
    #         [10, 16, 15,  9, 19],
    #         [18,  8, 23, 26, 20],
    #         [22, 11, 13,  6,  5],
    #         [2,  0, 12,  3,  7]]
    # boards = [Board(tmp1), Board(tmp2), Board(tmp3)]
    # numbers_called = [7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1]

    # for n in numbers_called:
    for i in range(len(numbers_called)):
        n = numbers_called[i]
        print(f"Calling number {n}")
        winning_board = []
        for board in boards:
            board.draw( n )
        for board in boards:
            if board.score > 0:
                print(f"board wins with {board.score} points, when number {n} was called")
                board.print_combined()
                last_score = board.score
                winning_board.append( board )
        for b in winning_board:
            boards.remove( b )
    print(f"Last score is: {last_score}")
    # #Expected answer 188*24 = 4512


main()
