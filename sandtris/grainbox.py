import math
import random

import numpy as np
import pygame
import tcod
from numba import njit

from consts import (
    CHUNK_SIZE,
    COLOURS,
    COLS,
    GAME_SCREEN_HEIGHT,
    GAME_SCREEN_WIDTH,
    GRAIN_SIZE,
    POINTS_PER_GRAIN,
    ROWS,
)

colours_values = np.array(
    [
        np.array([pygame.Color(j).r, pygame.Color(j).g, pygame.Color(j).b])
        for j in (COLOURS)
    ]
)


@njit
def update_item(box: np.array, i: int, j: int, next_box: np.array):
    # move down ---------------------------------------------------------------->
    if i < ROWS - 1:
        # return move_down(box, i, j, next_box)
        if box[i + 1, j][0] == 0 and next_box[i + 1, j][0] == 0:
            # list of all swaps to be made
            swaps = [(i, j, i + 1, j)]

            # move all cell above down too
            if i == 0:
                return [(i, j, i, j)]

            for new_i in range(i - 1, -1, -1):

                if box[new_i, j, 0] == 0:
                    break

                swaps.append((new_i, j, new_i + 1, j))

            return swaps

    # check if items lifetime is over
    if box[i, j, 1] <= 0:
        return [(i, j, i, j)]

    # move left or right randomly -------------------------------->
    direction = [-1, 1][random.randint(0, 1)]
    new_j = j + direction
    if new_j < COLS and new_j >= 0:
        if box[i, new_j][0] == 0 and next_box[i, new_j][0] == 0:
            return [(i, j, i, new_j)]

    new_j = j - direction
    if new_j < COLS and new_j >= 0:
        if box[i, new_j][0] == 0 and next_box[i, new_j][0] == 0:
            return [(i, j, i, new_j)]

    next_box[i, j, 0] = box[i, j, 0]
    next_box[i, j, 1] = box[i, j, 1] - 1

    return [(i, j, i, j)]


@njit
def update_box(grainbox: np.array, chunks: np.array, surface_array: np.array):

    next_box = np.copy(grainbox)

    # Iterate over each chunk -------------------------------->
    for i_chunk in range(len(chunks)):
        for j_chunk in range(len(chunks[i_chunk])):

            if chunks[i_chunk, j_chunk] <= 0:

                continue

            # find real range chunk
            start_i = max(0, j_chunk * CHUNK_SIZE - 1)
            end_i = min(start_i + CHUNK_SIZE + 1, ROWS)

            start_j = max(0, i_chunk * CHUNK_SIZE - 1)
            end_j = min(start_j + CHUNK_SIZE + 1, COLS)

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
                    # Pass in the box if empty at i,j
                    if grainbox[i, j, 0] == 0:
                        continue
                    swaps = update_item(grainbox, i, j, next_box)

                    if not swaps:
                        continue
                    for i, j, new_i, new_j in swaps:
                        if i == new_i and j == new_j:
                            continue
                        change = True

                        # swap to the next position

                        next_box[new_i, new_j, 0] = grainbox[i, j, 0]
                        next_box[new_i, new_j, 1] = grainbox[i, j, 1] - 1

                        # reset the current position
                        next_box[i, j] = 0
                        grainbox[i, j] = 0

                        # draw the new position
                        surface_array[j, i, :] = colours_values[0]
                        surface_array[new_j, new_i, :] = colours_values[
                            next_box[new_i, new_j, 0]
                        ]
                        # upadate the chunk
                        chunks[int(j / CHUNK_SIZE), int(i / CHUNK_SIZE)] = 5

            if not change and chunks[i_chunk, j_chunk] > 0:
                chunks[i_chunk, j_chunk] -= 1

            else:
                for i in range(max(0, i_chunk - 1), min(i_chunk + 3, len(chunks))):

                    for j in range(
                        max(0, j_chunk - 1), min(j_chunk + 3, len(chunks[0]))
                    ):
                        if i == i_chunk and j == j_chunk:
                            continue

                        empty = np.all(
                            next_box[
                                j * CHUNK_SIZE : min((j + 1) * CHUNK_SIZE, ROWS) + 1,
                                i * CHUNK_SIZE : min((i + 1) * CHUNK_SIZE, COLS) + 1,
                            ]
                            == 0
                        )
                        if chunks[i, j] == 0:
                            if not empty:

                                chunks[i, j] = 1

    return next_box, chunks, surface_array


class GrainBox:
    def __init__(self):

        # Store the sand
        self.box = np.zeros((ROWS, COLS, 2), np.int8)

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
                chunk = self.box[
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

    def update_box(self):

        data = update_box(self.box, self.chunks, self.surface_array)

        self.box, self.chunks, self.surface_array = data
        return

    def clear_grain(self, i, j):
        self.box[i, j] = 0
        self.surface_array[j, i, :] = colours_values[self.box[i, j, 0]]

    def piece_touching(self, i, j):
        return not self.box[i, j, 0] == 0

    def place(self, image, colour):
        self.clear_puase = 0
        for i, j in image:
            self.chunks[int(j / CHUNK_SIZE), int(i / CHUNK_SIZE)] = 5
            self.chunks[
                math.floor((j / CHUNK_SIZE) - 1) : math.ceil((j / CHUNK_SIZE) + 1),
                math.floor((i / CHUNK_SIZE) - 1) : math.ceil((i / CHUNK_SIZE) + 1),
            ] = 5

            self.box[i : i + 10, j : j + 10, 0] = colour
            self.box[i : i + 10, j : j + 10, 1] = 50

            self.surface_array[j : j + 10, i : i + 10, :] = colours_values[colour]

    def update(self, win):

        if not self.clearing:
            self.update_box()
            score = self.clear()

        else:
            score = self.next_clear()

        self.draw(win)
        # self.draw_chunks(win)
        return score

    def clear(self):
        if np.all(self.chunks == 0):
            return
        # Get all the possible colours
        possible_colours = [
            colour
            for colour in range(1, len(COLOURS))
            if all(np.any(self.box[:, i, 0] == colour) for i in range(COLS))
        ]

        # For each possible colour
        for colour in possible_colours:

            # Setup the graph for the given colour
            graph = tcod.path.SimpleGraph(
                cost=np.where(self.box != colour, 0, self.box)[:, :, 0],
                cardinal=2,
                diagonal=3,
            )
            pathfinder = tcod.path.Pathfinder(graph)

            if points := self.colour_clear(colour, pathfinder):
                return points

    def colour_clear(self, colour, pathfinder):
        for i in range(ROWS):
            if self.box[i, 0, 0] == colour:
                if i != 0 and i != ROWS - 1:
                    if (
                        self.box[i, 0, 0] == self.box[i - 1, 0, 0]
                        and self.box[i, 0, 0] == self.box[i + 1, 0, 0]
                    ):
                        continue
                pathfinder.add_root((i, 0))
                for i in range(ROWS):
                    if i != 0 and i != ROWS - 1:
                        if (
                            self.box[i, -1, 0] == self.box[i - 1, -1, 0]
                            and self.box[i, -1, 0] == self.box[i + 1, -1, 0]
                        ):
                            continue

                    if self.box[i, COLS - 1, 0] == colour:

                        path = pathfinder.path_to((i, COLS - 1)).tolist()

                        if len(path) > 1:
                            self.clearing = True
                            self.path = set(tuple(i) for i in path)
                            self.new_path = self.path

                            self.clear_colour = colour
                            return len(path) * POINTS_PER_GRAIN
        return False

    def next_clear(self):
        self.new_path = set()
        next_path = set(self.path)

        for i, j in self.path:
            # Cardinals
            if j + 1 < COLS and self.box[i, j + 1, 0] == self.clear_colour:
                self.new_path.add((i, j + 1))
                next_path.add((i, j + 1))

            if j - 1 >= 0 and self.box[i, j - 1, 0] == self.clear_colour:
                self.new_path.add((i, j - 1))
                next_path.add((i, j - 1))

            if i + 1 < ROWS and self.box[i + 1, j, 0] == self.clear_colour:
                self.new_path.add((i + 1, j))
                next_path.add((i + 1, j))

            if i - 1 >= 0 and self.box[i - 1, j, 0] == self.clear_colour:
                self.new_path.add((i - 1, j))
                next_path.add((i - 1, j))

            # Diagonals
            if (
                j + 1 < COLS
                and i + 1 < ROWS
                and self.box[i + 1, j + 1, 0] == self.clear_colour
            ):
                self.new_path.add((i + 1, j + 1))
                next_path.add((i + 1, j + 1))

            if (
                j + 1 < COLS
                and i - 1 >= 0
                and self.box[i - 1, j + 1, 0] == self.clear_colour
            ):
                self.new_path.add((i - 1, j + 1))
                next_path.add((i - 1, j + 1))

            if (
                j - 1 >= 0
                and i + 1 < ROWS
                and self.box[i + 1, j - 1, 0] == self.clear_colour
            ):
                self.new_path.add((i, j - 1))
                next_path.add((i + 1, j - 1))

            if (
                j - 1 >= 0
                and i - 1 >= 0
                and self.box[i - 1, j - 1, 0] == self.clear_colour
            ):
                self.new_path.add((i - 1, j - 1))
                next_path.add((i - 1, j - 1))

        for i, j in self.path:
            self.clear_grain(i, j)

        if self.path == next_path:
            self.chunks[:, :] = 1
            self.clearing = False
            return 0
        self.path = next_path

        return len(next_path) * POINTS_PER_GRAIN
