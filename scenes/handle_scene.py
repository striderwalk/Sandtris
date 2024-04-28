import pygame

from consts import BACKGROUND_COLOUR, FPS


def handle_scene(scene, win, clock):
    while True:
        # update the scene
        win.fill(BACKGROUND_COLOUR)
        if return_code := scene.update(win):
            return return_code

        for event in pygame.event.get():
            # Game exiting
            if event.type == pygame.QUIT:
                pygame.quit()
                return {"code": "quit"}

            elif event.type == pygame.KEYDOWN:
                # Game exiting
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    return {"code": "quit"}

            scene.handle_event(event)

        pygame.display.flip()
        pygame.display.set_caption(f"SandTris! fps:{clock.get_fps():.0f}")
        clock.tick(FPS)
