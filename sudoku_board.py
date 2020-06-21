from random import *


class SudokuBoard:
    def __init__(self, dif_set, board=[[0] * 9 for _ in range(9)]):
        self.board = board
        self.dif_set = dif_set
        seed(None, 2)

    def empty(self):
        for i in range(9):
            for s in range(9):
                if self.board[i][s] == 0:
                    return i, s
        return False

    def validate(self, pos, num):
        for i in range(len(self.board)):
            if self.board[pos[0]][i] == num and i != pos[1]:
                return False

        for i in range(len(self.board)):
            if self.board[i][pos[1]] == num and i != pos[0]:
                return False

        square_x = pos[0] // 3
        square_y = pos[1] // 3

        for i in range(square_x * 3, square_x * 3 + 3):
            for s in range(square_y * 3, square_y * 3 + 3):
                if self.board[i][s] == num and (i, s) != pos:
                    return False
        return True

    def fill_solve(self):
        if not self.empty():
            return True
        else:
            row, col = self.empty()

        for num in sample(range(1, 10), 9):
            if self.validate((row, col), num):
                self.board[row][col] = num
                if self.fill_solve():
                    return True
                self.board[row][col] = 0

        return False

    def create_board(self):
        for i in range(9):
            if i < 3:
                n, z = i, 0
            elif i < 6:
                n, z = i - 3, 1
            elif i >= 6:
                n, z = i - 6, 2
            square_x = n
            square_y = z
            list = []
            for s in range(square_x * 3, square_x * 3 + 3):
                for c in range(square_y * 3, square_y * 3 + 3):
                    list.append((s, c))

            for x in sample(list, self.dif_set):
                self.board[x[0]][x[1]] = 0

    def reset(self):
        self.board = [[0] * 9 for _ in range(9)]

    def show_board(self):
        for i in range(len(self.board)):
            if i % 3 == 0 and i != 0:
                print('- - - - - - - - - - - - - - - -', end='\n' * 2)
            for s in range(len(self.board)):
                if s % 3 == 0 and s != 0:
                    print('|  ', end='')
                print(self.board[i][s], end='  ')
                if s == 8:
                    print('\n')