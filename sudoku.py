import numpy as np
import random


class Board:
    def __init__(self):
        self.rows = [Row(i) for i in range(9)]
        self.cols = [Col(i) for i in range(9)]
        self.squares = [Square(i) for i in range(9)]
        self.cells = []
        self.cells_creation()
        self.none_cells = []
        self.none_cells_creation()

    def cells_creation(self):
        for row in self.rows:
            for col in self.cols:
                sq = self.squares[(3 * (row.num // 3)) + (col.num // 3)]
                cell = Cell(row, col, sq)
                self.cells.append(cell)
                sq.add_cell(cell)
                row.add_cell(cell)
                col.add_cell(cell)

    def __str__(self):
        row_strings = []
        for row in self.rows:
            row_values = [cell.value for cell in row.cells]
            row_strings.append(", ".join(str(value) for value in row_values))

        return f"{25 * '*'}\n{chr(10).join(row_strings)}"

    def diagonal_draw(self):
        for i in [0, 4, 8]:
            for cell in self.squares[i].cells:
                cell.draw_val()
        self.none_cells_creation()

    def random_deletion(self, n):
        rand = random.sample(range(81), n)
        for i in rand:
            self.cells[i].del_value()
        self.none_cells_creation()

    def none_cells_creation(self):
        self.none_cells = [cell for cell in self.cells if cell.value is None]

    def solver(self, n, loop):
        if n == len(self.none_cells):
            # if loop[0] == 0:
            #     loop[0] += 1
            #     return False
            #
            # else:
            #     print('jest nas więcej')
            return True

        elif len(self.none_cells[n].choice()) == 0:
            if self.none_cells[n].value is not None:
                self.none_cells[n].del_value()
            return False

        else:
            self.none_cells[n].add_value(self.none_cells[n].choice()[0])
            while self.solver(n + 1, loop) is False:
                if self.none_cells[n].add_value(self.none_cells[n].del_value()) is False:
                    return False


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


if __name__ == "__main__":
    board = Board()
    board.diagonal_draw()

    print(board)

    board.solver(0, [0])
    print(board)
    board.random_deletion(50)
    print(board)
    board.solver(0, [0])
    print(board)
