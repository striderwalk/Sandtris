import random

import pygame

from consts import (
    COLS,
    GAME_SCREEN_HEIGHT,
    GAME_SCREEN_WIDTH,
    GRAIN_SIZE,
    PIECE_SIZE,
    ROWS,
    COLOURS,
)
from utils.font_util import get_font
from sandtris.grid import Grid


font = get_font(20)


class Piece:

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
        self.color = random.randint(1, len(COLOURS) - 1)
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

    def draw(self, win):
        # Draw the current piece
        for i, j in self.image:

            pygame.draw.rect(
                win,
                COLOURS[self.color],
                [
                    GRAIN_SIZE * (10 * j + self.x) + 0.5,
                    GRAIN_SIZE * (10 * i + self.y) + 0.5,
                    PIECE_SIZE - 1,
                    PIECE_SIZE - 1,
                ],
            )


class Sandtris:
    def __init__(self):
        self.grid = Grid()

        self.piece = Piece(13, 0)
        self.next_piece = Piece(13, 0)
        self.score = 0
        self.count = 0
        self.pressing_down = False
        self.lost = False

    def new_piece(self):

        self.piece = self.next_piece
        self.next_piece = Piece(13, 0)
        if self.intersects():
            self.lost = True

    def intersects(self):
        for i, j in self.piece.full_image():
            x = j * 10 + self.piece.x
            y = i * 10 + self.piece.y
            if y > ROWS - 1 or x > COLS - 1 or x < 0 or self.grid.piece_touching(y, x):
                return True

    def press_space(self):
        score = 0
        while not self.intersects():
            score += 1
            self.piece.y += 1
        self.piece.y -= 1
        self.freeze()
        self.score_add(score)

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
        if not self.piece:
            return

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

    def score_add(self, score):
        self.score += score

    def draw(self, win):
        # Draw the score
        text = font.render(f"Score {int(self.score)}", True, pygame.Color("black"))
        win.blit(text, (400, 30))

        # Draw the next piece
        surface = pygame.Surface((200, 150))
        surface.fill((215, 215, 215))
        for i, j in self.next_piece.image:

            pygame.draw.rect(
                surface,
                COLOURS[self.next_piece.color],
                [
                    GRAIN_SIZE * (10 * j + self.next_piece.x) + 10.5,
                    GRAIN_SIZE * (10 * i + self.next_piece.y) + 10.5,
                    PIECE_SIZE - 1,
                    PIECE_SIZE - 1,
                ],
            )
        win.blit(surface, ((400, 60)))

    def update(self, win):
        # Get new piece if needed
        if self.piece is None and not pygame.key.get_pressed()[pygame.K_o]:
            self.new_piece()

        # Move the piece down
        if self.pressing_down or self.count % 3 == 0 and self.piece:
            self.go_down()

        # Add to the score is the down key is pressed
        if self.pressing_down:
            self.score_add(1)

        # Move to the side
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.go_side(-2)
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.go_side(2)

        screen = pygame.Surface((GAME_SCREEN_WIDTH, GAME_SCREEN_HEIGHT))
        # update the sand simulation
        new_points = self.grid.update(screen)
        if new_points:
            # added any new points
            self.score_add(new_points)

        # draw the current piece
        if self.piece:
            self.piece.draw(screen)
        win.blit(screen, (18, 18))

        # Draw the ui
        self.draw(win)

    def handle_event(self, event):
        if self.piece is None:
            return

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_SPACE:
                self.press_space()
            if event.key in [pygame.K_DOWN, pygame.K_s]:
                self.pressing_down = True
            if event.key in [pygame.K_UP, pygame.K_w]:
                self.rotate()

        if event.type == pygame.KEYUP:
            if event.key in [pygame.K_DOWN, pygame.K_s]:

                self.pressing_down = False
