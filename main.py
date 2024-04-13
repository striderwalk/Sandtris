import pygame

from consts import *
from font_util import get_font
from menu_button import Button
from tetris import Sandtris

large_font = get_font(38)
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
            return {"code": "lost", "screen": screen, "score": tetris.score}

        # update frame
        pygame.display.flip()
        pygame.display.set_caption(f"FPS: {clock.get_fps()}")
        win.fill((215, 215, 215))

        clock.tick(FPS)


def lost_loop(win, clock, score, screen):
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
        text_surface,
        (21, 54, 66),
        (
            2,
            2,
            lost_text.get_width() + 7,
            lost_text.get_height() + score_text.get_height() + 7,
        ),
        border_radius=5,
    )
    pygame.draw.rect(
        text_surface,
        (235, 235, 235),
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

    win.blit(screen, (0, 0))
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
        "Play again?",
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


def main():

    # setup pygame
    pygame.init()
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    while True:
        # Run the main game loop
        exit_data = main_game_loop(win, clock)

        if exit_data["code"] == "quit":
            return

        # Run the lost game loop
        score = exit_data["score"]
        game_screen = exit_data["screen"]
        exit_data = lost_loop(win, clock, score, game_screen)

        if exit_data["code"] == "quit":
            return


if __name__ == "__main__":
    main()
