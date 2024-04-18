import pygame


from font_util import get_font


class Button:
    """
    a class to represent buttons
     - handle drawing
     - check for clicks
    """

    font = get_font(24)

    def __init__(
        self,
        x,
        y,
        xsize,
        ysize,
        text,
        func=None,
        rect_colour=(21, 54, 66),
        text_colour=(235, 235, 235),
        file=False,
    ):
        self.rect = pygame.Rect(x, y, xsize, ysize)
        self.rect.topleft = (x, y)
        self.x = x
        self.y = y
        self.text = text
        self.func = func
        self.xsize, self.ysize = xsize, ysize
        self.clicked = False
        self.rect_colour = rect_colour
        self.text_colour = text_colour

        self.file = pygame.image.load(self.text) if file else False

    def draw(self, win):
        # draw button -------------------------------->
        pos = pygame.mouse.get_pos()
        # set colour
        if self.rect.collidepoint(pos):
            pygame.draw.rect(win, self.rect_colour, self.rect, border_radius=3)
            pygame.draw.rect(win, self.text_colour, self.rect, border_radius=3, width=2)
            text = Button.font.render(self.text, False, self.text_colour)
            if self.file:
                text = self.file

        else:

            pygame.draw.rect(win, self.text_colour, self.rect, border_radius=3)
            pygame.draw.rect(win, self.rect_colour, self.rect, border_radius=3, width=2)
            text = Button.font.render(self.text, False, self.rect_colour)
            if self.file:
                text = self.file

        # draw outter box

        # draw text
        win.blit(
            text,
            (
                self.rect.centerx - text.get_size()[0] / 2,
                self.rect.centery - text.get_size()[1] / 2,
            ),
        )

    def check_click(self):
        # check if clicked
        pos = pygame.mouse.get_pos()
        if (
            self.rect.collidepoint(pos) and pygame.mouse.get_pressed()[0]
        ) or self.clicked:

            return self.func if self.func else True

    def click(self):
        self.clicked = True

    def unclick(self):
        self.clicked = False
