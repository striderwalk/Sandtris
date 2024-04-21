import pygame

from consts import *
from utils import Button, get_font

large_font = get_font(38)
underline_large_font = get_font(38)
underline_large_font.set_underline(True)


small_font = get_font(20)


def lost_loop(win, clock, score, screen):
    win.blit(screen, (0, 0))

    background = pygame.Surface(win.get_size(), flags=pygame.SRCALPHA)
    background.set_alpha(75)
    background.fill((0, 0, 0))
    win.blit(background, (0, 0))
    # render the text -------------------------------->
    lost_text = large_font.render("You have lost!", True, (21, 54, 66))
    score_text = small_font.render(
        f" You scored {int(score)} points", True, (21, 54, 66)
    )

    # draw the background
    text_surface = pygame.Surface(
        (
            lost_text.get_width() + 10,
            lost_text.get_height() + score_text.get_height() + 10,
        ),
        flags=pygame.SRCALPHA,
    )
    pygame.draw.rect(
        win,
        (
            215,
            215,
            215,
        ),
        (
            (WIDTH - text_surface.get_width()) / 2 - 4,
            (HEIGHT - text_surface.get_height()) / 2 - 4,
            text_surface.get_width() + 8,
            text_surface.get_height() + 80,
        ),
        border_radius=2,
    )
    # pygame.draw.rect(
    #     text_surface,
    #     (21, 54, 66),
    #     (
    #         2,
    #         2,
    #         lost_text.get_width() + 7,
    #         lost_text.get_height() + score_text.get_height() + 7,
    #     ),
    #     border_radius=5,
    # )
    pygame.draw.rect(
        text_surface,
        (245, 245, 245),
        (
            5,
            5,
            lost_text.get_width(),
            lost_text.get_height() + score_text.get_height(),
        ),
        border_radius=5,
    )

    # add the text to the background
    text_surface.blit(
        lost_text,
        (
            (text_surface.get_width() - lost_text.get_width()) / 2 + 5,
            5,
        ),
    )

    text_surface.blit(
        score_text,
        (
            (text_surface.get_width() - score_text.get_width()) / 2 + 5,
            lost_text.get_height() + 5,
        ),
    )

    win.blit(
        text_surface,
        (
            (WIDTH - text_surface.get_width()) / 2,
            (HEIGHT - text_surface.get_height()) / 2,
        ),
    )

    pygame.display.flip()

    exit = Button(
        (WIDTH + text_surface.get_width()) / 2 - 160,
        (HEIGHT + text_surface.get_height()) / 2 + 20,
        160,
        50,
        "Exit",
    )
    play_again = Button(
        (WIDTH - text_surface.get_width()) / 2,
        (HEIGHT + text_surface.get_height()) / 2 + 20,
        160,
        50,
        "Play again",
    )
    # Lost loop -------------------------------->
    while True:
        exit.draw(win)
        if exit.check_click():
            return {"code": "quit"}

        play_again.draw(win)
        if play_again.check_click():
            return {"code": "again"}

        pygame.display.flip()

        for event in pygame.event.get():
            # Game exiting
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            if event.type == pygame.KEYDOWN:
                # Game exiting
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    return
        pygame.display.set_caption(f"FPS: {clock.get_fps()}")

        clock.tick(FPS)
