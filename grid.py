from copy import deepcopy
import math
from queue import Queue
import random

import numpy as np
import pygame
from tqdm import tqdm

from consts import *

colours = np.array(["black", "red", "green", "blue", "yellow"])


class Grid:
    def __init__(self):

        # Store the sand
        self.grid = np.zeros((ROWS, COLS, 2), np.int16)

        # Chunks used to optimize sand updates
        chucks_width = int(np.ceil(COLS / CHUNK_SIZE))
        chucks_height = int(np.ceil(ROWS / CHUNK_SIZE))

        self.chunks = np.array(
            ([[2 for _ in range(chucks_height)] for _ in range(chucks_width)])
        )

        # Surface to draw sand to
        self.screen = pygame.Surface((GAME_SCREEN_WIDTH, GAME_SCREEN_HEIGHT))
        self.screen.fill(pygame.Color("white"))

        # Store current possible paths to optimize line clearing
        self.clear_puase = 0

    def check_chunks(self):
        for i in range(len(self.chunks)):
            for j in range(len(self.chunks[i])):
                chunk = self.grid[
                    i * CHUNK_SIZE + 1 : min(i * CHUNK_SIZE + CHUNK_SIZE + 1, COLS + 1),
                    j * CHUNK_SIZE + 1 : min(j * CHUNK_SIZE + CHUNK_SIZE + 1, ROWS + 1),
                ]

                if (chunk == 0).all():
                    self.chunks[i, j] = 0

                else:
                    self.chunks[i, j] = 5

    def draw(self):

        for i_chunk in range(len(self.chunks)):
            for j_chunk in range(len(self.chunks[i_chunk])):
                if self.chunks[i_chunk, j_chunk] == 0:
                    continue

                for i in range(i_chunk * CHUNK_SIZE, (i_chunk + 1) * CHUNK_SIZE):
                    for j in range(j_chunk * CHUNK_SIZE, (j_chunk + 1) * CHUNK_SIZE):
                        colour = colours[self.grid[j, i, 0]]
                        pygame.draw.rect(
                            self.screen,
                            pygame.Color(colour),
                            (i * GRAIN_SIZE, j * GRAIN_SIZE, GRAIN_SIZE, GRAIN_SIZE),
                        )

    def draw_chunks(self, win):
        my_font = pygame.font.SysFont("Helvetica", 30)

        for i in range(len(self.chunks)):
            for j in range(len(self.chunks[i])):
                if self.chunks[i, j] <= 0:
                    continue
                text_surface = my_font.render(
                    str(self.chunks[i, j]), False, pygame.Color("white")
                )
                chunk_size = CHUNK_SIZE * GRAIN_SIZE
                win.blit(text_surface, ((i) * chunk_size, (j) * chunk_size))
                width = (
                    chunk_size
                    if (i) * chunk_size + chunk_size < GRAIN_SIZE * COLS
                    else -(i) * chunk_size + GRAIN_SIZE * COLS - 2
                )
                height = (
                    chunk_size
                    if (j) * chunk_size + chunk_size < GRAIN_SIZE * ROWS
                    else -(j) * chunk_size + GRAIN_SIZE * ROWS - 2
                )
                pygame.draw.rect(
                    win,
                    pygame.Color("cyan"),
                    (
                        (i) * chunk_size,
                        (j) * chunk_size,
                        width,
                        height,
                    ),
                    width=1,
                )

    def update_grid(self):
        next_grid = deepcopy(self.grid)

        # Iterate over each chunk -------------------------------->
        for i_chunk in range(len(self.chunks)):
            for j_chunk in range(len(self.chunks[i_chunk])):

                if self.chunks[i_chunk, j_chunk] <= 0:

                    continue

                # find real range chunk
                start_i = max(0, i_chunk * CHUNK_SIZE - 1)
                end_i = min(start_i + CHUNK_SIZE + 1, COLS)

                start_j = max(0, j_chunk * CHUNK_SIZE - 1)
                end_j = min(start_j + CHUNK_SIZE + 1, ROWS)

                # pick the direction to iterate
                i_range = (
                    range(start_i, end_i)
                    if random.random() < 0.5
                    else range(end_i - 1, start_i - 1, -1)
                )

                j_range = (
                    range(start_j, end_j)
                    if random.random() < 0.5
                    else range(end_j - 1, start_j - 1, -1)
                )

                change = False

                for i in i_range:
                    for j in j_range:
                        change = (self.update_item(j, i, next_grid)) or change

                if not change and self.chunks[i_chunk, j_chunk] > 0:
                    self.chunks[i_chunk, j_chunk] -= 1
                else:

                    self.check_neighbours(i_chunk, j_chunk)

        self.grid = next_grid

    def update_item(self, i, j, next_grid):

        # check if empty
        if self.grid[i, j, 0] == 0:
            return False

        direction = random.choice([-1, 1])
        # move down
        if i < ROWS - 1:

            if self.grid[i + 1, j][0] == 0 and next_grid[i + 1, j][0] == 0:
                next_grid[i + 1, j, 0] = self.grid[i, j, 0]
                next_grid[i + 1, j, 1] = self.grid[i, j, 1] - 1

                next_grid[i, j] = 0
                self.grid[i, j] = 0

                return True

        # check if lifetime is over
        if self.grid[i, j, 1] <= 0:
            return False
        # move left or right randomly
        if j + direction < COLS and j + direction >= 0:
            if (
                self.grid[i, j + direction][0] == 0
                and next_grid[i, j + direction][0] == 0
            ):
                next_grid[i, j + direction, 0] = self.grid[i, j, 0]
                next_grid[i, j + direction, 1] = self.grid[i, j, 1] - 1

                next_grid[i, j] = 0
                self.grid[i, j] = 0

                return True

        if j - direction < COLS and j - direction >= 0:
            if (
                self.grid[i, j - direction][0] == 0
                and next_grid[i, j - direction][0] == 0
            ):
                next_grid[i, j - direction, 0] = self.grid[i, j, 0]
                next_grid[i, j - direction, 1] = self.grid[i, j, 1] - 1
                next_grid[i, j] = 0
                self.grid[i, j] = 0

                return True

        next_grid[i, j, 0] = self.grid[i, j, 0]
        next_grid[i, j, 1] = self.grid[i, j, 1] - 1

        return False

    def check_neighbours(self, i_chunk, j_chunk):
        for i in range(max(0, i_chunk - 1), min(i_chunk + 2, len(self.chunks))):

            for j in range(max(0, j_chunk - 1), min(j_chunk + 2, len(self.chunks[0]))):
                if self.chunks[i, j] == 0:
                    if np.all(self.chunks[i, j] == 0):

                        self.chunks[i, j] = 1
                    else:
                        self.chunks[i, j] = -1

    def piece_touching(self, i, j):

        ratio = 1
        y = int(j * ratio)
        x = int(i * ratio)

        return not np.all(self.grid[x : x + ratio, y : y + ratio] == 0)

    def place(self, image, colour):
        self.clear_puase = 0
        for i, j in image:
            self.chunks[
                math.floor((j / CHUNK_SIZE) - 1) : math.ceil((j / CHUNK_SIZE) + 1),
                math.floor((i / CHUNK_SIZE) - 1) : math.ceil((i / CHUNK_SIZE) + 1),
            ] = 5

            self.grid[i : i + 10, j : j + 10, 0] = colour
            self.grid[i : i + 10, j : j + 10, 1] = 50

    def update(self, win):
        self.update_grid()

        self.draw()
        self.clear()
        win.blit(self.screen, (0, 0))
        self.draw_chunks(win)

        # self.chunks[:, 20:] = 1

    def _find_colour_path(self, colour, row):
        path = {(row, 0)}
        new = {(row, 0)}

        complete = False

        while not complete:

            next_new = set()

            for i, j in new:
                if j + 1 < COLS and self.grid[i, j + 1, 0] == colour:
                    if (i, j + 1) not in path and (i, j + 1) not in new:
                        next_new.add((i, j + 1))

                if i + 1 < ROWS and self.grid[i + 1, j, 0] == colour:
                    if (i + 1, j) not in path and (i + 1, j) not in new:

                        next_new.add((i + 1, j))
                if i - 1 >= 0 and self.grid[i - 1, j, 0] == colour:
                    if (i - 1, j) not in path and (i - 1, j) not in new:

                        next_new.add((i - 1, j))

                if j - 1 >= 0 and self.grid[i, j - 1, 0] == colour:
                    if (i, j - 1) not in path and (i, j - 1) not in new:
                        next_new.add((i, j - 1))

            if not next_new:
                complete = True

            path = path.union(new)
            new = next_new

        return path

    def find_colour_path(self, colour):

        # find the start point of a possible colour line
        last_path = set()

        for row in range(ROWS):

            # check if the current start point is the correct colour

            if self.grid[row, 0, 0] != colour:
                continue

            # check if has already been seen
            if (row, 0) in last_path:
                continue

            # Find the points in the path
            path = self._find_colour_path(colour, row)

            # Check if the path is completed
            if any(j == COLS - 1 for i, j in path):
                for i, j in path:
                    self.grid[i, j, 0] = 0

                self.chunks[:, :] = 5

            else:
                saved_path = set()
                for i, j in path:
                    if self.grid[i, j, 1] <= 0:
                        saved_path.add((i, j))
            if path:

                path_list = list(path)

                for i in range(len(path_list)):

                    pygame.draw.circle(
                        self.screen,
                        (255, 255, 255),
                        (
                            path_list[i][1] * GRAIN_SIZE,
                            path_list[i][0] * GRAIN_SIZE,
                        ),
                        1,
                    )
            last_path = path

        # pygame.display.flip()

    def clear(self):

        if self.clear_puase == 1:
            return
        if self.clear_puase > 0:
            self.clear_puase -= 1
        # find all colours that have a grain in each coloumn
        possible_colours = [
            colour
            for colour in range(1, len(colours))
            if all(colour in self.grid[:, i, 0] for i in range(COLS))
        ]

        if not np.all(self.chunks == 0):
            self.clear_puase = 2

        # for each colour check if there is a possible path
        _possible_colours = []
        for colour in possible_colours:
            left_min, right_min, left_max, right_max = ROWS - 1, ROWS - 1, 0, 0
            for row in range(ROWS - 1):
                if self.grid[row, 0, 0] == colour:
                    left_min = min(left_min, row)
                    left_max = max(left_max, row)

                if self.grid[row, -1, 0] == colour:
                    right_min = min(right_min, row)
                    right_max = max(right_max, row)
            possible = True
            if left_min < right_max:
                for i in range(left_min + 1, right_max):
                    if colour not in self.grid[i, :, 0]:
                        possible = False

            if left_max > right_min:
                for i in range(right_min + 1, left_max):
                    if colour not in self.grid[i, :, 0]:
                        possible = False
            if possible:

                _possible_colours.append(colour)

        possible_colours = _possible_colours
        # for each possible colour
        for colour in possible_colours:
            self.find_colour_path(colour)
