import pygame

from entities import Hero
from game.game_funcs import load_alpha_image, initial_heroes
from settings import game_settings
from world import World


def game_loop():
    game_exit = False

    pygame.init()
    pygame.display.set_caption('Python Game')
    game_screen = pygame.display.set_mode(
        (game_settings.screen_width, game_settings.screen_height),
        pygame.DOUBLEBUF | pygame.HWSURFACE,
        32,
    )
    game_world = World()

    clock = pygame.time.Clock()
    initial_heroes(game_world)
    while not game_exit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_exit = True
        time_passed = clock.tick(30)

        # draw background
        game_world.process(time_passed)
        game_world.render(game_screen)

        pygame.display.update()


if __name__ == '__main__':
    game_loop()
    pygame.quit()
