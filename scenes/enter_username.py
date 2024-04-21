import pygame

from consts import *
from utils import Button, draw_scoreboard, get_font, write_score

large_font = get_font(38)
underline_large_font = get_font(38)
underline_large_font.set_underline(True)

small_font = get_font(20)


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
