import pygame

from consts import *
from font_util import get_font
from menu_button import Button
from scorebored import draw_scoreboard, write_score
from tetris import Sandtris

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
        border_radius=5,
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


def add_scoreboard_loop(win, clock, score):
    title_text = underline_large_font.render("Sandtris!", True, ((21, 54, 66)))
    score_text_line_1 = small_font.render(
        f"You scored {score} points!",
        True,
        ((21, 54, 66)),
    )
    score_text_line_2 = small_font.render(
        f"Enter your name to get on the scoreboard.",
        True,
        ((21, 54, 66)),
    )

    current_username = ""

    # submit = Button(420, 160, 40, 47, "enter.png", file=True)
    submit = Button(420, 160, 40, 47, ">")

    while True:
        submit.draw(win)
        if submit.check_click():
            if current_username != "":
                write_score(current_username, score)
                return {"code": "again"}
            else:
                submit.unclick()

        draw_scoreboard(win, 80)
        win.blit(title_text, ((WIDTH - title_text.get_width()) / 2, 50))
        win.blit(score_text_line_1, ((WIDTH - score_text_line_1.get_width()) / 2, 100))
        win.blit(score_text_line_2, ((WIDTH - score_text_line_2.get_width()) / 2, 120))

        text = small_font.render(current_username, True, (0, 0, 0))

        pygame.draw.rect(
            win,
            pygame.Color("white"),
            (160, 160, 250, text.get_height() + 20),
            border_radius=5,
        )

        win.blit(text, ((WIDTH - text.get_width()) / 2, 170))

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
                if event.key == pygame.K_BACKSPACE and current_username:
                    current_username = current_username[:-1]

                if event.key == pygame.K_RETURN:
                    submit.click()

                if event.unicode and len(current_username) < 15:
                    char = chr(event.key)

                    if char.isprintable():
                        if pygame.key.get_mods() & pygame.KMOD_CAPS:
                            current_username += char.upper()

                        else:
                            current_username += char

        clock.tick(FPS)
        pygame.display.flip()
        win.fill((235, 235, 235))


def main():

    # setup pygame
    pygame.init()
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    exit_data = menu_loop(win, clock)
    if exit_data["code"] == "quit":
        pygame.quit()
        return
    while True:
        # Run the main game loop
        exit_data = main_game_loop(win, clock)

        if exit_data["code"] == "quit":
            pygame.quit()
            return

        # Run the lost game loop
        score = exit_data["score"]
        game_screen = exit_data["screen"]
        exit_data = lost_loop(win, clock, score, game_screen)

        if exit_data["code"] == "quit":
            pygame.quit()
            return
        else:
            add_scoreboard_loop(win, clock, score)


if __name__ == "__main__":
    main()
