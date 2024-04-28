import pygame

from consts import WIDTH, HEIGHT
import utils
from scenes import *

large_font = utils.get_font(38)
underline_large_font = utils.get_font(38)
underline_large_font.set_underline(True)

small_font = utils.get_font(20)


def main():

    # setup pygame
    pygame.init()
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    # Start menu

    return_code = handle_scene(Menu(), win, clock)
    if return_code["code"] == "quit":
        pygame.quit()
        return

    while True:
        # loading screen
        return_code = handle_scene(Loading(), win, clock)
        if return_code["code"] == "quit":
            pygame.quit()
            return

        # Run the main game loop
        return_code = handle_scene(Game(), win, clock)
        if return_code["code"] == "quit":
            pygame.quit()
            return

        # Run the lost game loop
        score = return_code["score"]
        game_screen = return_code["screen"]
        return_code = handle_scene(Lost(game_screen, score), win, clock)

        if return_code["code"] == "quit":
            pygame.quit()
            return

        return_code = handle_scene(Scoreboard(score), win, clock)
        if return_code["code"] == "quit":
            pygame.quit()
            return


if __name__ == "__main__":
    main()
