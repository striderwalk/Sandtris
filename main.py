import random
import numpy as np
import pygame

from consts import *
from grid import Grid
from tetris import Sandtris


def main():

    # setup pygame
    pygame.init()
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    # setup grid
    tetris = Sandtris()
    run = True
    pressing_down = False
    count = 0

    # main game loop -------------------------------->
    while run:
        count += 1

        # Update the game
        tetris.update(win)
        if pressing_down or count % 3 == 0:

            tetris.go_down()
        if pressing_down:
            tetris.score_add(1)

        # handle pygame events -------------------------------->
        for event in pygame.event.get():
            # game exiting
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            if event.type == pygame.KEYDOWN:
                # game exiting
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    return

                # game inputs

                if event.key == pygame.K_SPACE:
                    tetris.press_space()
                if event.key == pygame.K_DOWN:
                    pressing_down = True
                if event.key == pygame.K_UP:
                    tetris.rotate()

                # debug tool
                if event.key == pygame.K_o:
                    tetris.new_piece()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:

                    pressing_down = False

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            tetris.go_side(-2)
        if keys[pygame.K_RIGHT]:
            tetris.go_side(2)

        # update frame
        pygame.display.flip()
        pygame.display.set_caption(f"FPS: {clock.get_fps()}")
        win.fill(pygame.Color("gray"))

        clock.tick(FPS)


if __name__ == "__main__":
    main()
