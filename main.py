import pygame

from consts import *
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
    exit_data = menu_loop(win, clock)
    if exit_data["code"] == "quit":
        pygame.quit()
        return
    while True:
        # loading screen
        exit_data = loading_loop(win, clock)
        if exit_data["code"] == "quit":
            pygame.quit()
            return

        # Run the main game loop
        exit_data = main_game_loop(win, clock)
        if exit_data["code"] == "quit":
            pygame.quit()
            return

        # # loading screen
        # exit_data = loading_loop(win, clock)
        # if exit_data["code"] == "quit":
        #     pygame.quit()
        #     return

        # Run the lost game loop
        score = exit_data["score"]
        game_screen = exit_data["screen"]
        exit_data = lost_loop(win, clock, score, game_screen)

        if exit_data["code"] == "quit":
            pygame.quit()
            return
        else:
            # loading screen
            exit_data = loading_loop(win, clock)
            if exit_data["code"] == "quit":
                pygame.quit()
                return
            add_scoreboard_loop(win, clock, score)

        # loading screen
        exit_data = loading_loop(win, clock)
        if exit_data["code"] == "quit":
            pygame.quit()
            return


if __name__ == "__main__":
    main()
