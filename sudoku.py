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

    def choice(self):
        return np.intersect1d(np.intersect1d(np.array(self.row.num_options), np.array(self.col.num_options)),
                              np.array(self.square.num_options))

    def draw_val(self):
        try:
            self.value = random.choice(self.choice())
        except IndexError:
            return None
        self.row.num_options.remove(self.value)
        self.col.num_options.remove(self.value)
        self.square.num_options.remove(self.value)

    def add_value(self, value):
        if value is None:
            return False
        self.value = value
        self.row.num_options.remove(self.value)
        self.col.num_options.remove(self.value)
        self.square.num_options.remove(self.value)

    def del_value(self):
        self.row.num_options.append(self.value)
        self.row.num_options.sort()
        self.col.num_options.append(self.value)
        self.col.num_options.sort()
        self.square.num_options.append(self.value)
        self.square.num_options.sort()
        index = np.where(self.choice() == self.value)[0][0]

        self.value = None
        if len(self.choice()) == index + 1:
            return None
        else:
            return self.choice()[index+1]


rows = [Row(i) for i in range(0, 9)]
cols = [Col(i) for i in range(0, 9)]
squares = [Square(i) for i in range(0, 9)]


def square_indent(row, col):
    return (3 * (row.num // 3)) + (col.num // 3)

cells = []
for i in rows:
    for j in cols:
        sq = squares[square_indent(i, j)]
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

none_cells = [cell for cell in cells if cell.value is None]
# random.shuffle(none_cells)


def solver(n):
    if n == 54:
        return True

    elif len(none_cells[n].choice()) == 0:
        if none_cells[n].value is not None:
            none_cells[n].del_value()
        return False

    else:
        none_cells[n].add_value(none_cells[n].choice()[0])
        while solver(n+1) is False:
            if none_cells[n].add_value(none_cells[n].del_value()) is False:
                return False


solver(0)

for row in rows:
    print([cell.value for cell in row.cells])
