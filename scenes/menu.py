from consts import WIDTH

from utils import Button, draw_scoreboard, get_font

large_font = get_font(38)
underline_large_font = get_font(38)
underline_large_font.set_underline(True)

small_font = get_font(20)


class Menu:
    def __init__(self):
        self.exit_button = Button((WIDTH) / 2 + 40, 600, 160, 50, "Exit")
        self.play_button = Button((WIDTH) / 2 - 40 - 160, 600, 160, 50, "Play")

    def draw(self, win):
        title_text = underline_large_font.render("Sandtris!", True, ((21, 54, 66)))
        win.blit(title_text, ((WIDTH - title_text.get_width()) / 2, 50))
        draw_scoreboard(win)

        self.exit_button.draw(win)

        self.play_button.draw(win)

    def update(self, win):
        self.draw(win)
        if self.play_button.check_click():
            return {"code": "again"}
        if self.exit_button.check_click():
            return {"code": "quit"}

    def handle_event(self, event):
        pass
