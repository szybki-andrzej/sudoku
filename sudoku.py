import numpy as np
import random
import math


class Board:
    def __init__(self, size):
        self.size = size
        self.sq_size = int(math.sqrt(self.size))
        self.rows = [Row(i, self.size) for i in range(self.size)]
        self.cols = [Col(i, self.size) for i in range(self.size)]
        self.squares = [Square(i, self.size) for i in range(self.size)]
        self.cells = []
        self.cells_creation()
        self.none_cells = []
        self.none_cells_creation()
        self.cells_values_list = [None for _ in range(len(self.cells))]

    def cells_values(self):
        self.cells_values_list = [cell.value for cell in self.cells]

    def cells_creation(self):
        for row in self.rows:
            for col in self.cols:
                sq = self.squares[(self.sq_size * (row.num // self.sq_size)) + (col.num // self.sq_size)]
                cell = Cell(row, col, sq)
                self.cells.append(cell)
                sq.add_cell(cell)
                row.add_cell(cell)
                col.add_cell(cell)

    def __str__(self):
        row_strings = []
        for row in self.rows:
            row_values = []
            for cell in row.cells:
                if cell.value is None:
                    row_values.append('X')
                else:
                    row_values.append(cell.value)
            row_strings.append(", ".join(str(value) for value in row_values))

        return f"{chr(10).join(row_strings)}"

    def save_to_file(self):
        row_strings = []
        for row in self.rows:
            row_values = []
            for cell in row.cells:
                if cell.value is None:
                    row_values.append('X')
                else:
                    row_values.append(cell.value)
            row_strings.append(", ".join(str(value) for value in row_values))

        with open("result_board.txt", 'w') as f:
            f.write(f"{chr(10).join(row_strings)}")

    def diagonal_draw(self):
        """Function that draw values to the cells in diagonal squares of board. """
        for i in range(0, self.size, self.sq_size + 1):
            for cell in self.squares[i].cells:
                cell.draw_val()
        self.none_cells_creation()
        self.cells_values()

    def random_deletion(self, n):
        """Function that randomly change n values to in the board to None."""
        rand = random.sample(range(self.size**2), n)
        for i in rand:
            self.cells[i].del_value()
        self.none_cells_creation()
        self.cells_values()

    def none_cells_creation(self):
        """Function that identifies cells with None values."""
        self.none_cells = [cell for cell in self.cells if cell.value is None]

    def solver(self, n, loop):
        """Function that fills none_cells with values using backtracking algorithm using recurrence and leave values not
         changed if there is more than one solution."""
        if n == len(self.none_cells):
            if loop[0] == 0:
                loop[0] += 1
                return False
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
    def __init__(self, num, size, num_options=None):
        self.size = size
        if num_options is None:
            num_options = list(range(self.size))
        self.num = num
        self.num_options = num_options
        self.cells = []

    def add_cell(self, cell):
        self.cells.append(cell)


class Col:
    def __init__(self, num, size, num_options=None):
        self.size = size
        if num_options is None:
            num_options = list(range(self.size))
        self.num = num
        self.num_options = num_options
        self.cells = []

    def add_cell(self, cell):
        self.cells.append(cell)


class Square:
    def __init__(self, num, size, num_options=None):
        self.size = size
        if num_options is None:
            num_options = list(range(self.size))
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
        """Function that returns list of possible choices of values for the cell."""
        return np.intersect1d(np.intersect1d(np.array(self.row.num_options), np.array(self.col.num_options)),
                              np.array(self.square.num_options))

    def draw_val(self):
        """Function that draw values from the possible choices for the cell."""
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
        """Function that changes value for the cell to None and return next element from choices of the cell if
        exists."""
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
    board = Board(9)
    board.diagonal_draw()
    board.solver(0, [0])
    for i in range(10000):
        board.random_deletion(10)
        board.solver(0, [0])
        board.cells_values()
        if None in board.cells_values_list:
            break
    print(board)
    board.save_to_file()
