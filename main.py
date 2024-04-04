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
    tetris_screen = pygame.surface.Surface((GAME_SCREEN_WIDTH, GAME_SCREEN_HEIGHT))
    pressing_down = False
    count = 0
    while run:
        count += 1

        # update gane aspects
        tetris.update(tetris_screen)
        if pressing_down or count % 3 == 0:
            tetris.go_down()

        # draw game
        win.blit(tetris_screen, (10, 10))

        # handle pygame events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    return

                if event.key == pygame.K_SPACE:
                    tetris.press_space()
                if event.key == pygame.K_DOWN:
                    pressing_down = True
                if event.key == pygame.K_UP:
                    tetris.rotate()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    pressing_down = False

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            tetris.go_side(-1)
        if keys[pygame.K_RIGHT]:
            tetris.go_side(1)

        # update frame
        pygame.display.flip()
        pygame.display.set_caption(f"FPS: {clock.get_fps()}")
        win.fill(pygame.Color("gray"))
        tetris_screen.fill(pygame.Color("black"))

        clock.tick(FPS)


if __name__ == "__main__":
    main()
