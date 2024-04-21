import pygame

from consts import *
from tetris import Sandtris
from utils import get_font

large_font = get_font(38)
underline_large_font = get_font(38)
underline_large_font.set_underline(True)

small_font = get_font(20)


def main_game_loop(win, clock):
    tetris = Sandtris()
    # main game loop -------------------------------->
    while True:

        # Update the game
        tetris.update(win)

        # handle pygame events -------------------------------->
        for event in pygame.event.get():
            # Game exiting
            if event.type == pygame.QUIT:
                pygame.quit()
                return {"code": "quit"}

            if event.type == pygame.KEYDOWN:
                # Game exiting
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    return {"code": "quit"}

            # If the event is needs to be handled by the tetris game
            tetris.handle_event(event)

        if tetris.lost:
            screen = win.copy()
            return {"code": "lost", "screen": screen, "score": int(tetris.score)}

        # update frame
        pygame.display.flip()
        pygame.display.set_caption(f"FPS: {clock.get_fps()}")
        win.fill((215, 215, 215))

        clock.tick(FPS)
