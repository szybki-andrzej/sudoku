import numpy as np
import random


class Row:
    def __init__(self, num, num_options=None):
        if num_options is None:
            num_options = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        self.num = num
        self.num_options = num_options
        self.cells = []

    def add_cell(self, cell):
        self.cells.append(cell)


class Col:
    def __init__(self, num, num_options=None):
        if num_options is None:
            num_options = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        self.num = num
        self.num_options = num_options
        self.cells = []

    def add_cell(self, cell):
        self.cells.append(cell)


class Square:
    def __init__(self, num, num_options=None):
        if num_options is None:
            num_options = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        self.num = num
        self.num_options = num_options
        self.cells = []

    def add_cell(self, cell):
        self.cells.append(cell)


class Cell:
    def __init__(self, row, col, square, value=None):
        self.row = row
        self.row_num = row.num
        self.col = col
        self.col_num = col.num
        self.square = square
        self.square_num = square.num
        self.value = value

    def draw_val(self):
        try:
            self.value = random.choice(
                np.intersect1d(np.intersect1d(np.array(self.row.num_options), np.array(self.col.num_options)),
                               np.array(self.square.num_options)))
            print(self.value)
        except IndexError:
            return None
        self.row.num_options.remove(self.value)
        self.col.num_options.remove(self.value)
        self.square.num_options.remove(self.value)


rows = [Row(i) for i in range(1, 10)]
cols = [Col(i) for i in range(1, 10)]
squares = [Square(i) for i in range(1, 10)]


def square_indent(row, col):
    r = row.num
    c = col.num
    if 1 <= r <= 3 and 1 <= c <= 3:
        return 1
    elif 1 <= r <= 3 and 4 <= c <= 6:
        return 2
    elif 1 <= r <= 3 and 7 <= c <= 9:
        return 3
    elif 4 <= r <= 6 and 1 <= c <= 3:
        return 4
    elif 4 <= r <= 6 and 4 <= c <= 6:
        return 5
    elif 4 <= r <= 6 and 7 <= c <= 9:
        return 6
    elif 7 <= r <= 9 and 1 <= c <= 3:
        return 7
    elif 7 <= r <= 9 and 4 <= c <= 6:
        return 8
    elif 7 <= r <= 9 and 7 <= c <= 9:
        return 9


cells = []
for i in rows:
    for j in cols:
        sq = squares[square_indent(i, j) - 1]
        cell = Cell(i, j, sq)
        cells.append(cell)
        sq.add_cell(cell)
        i.add_cell(cell)
        j.add_cell(cell)

for i in [0, 4, 8]:
    for cell in squares[i].cells:
        cell.draw_val()

for row in rows:
    print([cell.value for cell in row.cells])
