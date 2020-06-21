from sudoku_board import SudokuBoard
import sys
import pygame
import random


class Visual:
    def __init__(self, display, img=None):
        self.display = display
        self.img = img
        self.screen = pygame.display.set_mode(self.display)
        self.time = pygame.time.Clock()
        self.toggle = True
        pygame.init()
        pygame.display.init()
        pygame.font.init()
        pygame.display.set_caption('Sudoku')
        #https://www.flaticon.com/authors/surang

    def background(self):
        if pygame.image.get_extended() and self.img:
            try:
                icon = pygame.image.load('sudoku.png')
                pygame.display.set_icon(icon)
                self.screen.blit(pygame.image.load(self.img), (0, 0))
                pygame.display.update()
            except pygame.error:
                self.screen.fill((30, 30, 30))
                pygame.display.update()
        else:
            self.screen.fill((30, 30, 30))
            pygame.display.update()


class Board:
    def __init__(self, display, board=SudokuBoard(9)):
        self.screen = display.screen
        self.board = board
        self.squares_pos = []
        self.wrong = []
        self.interactive = self.interactive_shell()
        self.time = pygame.time.Clock()
        self.font = pygame.font.Font('freesansbold.ttf', 30)
        self.active = False
        self.input = ''
        self.active_cell = None

    def draw_board(self):
        for i in range(len(self.board.board)):
            for s in range(len(self.board.board[0])):
                self.squares_pos.append((i, s))

        pygame.draw.rect(self.screen, (160, 160, 160), (400, 300, -180, -180))
        pygame.draw.rect(self.screen, (160, 160, 160), (400, 300, 180, -180))
        pygame.draw.rect(self.screen, (160, 160, 160), (400, 300, -180, 180))
        pygame.draw.rect(self.screen, (160, 160, 160), (400, 300, 180, 180))
        pygame.draw.line(self.screen, (0, 0, 0), (220, 240), (580, 240), 4)
        pygame.draw.line(self.screen, (0, 0, 0), (220, 360), (580, 360), 4)
        pygame.draw.line(self.screen, (0, 0, 0), (340, 120), (340, 480), 4)
        pygame.draw.line(self.screen, (0, 0, 0), (460, 120), (460, 480), 4)
        pygame.draw.line(self.screen, (0, 0, 0), (220, 160), (580, 160), 1)
        pygame.draw.line(self.screen, (0, 0, 0), (220, 200), (580, 200), 1)
        pygame.draw.line(self.screen, (0, 0, 0), (220, 280), (580, 280), 1)
        pygame.draw.line(self.screen, (0, 0, 0), (220, 320), (580, 320), 1)
        pygame.draw.line(self.screen, (0, 0, 0), (220, 400), (580, 400), 1)
        pygame.draw.line(self.screen, (0, 0, 0), (220, 440), (580, 440), 1)
        pygame.draw.line(self.screen, (0, 0, 0), (260, 120), (260, 480), 1)
        pygame.draw.line(self.screen, (0, 0, 0), (300, 120), (300, 480), 1)
        pygame.draw.line(self.screen, (0, 0, 0), (380, 120), (380, 480), 1)
        pygame.draw.line(self.screen, (0, 0, 0), (420, 120), (420, 480), 1)
        pygame.draw.line(self.screen, (0, 0, 0), (500, 120), (500, 480), 1)
        pygame.draw.line(self.screen, (0, 0, 0), (540, 120), (540, 480), 1)

        x, y = 234, 125

        for i in self.squares_pos:
            if i in self.wrong:
                color = (190, 0, 0)
            else:
                color = (0, 0, 0)

            text = self.font.render(str(self.board.board[i[0]][i[1]]) if str(self.board.board[i[0]][i[1]]) != '0' else None, True, color)
            self.screen.blit(text, (x, y))
            x += 40
            if (x-234) == 360:
                x = 234
                y += 40
        self.squares_pos = []
        pygame.display.flip()
        self.time.tick(30)

    def interactive_shell(self):
        for i in range(len(self.board.board)):
            for s in range(len(self.board.board[0])):
                self.squares_pos.append((i, s))

        input_box = []
        x, y = 234, 125

        for i in self.squares_pos:
            if self.board.board[i[0]][i[1]] == 0:
                s = pygame.Rect(x-15, y-5, 40, 40)
                input_box.append((s, i, (x, y)))
            x += 40
            if (x-234) == 360:
                x = 234
                y += 40

        self.squares_pos = []
        return input_box

    def user_input(self):

        if self.active_cell and self.input != '0':
            text = self.font.render(self.input, True, (0, 0, 0))
            self.screen.blit(text, self.active_cell[1])
            pygame.display.flip()

        if event.type == pygame.MOUSEBUTTONDOWN:
            for i in self.interactive:
                if i[0].collidepoint(event.pos):
                    self.active = not self.active
                    self.active_cell = (i[1], i[2])
                    break
                else:
                    self.active = False

        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_RETURN:
                try:
                    if int(self.input) in range(10):
                        self.board.board[self.active_cell[0][0]][self.active_cell[0][1]] = int(self.input)
                        if self.board.validate(self.active_cell[0], int(self.input)) and self.active_cell[0] in self.wrong:
                            self.wrong.remove(self.active_cell[0])
                        if not self.board.validate(self.active_cell[0], int(self.input)):
                            self.wrong.append(self.active_cell[0])
                    self.input = ''
                    pygame.display.flip()
                except ValueError:
                    self.input = ''
            elif event.key == pygame.K_BACKSPACE:
                if self.board.board[self.active_cell[0][0]][self.active_cell[0][1]] != 0 and not self.input:
                    self.board.board[self.active_cell[0][0]][self.active_cell[0][1]] = 0
                else:
                    self.input = self.input[:-1]
            else:
                self.input += event.unicode


class Menu:
    def __init__(self, display):
        self.display = display
        self.screen = display.screen
        self.background = display.background
        self.time = pygame.time.Clock()
        self.active = True
        self.dif_menu = False
        self.submit_mode = False
        self.font = pygame.font.Font('freesansbold.ttf', 30)
        self.board = Board(display)
        self.sudoku = self.board.board
        self.difficulty = (3, "Easy")
        self.interactive = None

    def create_menu_1(self):
        if not self.dif_menu:
            pressed_button = None
            buttons = []
            texts = ("Create New Board", "Solve Given Board", "Difficulty Settings")
            if self.interactive:
                texts = ("Create New Board", "Solve Given Board", "Difficulty Settings", "Resume")
            x, y = 0, 50

            for i in range(len(texts)):
                buttons.append([pygame.Rect(x, y, 400, 50), i])
                pygame.draw.rect(self.screen, (160, 160, 160), buttons[i][0])
                pygame.draw.rect(self.screen, (0, 0, 0), buttons[i][0], 2)
                text = self.font.render(texts[i], True, (0, 0, 0))
                self.screen.blit(text, (x+30, y+10))
                y += 50
            pygame.display.flip()

            if event.type == pygame.MOUSEBUTTONDOWN:
                for i in buttons:
                    if i[0].collidepoint(event.pos):
                        pygame.draw.rect(self.screen, (0, 0, 255), i[0], 2)
                        pygame.display.flip()
                        pressed_button = texts[i[1]]
                        break

            if pressed_button == "Create New Board":
                self.board = Board(self.display, SudokuBoard(self.difficulty[0]))
                self.sudoku = self.board.board
                self.sudoku.reset()
                self.sudoku.fill_solve()
                self.sudoku.create_board()
                self.board.interactive = self.board.interactive_shell()
                self.interactive = self.board.interactive
                self.submit_mode = False
                self.active = False

            if pressed_button == "Solve Given Board":
                self.board = Board(self.display)
                self.sudoku = self.board.board
                self.sudoku.reset()
                self.board.interactive = self.board.interactive_shell()
                self.interactive = self.board.interactive
                self.submit_mode = True
                self.active = False

            if pressed_button == "Difficulty Settings":
                self.dif_menu = True
                self.background()

            if pressed_button == "Resume":
                self.active = False

        else:
            pressed_button = None
            buttons = []
            dif_texts = ("Easy", "Normal", "Hard", "Really Hard", "Back")
            x, y = 500, 100

            for i in range(len(dif_texts)):
                buttons.append([pygame.Rect(x, y, 300, 50), i])
                pygame.draw.rect(self.screen, (160, 160, 160), buttons[i][0])
                if self.difficulty[1] == dif_texts[i]:
                    pygame.draw.rect(self.screen, (0, 0, 255), buttons[i][0], 2)
                else:
                    pygame.draw.rect(self.screen, (0, 0, 0), buttons[i][0], 2)
                text = self.font.render(dif_texts[i], True, (0, 0, 0))
                self.screen.blit(text, (x + 30, y + 10))
                y += 50
            pygame.display.flip()

            if event.type == pygame.MOUSEBUTTONDOWN:
                for i in buttons:
                    if i[0].collidepoint(event.pos):
                        pressed_button = dif_texts[i[1]]
                        break

            if pressed_button == "Easy":
                self.difficulty = 3, "Easy"

            if pressed_button == "Normal":
                self.difficulty = 4, "Normal"

            if pressed_button == "Hard":
                self.difficulty = 5, "Hard"

            if pressed_button == "Really Hard":
                self.difficulty = 6, "Really Hard"

            if pressed_button == "Back":
                self.dif_menu = False
                self.background()

    def create_menu_2(self):
        if self.submit_mode:
            submit_button = pygame.Rect(250, 500, 150, 50)
            pygame.draw.rect(self.screen, (160, 160, 160), submit_button)
            pygame.draw.rect(self.screen, (0, 0, 0), submit_button, 2)
            text = self.font.render("Submit", True, (0, 0, 0))
            self.screen.blit(text, (275, 510))

            if event.type == pygame.MOUSEBUTTONDOWN:
                if submit_button.collidepoint(event.pos):
                    pygame.draw.rect(self.screen, (0, 0, 255), submit_button, 2)
                    self.submit_mode = False
                    self.board.interactive = self.board.interactive_shell()
                    self.interactive = self.board.interactive
                pygame.display.flip()

        else:
            solve_button = pygame.Rect(250, 500, 150, 50)
            pygame.draw.rect(self.screen, (160, 160, 160), solve_button)
            pygame.draw.rect(self.screen, (0, 0, 0), solve_button, 2)
            text = self.font.render("Solve", True, (0, 0, 0))
            self.screen.blit(text, (285, 510))

            if event.type == pygame.MOUSEBUTTONDOWN:
                if solve_button.collidepoint(event.pos):
                    pygame.draw.rect(self.screen, (0, 0, 255), solve_button, 2)
                    if self.sudoku.fill_solve():
                        pass
                    else:
                        interactive = self.interactive
                        random.shuffle(interactive)
                        for i in interactive:
                            if self.sudoku.board[i[1][0]][i[1][1]] != 0:
                                self.sudoku.board[i[1][0]][i[1][1]] = 0
                                pygame.display.flip()
                                print(1)
                                if self.sudoku.fill_solve():
                                    break
                pygame.display.flip()

        menu_button = pygame.Rect(650, 50, 100, 50)
        pygame.draw.rect(self.screen, (160, 160, 160), menu_button)
        pygame.draw.rect(self.screen, (0, 0, 0), menu_button, 2)
        text = self.font.render("Menu", True, (0, 0, 0))
        self.screen.blit(text, (660, 60))
        pygame.display.flip()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if menu_button.collidepoint(event.pos):
                self.active = True
                pygame.draw.rect(self.screen, (0, 0, 255), menu_button, 2)
            pygame.display.flip()


dis = Visual((800, 600), 'sudoku_background.jpg')
menu = Menu(dis)
while True:
    for event in pygame.event.get():
        if menu.active:
            menu.create_menu_1()
            if dis.toggle:
                dis.background()
                dis.toggle = False
        else:
            menu.create_menu_2()
            menu.board.draw_board()
            menu.board.user_input()
            if not dis.toggle:
                dis.background()
                dis.toggle = True
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)
