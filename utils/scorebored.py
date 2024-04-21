import csv


import pygame

from consts import *
from utils import get_font


def load_scoreboard():
    # load the scoreboard
    with open("assets/scorebored.csv", "r", newline="") as file:

        scoreboard = [(data[0], int(data[1])) for data in csv.reader(file) if data]

    # return in ascending score order
    return sorted(scoreboard, key=lambda x: x[1], reverse=True)


def write_score(name: str, score: int):
    if not name:
        raise ValueError("Name must not be empty")
    # load the scorebored
    with open("assets/scorebored.csv", "a", newline="") as file:
        # write the name and score to the file
        writer = csv.writer(file)
        writer.writerow([name, score])


def draw_scoreboard(win: pygame.Surface, y_offset: int = 0):

    scoreboard = load_scoreboard()
    large_font = get_font(40)
    small_font = get_font(20)

    # setup the surface
    surf = pygame.Surface((300, 430), flags=pygame.SRCALPHA)
    # surf.set_alpha(0)
    pygame.draw.rect(surf, (255, 255, 255, 255), (0, 0, 300, 500), border_radius=3)

    scoreboard_text = large_font.render("Scoreboard", True, (0, 0, 0))
    surf.blit(scoreboard_text, (10, 10))

    for index in range(min(12, len(scoreboard))):
        name, score = scoreboard[index]
        name = small_font.render(f"{name}:", True, (0, 0, 0))
        surf.blit(name, (10, scoreboard_text.get_height() + 20 + 35 * (index)))

        score = small_font.render(str(score).zfill(5), True, (0, 0, 0))
        surf.blit(
            score,
            (
                surf.get_width() - score.get_width() - 20,
                scoreboard_text.get_height() + 20 + 35 * (index),
            ),
        )

    win.blit(surf, ((WIDTH - 300) / 2, 140 + y_offset))
