import time
import random
import copy
import platform

import tkinter as tk
from tkinter import messagebox
from os import getpid
from os import system
from conf import Configuration
from shapes import *
import settings as set
from tools import ptype

# ===============================================
# WINDOW OPTIONS
# ===============================================
BG_COLOR = 'gray'

# Board
BOARD_BG_COLOR = 'lightgray'
BOARD_FG_COLOR = 'white'
BOARD_GRID_COLOR = '#333'
MENU_FONTS = 'TkDefaultFont 12'

# Status
FONT_SIZE = 12
FONT_COLOR = 'white'

# Tetrominos
TETROMINO_FG_COLOR = 'black'
TETROMINO_BORDER_WIDTH = 2  # in pixels
I_COLOR = 'cyan'
O_COLOR = 'yellow'
T_COLOR = 'magenta'
J_COLOR = 'blue'
L_COLOR = 'orange'
S_COLOR = 'green'
Z_COLOR = 'red'
COMPLETE_ROW_BG_COLOR = 'white'  # None for inherit
COMPLETE_ROW_FG_COLOR = None
# ===============================================

NORMAL_GAME = 1
PAUSED_GAME = 2
CHANGE_SPEED_GAME = 3
isPaused = False
SIZE_STATE = 2

# Levels
LEVEL_0_DELAY = 1000  # inital delay between steps
ROWS_BY_LEVEL = 10
POINTS = [40, 100, 300, 1200]  # 1 , 2, 3, Tetris


class Application(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title('Tetris')
        self.option_add('*Font', MENU_FONTS)
        self.configurationWin = None
        self.startGame()

    def startGame(self):
        self.grid()
        self.create_widgets()
        self.draw_grid()
        self.create_events()
        self.tetrominos = self.get_tetrominos()
        self.board = None
        self.board = self.get_init_board()
        self.next = copy.deepcopy(random.choice(self.tetrominos))
        self.tetromino = None
        self.status = self.get_init_status()
        self.delay = LEVEL_0_DELAY
        self.job_id = None
        self.running = True
        self.step()

    def create_widgets(self):
        top = self.winfo_toplevel()
        top.config(bg=BG_COLOR)

        width = set.width * set.boxSize
        height = set.height * set.boxSize

        # main menu
        self.menuBar = tk.Menu()
        self.config(menu=self.menuBar)

        # file submenu
        self.fileMenu = tk.Menu(self.menuBar, tearoff=False)
        self.menuBar.add_cascade(label='File', menu=self.fileMenu)
        self.fileMenu.add_command(label='Exit', command=self.onExit)

        # configuration submenu
        self.confMenu = tk.Menu(self.menuBar, tearoff=False)
        self.menuBar.add_cascade(label='Configuration', menu=self.confMenu)
        self.confMenu.add_command(label='Game', command=self.generalConfig)

        # help submenu
        self.helpMenu = tk.Menu(self.menuBar, tearoff=False)
        self.menuBar.add_cascade(label='Help', menu=self.helpMenu)
        self.helpMenu.add_command(label='Instructions',
                                  command=self.instructions)

        self.canvas = tk.Canvas(self, width=width, height=height,
                                bg=BOARD_BG_COLOR,
                                highlightbackground=BOARD_FG_COLOR)
        self.canvas.grid(row=0, column=0, padx=20, pady=20)

        lb_status = self.lb_status = tk.Label(
            self, bg=BG_COLOR, fg=FONT_COLOR, font=('monospace', FONT_SIZE))
        lb_status.grid(row=0, column=1, padx=(0, 20), pady=20, sticky=tk.N)

    def pause(self, event):
        tk.messagebox.showinfo('Paused', 'Press ok to continue')

    def generalConfig(self):
        self.configurationWin = Configuration(self)

    def instructions(self):
        message = "------ Game Modes -------\n\n" \
                  "NORMAL: Exactly like normal Tetris\n\n" \
                  "PAUSED: The piece falls only when " \
                  "the player presses the Down key\n\n" \
                  "SPEED: The speed of the falling " \
                  "piece is determined by the player\n\n\n" \
                  "------- Key Bindings -------\n" \
                  "Up\t\t=> up arrow\n" \
                  "Down\t\t=> down arrow\n" \
                  "Left\t\t=> left arrow\n" \
                  "Right\t\t=> right arrow\n" \
                  "Increase speed\t=> F1\n" \
                  "Decrease speed\t=> F2\n" \
                  "Pause\t\t=> p\n"
        tk.messagebox.showinfo('Game Modes', message)

    # Exit function
    def onExit(self):
        id = getpid()
        os = platform.system()
        if os == 'Linux':
            command = 'kill ' + str(id)
            system(command)
        else:
            command = 'taskkill -f /pid ' + str(id)
            system(command)

    def draw_grid(self):
        for i in range(set.width - 1):
            x = (set.boxSize * i) + set.boxSize
            y0 = 0
            y1 = set.boxSize * set.height
            self.canvas.create_line(x, y0, x, y1,
                                    fill=BOARD_GRID_COLOR)
        for i in range(set.height - 1):
            x0 = 0
            x1 = set.boxSize * set.width
            y = (set.boxSize * i) + set.boxSize
            self.canvas.create_line(x0, y, x1, y, fill=BOARD_GRID_COLOR)

    def create_events(self):
        self.bind('<KeyPress-p>', self.pause)
        self.bind('<KeyPress-Up>', self.rotate)
        self.bind('<KeyPress-Down>', self.move)
        self.bind('<KeyPress-Left>', self.move)
        self.bind('<KeyPress-Right>', self.move)
        self.bind('<KeyPress-1>', self.shorten)
        self.bind('<KeyPress-2>', self.enlarge)
        if set.gameTypeVar is CHANGE_SPEED_GAME:
            self.bind('<KeyPress-F1>', self.increaseSpeed)
            self.bind('<KeyPress-F2>', self.decreaseSpeed)
        else:
            self.unbind('<KeyPress-F1>')
            self.unbind('<KeyPress-F2>')

    def shorten(self, event):
        global SIZE_STATE
        if SIZE_STATE > 0:
            SIZE_STATE -= 1
        self.draw_tetromino()

    def enlarge(self, event):
        global SIZE_STATE
        if SIZE_STATE < 2:
            SIZE_STATE += 1
        self.draw_tetromino()

    def increaseSpeed(self, event):
        if self.delay < 50:
            self.delay = 50
        else:
            self.delay -= 20

    def decreaseSpeed(self, event):
        if self.delay > 5000:
            self.delay = 5000
        else:
            self.delay += 20

    def get_tetrominos(self):
        tetrominos = []
        s = [set.shapeI, set.shapeO, set.shapeT, set.shapeL,
             set.shapeJ, set.shapeS, set.shapeZ]
        shapes = 'IOTLJSZ'
        usedShapes = []
        for i in range(len(shapes)):
            if s[i] == True:
                usedShapes.append(shapes[i])
        for name in usedShapes:
            tetromino = globals()[name]
            data = {
                'name': name,
                'pieces': tetromino,
                'actual': 0,
                'color': globals()[name + '_COLOR'],
                'coords': self.get_init_coords(tetromino),
                'rows': (len(tetromino[0][0]),
                         len(tetromino[1][0]),
                         len(tetromino[2][0]),),
                'cols': (len(tetromino[0][0][0]),
                         len(tetromino[1][0][0]),
                         len(tetromino[2][0][0])),
                'total_pieces': (len(tetromino[0]),
                                len(tetromino[1]),
                                len(tetromino[2])),
                'can_rotate': True, # if name is not 'O' else False,
                'ids': [],
            }
            tetrominos.append(data)
        return tetrominos

    def get_init_coords(self, tetromino):
            return int(set.width / 2.0 - len(tetromino[2][0]) / 2.0), 1

    def get_init_board(self):
        if getattr(self, 'board', None) is None:
            self.board = [[0] * set.width for _ in range(set.height)]
        else:
            for y in range(set.height):
                for x in range(set.width):
                    if self.board[y][x]:
                        self.canvas.delete(self.board[y][x])
                        self.board[y][x] = 0
        return self.board

    def get_init_status(self):
        return {'score': 0, 'rows': 0, 'level': 0,
                'O': 0, 'I': 0, 'S': 0, 'T': 0, 'Z': 0, 'L': 0, 'J': 0,
                'total': 0, 'next': ''}

    def step(self):
        for child in self.winfo_children():
            if child.__dict__['widgetName'] == 'frame':
                self.job_id = self.canvas.after(100, self.step)
                return

        if self.configurationWin is not None and \
                self.configurationWin.winfo_exists():
            if not set.replay:
                self.job_id = self.canvas.after(100, self.step)
            else:
                set.replay = False
                pass
        else:
            if self.tetromino and self.can_be_moved('Down'):
                if set.gameTypeVar is not PAUSED_GAME:
                    self.move_tetromino((0, 1))
                    self.job_id = self.canvas.after(self.delay, self.step)
            else:
                self.check_status()
                if self.is_gameover(self.next):
                    title = 'Game Over'
                    message = 'Your score: %d' % self.status['score']
                    messagebox.showinfo(title, message)
                    self.startGame()
                else:
                    self.tetromino = self.next
                    self.next = copy.deepcopy(random.choice(self.tetrominos))
                    self.status[self.tetromino['name']] += 1
                    self.status['total'] += 1
                    self.status['next'] = self.next['name']
                    self.update_label_status()
                    self.draw_tetromino()

                    self.job_id = self.canvas.after(self.delay, self.step)

    def check_status(self):
        rows = []
        for row in range(set.height):
            if 0 not in self.board[row]:
                rows.append(row)
        if rows:
            self.del_rows(rows)
            self.set_score(rows)

    def del_rows(self, rows):
        for row in rows:
            for id in self.board[row]:
                self.canvas.tag_raise(id)  # bring to front
                self.canvas.itemconfig(id, fill=COMPLETE_ROW_BG_COLOR,
                                       outline=COMPLETE_ROW_FG_COLOR)
        self.canvas.update()
        time.sleep(0.5)
        for row in rows:
            for id in self.board[row]:
                self.canvas.delete(id)
            del self.board[row]
            self.board.insert(0, [0] * set.width)
            for row0 in range(row + 1):
                for id0 in self.board[row0]:
                    self.canvas.move(id0, 0, set.boxSize)
        self.canvas.update()

    def set_score(self, rows):
        points = POINTS[len(rows) - 1]
        self.status['rows'] += len(rows)
        if self.status['rows'] % ROWS_BY_LEVEL == 0:
            self.status['level'] += 1
            if set.gameTypeVar is not CHANGE_SPEED_GAME:
                if self.delay > 100:
                    self.delay -= 100
        self.status['score'] += points
        self.update_label_status()

    def update_label_status(self):
        if set.gameTypeVar == NORMAL_GAME:
            type = 'Normal'
        elif set.gameTypeVar == PAUSED_GAME:
            type = 'Paused'
        else:
            type = 'Speed'
        lines = [
            'Score: %7s' % self.status['score'],
            '',
            'Mode : %7s' % type,
            'Level: %7s' % self.status['level'],
            'Rows : %7s' % self.status['rows'],
            '',
            'Next : %7s' % self.status['next'],
        ]
        self.lb_status.config(text='\n'.join(lines))

    def is_gameover(self, next):
        x, y = next['coords']
        for y0 in range(next['rows'][SIZE_STATE]):
            for x0 in range(next['cols'][SIZE_STATE]):
                x1 = x0 + x
                y1 = y0 + y
                if self.board[y1][x1]:
                    self.running = False
                    self.canvas.after_cancel(self.job_id)
                    return True
        return False

    def draw_tetromino(self):
        self.del_tetromino()
        piece = self.tetromino['pieces'][SIZE_STATE][self.tetromino['actual']]
        x0, y0 = self.tetromino['coords']
        for y in range(self.tetromino['rows'][SIZE_STATE]):
            for x in range(self.tetromino['cols'][SIZE_STATE]):
                if piece[y][x] == 1:
                    x1 = (x0 + x) * set.boxSize
                    y1 = (y0 + y) * set.boxSize
                    x2 = x1 + set.boxSize
                    y2 = y1 + set.boxSize
                    id = self.canvas.create_rectangle(
                        x1, y1, x2, y2, width=TETROMINO_BORDER_WIDTH,
                        outline=TETROMINO_FG_COLOR,
                        fill=self.tetromino['color'])
                    self.tetromino['ids'].append(id)
                    self.board[y0 + y][x0 + x] = id
        self.canvas.update()

    def del_tetromino(self):
        if self.tetromino['ids']:
            for y in range(set.height):
                for x in range(set.width):
                    if self.board[y][x] in self.tetromino['ids']:
                        self.board[y][x] = 0
            for id in self.tetromino['ids']:
                self.canvas.delete(id)
            self.tetromino['ids'] = []

    def rotate(self, event):
        if self.tetromino['actual'] < self.tetromino['total_pieces'][SIZE_STATE] \
                - 1:
            next = self.tetromino['actual'] + 1
        else:
            next = 0
        if self.can_be_rotated(next):
            self.tetromino['actual'] = next
            self.draw_tetromino()

    def can_be_rotated(self, next):
        piece = self.tetromino['pieces'][SIZE_STATE][next]
        board = self.board
        x, y = self.tetromino['coords']
        for y0 in range(self.tetromino['rows'][SIZE_STATE]):
            for x0 in range(self.tetromino['cols'][SIZE_STATE]):
                if piece[y0][x0] == 1:
                    if x == -1 and x0 == 1:
                        return False
                    if x + x0 >= set.width:
                        return False
                    if y + y0 >= set.height:
                        return False
                    x1 = x + x0
                    y1 = y + y0
                    if board[y1][x1] and \
                            (board[y1][x1] not in self.tetromino['ids']):
                        return False
        return True

    def move(self, event):
        if self.running and self.can_be_moved(event.keysym):
            x, y = self.tetromino['coords']
            if event.keysym == 'Left':
                self.move_tetromino((-1, 0))
            if event.keysym == 'Right':
                self.move_tetromino((1, 0))
            if event.keysym == 'Down':
                self.canvas.after_cancel(self.job_id)
                self.move_tetromino((0, 1))
                self.job_id = self.canvas.after(self.delay, self.step)

    def move_tetromino(self, offset):
        x, y = offset
        ranges = {
            (-1, 0): ((0, set.width, 1), (0, set.height, 1)),
            (1, 0): ((set.width - 1, -1, -1), (0, set.height, 1)),
            (0, 1): ((0, set.width, 1), (set.height - 1, -1, -1))
        }

        x_start_stop_step, y_start_stop_step = ranges[offset]
        for y0 in range(*y_start_stop_step):
            for x0 in range(*x_start_stop_step):
                id = self.board[y0][x0]
                if id in self.tetromino['ids']:
                    self.board[y0 + y][x0 + x] = self.board[y0][x0]
                    self.board[y0][x0] = 0
                    self.canvas.move(id, x * set.boxSize, y * set.boxSize)

        x1, y1 = self.tetromino['coords']
        self.tetromino['coords'] = (x1 + x, y1 + y)
        self.canvas.update()

    def can_be_moved(self, direction):
        piece = self.tetromino['pieces'][SIZE_STATE][self.tetromino['actual']]
        board = self.board
        x, y = self.tetromino['coords']
        for y0 in range(self.tetromino['rows'][SIZE_STATE]):
            for x0 in range(self.tetromino['cols'][SIZE_STATE]):
                if piece[y0][x0] == 1:
                    if direction == 'Left':
                        x1 = x + x0 - 1
                        y1 = y + y0
                        if x1 < 0 or (board[y1][x1] and
                                              board[y1][x1] not in
                                              self.tetromino['ids']):
                            return False
                    if direction == 'Right':
                        x1 = x + x0 + 1
                        y1 = y + y0
                        if x1 >= set.width or (board[y1][x1] and
                                                       board[y1][x1] not in
                                                       self.tetromino['ids']):
                            return False
                    if direction == 'Down':
                        x1 = x + x0
                        y1 = y + y0 + 1
                        if y1 >= set.height or (board[y1][x1] and
                                                        board[y1][x1] not in
                                                        self.tetromino['ids']):
                            return False
        return True


if __name__ == '__main__':
    app = Application()
    app.mainloop()
