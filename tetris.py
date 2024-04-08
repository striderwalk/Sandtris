import pygame
import random

from consts import (
    COLS,
    GAME_SCREEN_WIDTH,
    GRAIN_SIZE,
    PIECE_SIZE,
    ROWS,
)
from grid import Grid

colours = ["white", "red", "green", "blue", "yellow"]


class Piece:
    x = 0
    y = 0

    pieces = [
        [[4, 5, 6, 7], [2, 6, 10, 14], [8, 9, 10, 11], [1, 5, 9, 13]],  # I
        [[0, 4, 5, 6], [1, 2, 5, 9], [4, 5, 6, 10], [1, 5, 9, 8]],  # J
        [[4, 5, 6, 2], [1, 5, 9, 10], [4, 5, 6, 8], [0, 1, 5, 9]],  # L
        [[1, 2, 4, 5], [1, 5, 6, 10], [5, 6, 8, 9], [0, 4, 5, 9]],  # S
        [[0, 1, 5, 6], [2, 5, 6, 9], [4, 5, 9, 10], [1, 4, 5, 8]],  # Z
        [[1, 4, 5, 6], [1, 5, 6, 9], [4, 5, 6, 9], [1, 4, 5, 9]],  # T
        [[1, 2, 5, 6]],  # O
    ]

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.type = random.randint(0, 6)
        self.color = random.randint(1, len(colours) - 1)
        self.rotation = 0

    def full_image(self):
        parts = set()
        for image in self.pieces[self.type][self.rotation]:
            i, j = int(image // 4), int(image % 4)
            parts.add((i, j))
            parts.add((i + 1, j))
            parts.add((i, j + 1))
            parts.add((i + 1, j + 1))

        return parts

    @property
    def image(self):

        return [
            (int(i // 4), int(i % 4)) for i in self.pieces[self.type][self.rotation]
        ]

    def rotate(self):
        self.rotation = (self.rotation + 1) % len(self.pieces[self.type])


class Sandtris:
    def __init__(self):
        self.grid = Grid()

        self.piece = None
        self.score = 0

    def new_piece(self):
        # self.piece = Piece(int(GAME_SCREEN_WIDTH / 2), 0)
        self.piece = Piece(10, 0)

    def intersects(self):
        for i, j in self.piece.full_image():
            x = j * 10 + self.piece.x
            y = i * 10 + self.piece.y
            if y > ROWS or x > COLS or x < 0 or self.grid.piece_touching(y, j * 10 + x):
                return True

    def press_space(self):
        while not self.intersects():
            self.piece.y += 1
        self.piece.y -= 1
        self.freeze()

    def go_down(self):
        self.piece.y += 1
        if self.intersects():
            self.piece.y -= 1
            self.freeze()

    def freeze(self):
        self.grid.place(
            [
                (i * 10 + self.piece.y, j * 10 + self.piece.x)
                for i, j in self.piece.image
            ],
            self.piece.color,
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
                self.piece.x += 10
            else:
                self.piece.x -= 10

            if count > 5:
                self.piece.rotation = old_rotation

                break

    def draw(self, win):
        if self.piece is not None:

            for i, j in self.piece.image:

                pygame.draw.rect(
                    win,
                    colours[self.piece.color],
                    [
                        GRAIN_SIZE * (10 * j + self.piece.x) + 0.5,
                        GRAIN_SIZE * (10 * i + self.piece.y) + 0.5,
                        PIECE_SIZE - 1,
                        PIECE_SIZE - 1,
                    ],
                )

    def update(self, win):
        if self.piece == None:
            self.new_piece()

        self.grid.update(win)
        self.draw(win)
