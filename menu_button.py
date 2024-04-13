import pygame

from font_util import get_font


class Button:
    """
    a class to represent buttons
     - handle drawing
     - check for clicks
    """

    font = get_font(24)

    def __init__(self, x, y, xsize, ysize, text, func=None):
        self.rect = pygame.Rect(x, y, xsize, ysize)
        self.rect.topleft = (x, y)
        self.x = x
        self.y = y
        self.text = text
        self.func = func
        self.xsize, self.ysize = xsize, ysize

    def draw(self, win):
        # draw button -------------------------------->
        pos = pygame.mouse.get_pos()
        # set colour
        if self.rect.collidepoint(pos):
            rect_colour = (21, 54, 66)
            text_colour = (235, 235, 235)
        else:
            rect_colour = (235, 235, 235)
            text_colour = (21, 54, 66)

        # draw outter box
        pygame.draw.rect(win, rect_colour, self.rect, border_radius=3)
        pygame.draw.rect(win, text_colour, self.rect, border_radius=3, width=2)

        # draw text
        img = Button.font.render(self.text, False, text_colour)
        win.blit(
            img,
            (
                self.rect.centerx - img.get_size()[0] / 2,
                self.rect.centery - img.get_size()[1] / 2,
            ),
        )

    def check_click(self):
        # check if clicked
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0]:
                return self.func if self.func else True

    def click(self):
        return self.func
