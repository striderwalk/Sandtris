import math
import random
from copy import deepcopy

import numpy as np
import pygame
import tcod

from consts import *

colours_dict = {
    i: np.array([pygame.Color(j).r, pygame.Color(j).g, pygame.Color(j).b])
    for i, j in enumerate(COLOURS)
}


class Grid:
    def __init__(self):

        # Store the sand
        self.grid = np.zeros((ROWS, COLS, 2), np.int8)

        self.surface_array = np.zeros((COLS, ROWS, 3), np.int8)

        # Chunks used to optimize sand updates
        chucks_width = int(np.ceil(COLS / CHUNK_SIZE))
        chucks_height = int(np.ceil(ROWS / CHUNK_SIZE))

        self.chunks = np.ones((chucks_width, chucks_height), np.int8)

        # Surface to draw sand to
        self.screen = pygame.Surface((GAME_SCREEN_WIDTH, GAME_SCREEN_HEIGHT))
        self.screen.fill(pygame.Color("white"))

        self.clearing = False

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

    def draw(self, win):

        surface = pygame.Surface((COLS, ROWS))
        pygame.surfarray.blit_array(surface, self.surface_array)
        surface = pygame.transform.scale(
            surface,
            (
                COLS * GRAIN_SIZE,
                ROWS * GRAIN_SIZE,
            ),
        )

        win.blit(surface, (0, 0))

        if self.clearing:

            for j, i in self.new_path:
                pygame.draw.rect(
                    win,
                    (255, 255, 255),
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
                    range(end_i - 1, start_i - 1, -1)
                    if random.random() < 0.5
                    else range(start_i, end_i)
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

    def clear_grain(self, i, j):
        self.grid[i, j] = 0
        self.surface_array[j, i, :] = colours_dict[self.grid[i, j, 0]]

    def swap_grain(self, i, j, new_i, new_j, next_grid):
        # swap to the next position
        next_grid[new_i, new_j, 0] = self.grid[i, j, 0]
        next_grid[new_i, new_j, 1] = self.grid[i, j, 1] - 1

        # reset the current position
        next_grid[i, j] = 0
        self.grid[i, j] = 0

        # draw the new position
        self.surface_array[j, i, :] = colours_dict[0]
        self.surface_array[new_j, new_i, :] = colours_dict[next_grid[new_i, new_j, 0]]

    def update_item(self, i, j, next_grid):

        # check if empty
        if self.grid[i, j, 0] == 0:
            return False

        direction = random.choice([-1, 1])
        # move down
        if i < ROWS - 1:

            if self.grid[i + 1, j][0] == 0 and next_grid[i + 1, j][0] == 0:

                # swap the grain to its new position
                self.swap_grain(i, j, i + 1, j, next_grid)

                # move all cell above down too
                if i == 0:
                    return True
                for new_i in range(i - 1, -1, -1):

                    if self.grid[new_i, j, 0] == 0:
                        break

                    self.swap_grain(new_i, j, new_i + 1, j, next_grid)

                self.chunks[
                    int(j / CHUNK_SIZE) - 1 : int(j / CHUNK_SIZE) + 2,
                    int(new_i / CHUNK_SIZE) - 1 : int(i / CHUNK_SIZE) + 1,
                ] = 5

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

                self.swap_grain(i, j, i, j + direction, next_grid)

                return True

        if j - direction < COLS and j - direction >= 0:
            if (
                self.grid[i, j - direction][0] == 0
                and next_grid[i, j - direction][0] == 0
            ):
                self.swap_grain(i, j, i, j - direction, next_grid)

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
        return not self.grid[i, j, 0] == 0

    def place(self, image, colour):
        self.clear_puase = 0
        for i, j in image:
            self.chunks[int(j / CHUNK_SIZE), int(i / CHUNK_SIZE)] = 5
            self.chunks[
                math.floor((j / CHUNK_SIZE) - 1) : math.ceil((j / CHUNK_SIZE) + 1),
                math.floor((i / CHUNK_SIZE) - 1) : math.ceil((i / CHUNK_SIZE) + 1),
            ] = 5

            self.grid[i : i + 10, j : j + 10, 0] = colour
            self.grid[i : i + 10, j : j + 10, 1] = 50

            self.surface_array[j : j + 10, i : i + 10, :] = colours_dict[colour]

    def update(self, win):

        if not self.clearing:
            self.update_grid()
            score = self.clear()
        else:
            score = self.next_clear()

        self.draw(win)
        # self.draw_chunks(win)
        return score

    def clear(self):
        # Get all the possible colours
        possible_colours = [
            colour
            for colour in range(1, len(COLOURS))
            if all(colour in self.grid[:, i, 0] for i in range(COLS))
        ]

        # For each possible colour
        for colour in possible_colours:

            # Setup the graph for the given colour
            graph = tcod.path.SimpleGraph(
                cost=np.where(self.grid != colour, 0, self.grid)[:, :, 0],
                cardinal=2,
                diagonal=3,
            )
            pathfinder = tcod.path.Pathfinder(graph)

            for i in range(ROWS):

                if self.grid[i, 0, 0] == colour:
                    if i != 0 and i != ROWS - 1:
                        if (
                            self.grid[i, 0, 0] == self.grid[i - 1, 0, 0]
                            and self.grid[i, 0, 0] == self.grid[i + 1, 0, 0]
                        ):
                            continue
                    pathfinder.add_root((i, 0))
                    for i in range(ROWS):
                        if i != 0 and i != ROWS - 1:
                            if (
                                self.grid[i, -1, 0] == self.grid[i - 1, -1, 0]
                                and self.grid[i, -1, 0] == self.grid[i + 1, -1, 0]
                            ):
                                continue

                        if self.grid[i, COLS - 1, 0] == colour:

                            path = pathfinder.path_to((i, COLS - 1)).tolist()

                            if len(path) > 1:

                                self.clearing = True
                                self.path = set(tuple(i) for i in path)
                                self.new_path = self.path

                                self.clear_colour = colour
                                self.chunks[:, :] = 1
                                return len(path) * POINTS_PER_GRAIN

    def next_clear(self):
        self.new_path = set()
        next_path = set(self.path)

        for i, j in self.path:
            # Cardinals
            if j + 1 < COLS and self.grid[i, j + 1, 0] == self.clear_colour:
                self.new_path.add((i, j + 1))
                next_path.add((i, j + 1))

            if j - 1 >= 0 and self.grid[i, j - 1, 0] == self.clear_colour:
                self.new_path.add((i, j - 1))
                next_path.add((i, j - 1))

            if i + 1 < ROWS and self.grid[i + 1, j, 0] == self.clear_colour:
                self.new_path.add((i + 1, j))
                next_path.add((i + 1, j))

            if i - 1 >= 0 and self.grid[i - 1, j, 0] == self.clear_colour:
                self.new_path.add((i - 1, j))
                next_path.add((i - 1, j))

            # Diagonals
            if (
                j + 1 < COLS
                and i + 1 < ROWS
                and self.grid[i + 1, j + 1, 0] == self.clear_colour
            ):
                self.new_path.add((i + 1, j + 1))
                next_path.add((i + 1, j + 1))

            if (
                j + 1 < COLS
                and i - 1 >= 0
                and self.grid[i - 1, j + 1, 0] == self.clear_colour
            ):
                self.new_path.add((i - 1, j + 1))
                next_path.add((i - 1, j + 1))

            if (
                j - 1 >= 0
                and i + 1 < ROWS
                and self.grid[i + 1, j - 1, 0] == self.clear_colour
            ):
                self.new_path.add((i, j - 1))
                next_path.add((i + 1, j - 1))

            if (
                j - 1 >= 0
                and i - 1 >= 0
                and self.grid[i - 1, j - 1, 0] == self.clear_colour
            ):
                self.new_path.add((i - 1, j - 1))
                next_path.add((i - 1, j - 1))

        for i, j in self.path:
            self.clear_grain(i, j)

        if self.path == next_path:
            self.clearing = False
            return 0
        self.path = next_path

        return len(next_path) * POINTS_PER_GRAIN