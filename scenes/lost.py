import pygame

from consts import WIDTH, HEIGHT
from utils import Button, get_font

large_font = get_font(38)
underline_large_font = get_font(38)
underline_large_font.set_underline(True)


small_font = get_font(20)


class Lost:
    def __init__(self, game_screen, score):

        self.game_score = score
        self.game_screen = game_screen
        # dim the game screen
        background = pygame.Surface(self.game_screen.get_size(), flags=pygame.SRCALPHA)
        background.set_alpha(75)
        background.fill((0, 0, 0))
        self.game_screen.blit(background, (0, 0))

        # create the buttons
        self.exit_button = Button(
            (WIDTH + (332)) / 2 - 160,
            (HEIGHT + 88) / 2 + 20,
            160,
            50,
            "Exit",
        )
        self.again_button = Button(
            (WIDTH - 332) / 2,
            (HEIGHT + 88) / 2 + 20,
            160,
            50,
            "Play again",
        )

        # render the text -------------------------------->
        self.lost_text = large_font.render("You lost!", True, (21, 54, 66))
        self.score_text = small_font.render(
            f" You scored {int(self.game_score)} points", True, (21, 54, 66)
        )

        self.text_surface = pygame.Surface(
            (
                self.score_text.get_width() + 10,
                self.lost_text.get_height() + self.score_text.get_height() + 10,
            ),
            flags=pygame.SRCALPHA,
        )
        pygame.draw.rect(
            self.text_surface,
            (245, 245, 245),
            (
                5,
                5,
                self.score_text.get_width(),
                self.lost_text.get_height() + self.score_text.get_height(),
            ),
            border_radius=5,
        )

        # add the text to the background
        self.text_surface.blit(
            self.lost_text,
            (
                (self.text_surface.get_width() - self.lost_text.get_width()) / 2 + 5,
                5,
            ),
        )

        self.text_surface.blit(
            self.score_text,
            (
                (self.text_surface.get_width() - self.score_text.get_width()) / 2 + 5,
                self.lost_text.get_height() + 5,
            ),
        )

    def draw(self, win):
        win.blit(self.game_screen, (0, 0))

        # draw the background
        pygame.draw.rect(
            win,
            (
                215,
                215,
                215,
            ),
            (
                (WIDTH - self.text_surface.get_width()) / 2 - 4,
                (HEIGHT - self.text_surface.get_height()) / 2 - 4,
                self.text_surface.get_width() + 8,
                self.text_surface.get_height() + 80,
            ),
            border_radius=2,
        )

        # draw the static text
        win.blit(
            self.text_surface,
            (
                (WIDTH - self.text_surface.get_width()) / 2,
                (HEIGHT - self.text_surface.get_height()) / 2,
            ),
        )

        self.exit_button.draw(win)
        self.again_button.draw(win)

    def update(self, win):
        self.draw(win)
        if self.exit_button.check_click():
            return {"code": "quit"}
        if self.again_button.check_click():
            return {"code": "again"}

    def handle_event(self, event):
        pass
