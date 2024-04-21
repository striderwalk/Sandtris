import pygame

from consts import *
from utils import Button, draw_scoreboard, get_font

large_font = get_font(38)
underline_large_font = get_font(38)
underline_large_font.set_underline(True)

small_font = get_font(20)


def menu_loop(win, clock):

    # set the background colour
    win.fill((235, 235, 235))

    title_text = underline_large_font.render("Sandtris!", True, ((21, 54, 66)))
    win.blit(title_text, ((WIDTH - title_text.get_width()) / 2, 50))
    draw_scoreboard(win)

    exit = Button(
        (WIDTH) / 2 + 40,
        600,
        160,
        50,
        "Exit",
    )
    play = Button(
        (WIDTH) / 2 - 40 - 160,
        600,
        160,
        50,
        "Play",
    )
    # main loop -------------------------------->
    while True:
        exit.draw(win)
        if exit.check_click():
            return {"code": "quit"}

        play.draw(win)
        if play.check_click():
            return {"code": "again"}

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
