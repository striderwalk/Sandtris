import pygame

from consts import *
from utils import draw_scoreboard, get_font

large_font = get_font(38)
underline_large_font = get_font(38)
underline_large_font.set_underline(True)

small_font = get_font(20)


def loading_loop(win, clock):
    # set the background colour
    win.fill((235, 235, 235))

    title_text = large_font.render("Loading", True, ((21, 54, 66)))
    win.blit(title_text, ((WIDTH - title_text.get_width()) / 2, 50))
    draw_scoreboard(win)

    # main loop -------------------------------->
    for _ in range(500):

        pygame.display.flip()
        # Handle pygame events -------------------------------->
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

            pygame.display.flip()
            pygame.display.set_caption(f"FPS: {clock.get_fps()}")

            clock.tick(FPS)

    return {"code": "again"}
