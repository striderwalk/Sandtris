from sandtris.tetris import Sandtris
from utils import get_font

large_font = get_font(38)
underline_large_font = get_font(38)
underline_large_font.set_underline(True)

small_font = get_font(20)


class Game:
    def __init__(self):
        self.tetris = Sandtris()

    def draw(self, win):

        # Update the game
        self.tetris.update(win)

    def update(self, win):

        # draw the game
        self.draw(win)
        if self.tetris.lost:
            screen = win.copy()
            return {"code": "lost", "screen": screen, "score": int(self.tetris.score)}

    def handle_event(self, event):
        self.tetris.handle_event(event)
