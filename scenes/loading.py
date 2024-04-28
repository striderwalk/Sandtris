import random

from consts import WIDTH
from utils import draw_scoreboard, get_font

large_font = get_font(38)
underline_large_font = get_font(38)
underline_large_font.set_underline(True)

small_font = get_font(20)


class Loading:
    def __init__(self):
        self.life_time = random.binomialvariate(200, 0.6)
        self.title_text = large_font.render("Loading", True, ((21, 54, 66)))

    def draw(self, win):
        # draw the screen
        win.blit(self.title_text, ((WIDTH - self.title_text.get_width()) / 2, 50))
        draw_scoreboard(win)

    def update(self, win):
        # loading time
        self.life_time -= 1
        if self.life_time < 0:
            return {"code": "done"}

        # draw the screen
        self.draw(win)

    def handle_event(self, event):
        pass
