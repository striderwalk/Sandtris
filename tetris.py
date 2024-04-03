import numpy as np
import pygame
import random

from consts import GRAIN_SIZE, GRID_COLS, GRID_ROWS, HEIGHT, PIECE_SIZE, WIDTH
from grid import Grid

colors = ["white", "red", "green", "blue", "yellow"]


class Piece:
    x = 0
    y = 0

    pieces = [
        [[1, 5, 9, 13], [4, 5, 6, 7]],
        [[4, 5, 9, 10], [2, 6, 5, 9]],
        [[6, 7, 9, 10], [1, 5, 6, 10]],
        [[1, 2, 5, 9], [0, 4, 5, 6], [1, 5, 9, 8], [4, 5, 6, 10]],
        [[1, 2, 6, 10], [5, 6, 7, 9], [2, 6, 10, 11], [3, 5, 6, 7]],
        [[1, 4, 5, 6], [1, 4, 5, 9], [4, 5, 6, 9], [1, 5, 6, 9]],
        [[1, 2, 5, 6]],
    ]

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.type = random.randint(0, len(self.pieces) - 1)
        self.color = random.randint(1, len(colors) - 1)
        self.rotation = 0

    def image(self):
        return self.pieces[self.type][self.rotation]

    def rotate(self):
        self.rotation = (self.rotation + 1) % len(self.pieces[self.type])


class Sandtris:
    def __init__(self):
        self.grid = Grid()

        self.piece = None
        self.field = np.zeros((GRID_COLS, GRID_ROWS), dtype=np.int8)
        self.score = 0

    def new_piece(self):
        self.piece = Piece(3, 0)

    def intersects(self):

        intersection = False
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.piece.image():
                    if (
                        i + self.piece.y > GRID_COLS - 1
                        or j + self.piece.x > GRID_ROWS - 1
                        or j + self.piece.x < 0
                        or self.grid.piece_touching(i + self.piece.y, j + self.piece.x)
                    ):
                        intersection = True
        return intersection

    def press_space(self):
        while not self.intersects():
            self.piece.y += 1
        self.piece.y -= 1
        self.freeze()

    def go_down(self):
        self.piece.y += 0.2
        if self.intersects():
            self.piece.y -= 0.2
            self.freeze()

    def freeze(self):
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.piece.image():
                    self.grid.place(
                        i + self.piece.y, j + self.piece.x, self.piece.color
                    )
        self.piece = None

    def go_side(self, dx):
        if self.piece == None:
            self.new_piece()
        old_x = self.piece.x
        self.piece.x += dx
        if self.intersects():
            self.piece.x = old_x

    def rotate(self):
        old_rotation = self.piece.rotation
        self.piece.rotate()
        count = 0
        while self.intersects():
            count += 1
            if self.piece.x < 5:
                self.piece.x += 1
            else:
                self.piece.x -= 1

            if count > 5:
                self.piece.rotation = old_rotation

                break

    def draw(self, win):
        if self.piece is not None:
            for i in range(4):
                for j in range(4):
                    p = i * 4 + j
                    if p in self.piece.image():
                        pygame.draw.rect(
                            win,
                            colors[self.piece.color],
                            [
                                PIECE_SIZE * (j + self.piece.x) + 1,
                                PIECE_SIZE * (i + self.piece.y) + 1,
                                PIECE_SIZE - 2,
                                PIECE_SIZE - 2,
                            ],
                        )

    def update(self, win):
        if self.piece == None:
            self.new_piece()

        self.grid.update(win)
        self.draw(win)
