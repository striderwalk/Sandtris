import pygame

from consts import WIDTH
from utils import Button, draw_scoreboard, get_font, write_score

large_font = get_font(38)
underline_large_font = get_font(38)
underline_large_font.set_underline(True)

small_font = get_font(20)


class Scoreboard:
    def __init__(self, score):
        self.game_score = score

        self.submit_button = Button(420, 160, 40, 47, ">")
        self.current_username = ""
        self.title_text = underline_large_font.render("Sandtris!", True, ((21, 54, 66)))

        self.score_text_line_1 = small_font.render(
            f"You scored {self.game_score} points!", True, ((21, 54, 66)),
        )
        self.score_text_line_2 = small_font.render(
            "Enter your name to get on the scoreboard.", True, ((21, 54, 66)),
        )

    def draw(self, win):
        # draw all of the static text
        win.blit(self.title_text, ((WIDTH - self.title_text.get_width()) / 2, 50))
        win.blit(
            self.score_text_line_1,
            ((WIDTH - self.score_text_line_1.get_width()) / 2, 100),
        )
        win.blit(
            self.score_text_line_2,
            ((WIDTH - self.score_text_line_2.get_width()) / 2, 120),
        )

        draw_scoreboard(win, 80)
        text = small_font.render(self.current_username, True, (0, 0, 0))

        pygame.draw.rect(
            win,
            pygame.Color("white"),
            (160, 160, 250, text.get_height() + 20),
            border_radius=5,
        )

        win.blit(text, ((WIDTH - text.get_width()) / 2, 170))

    def update(self, win):
        self.draw(win)

        self.submit_button.draw(win)
        if self.submit_button.check_click():
            if self.current_username != "":
                write_score(self.current_username, self.game_score)
                return {"code": "again"}
            else:
                self.submit_button.unclick()

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE and self.current_username:
                self.current_username = self.current_username[:-1]

            if event.key == pygame.K_RETURN:
                self.submit_button.click()

            if event.unicode and len(self.current_username) < 15:
                char = chr(event.key)

                if char.isprintable():
                    if pygame.key.get_mods() & pygame.KMOD_CAPS:
                        self.current_username += char.upper()

                    else:
                        self.current_username += char
