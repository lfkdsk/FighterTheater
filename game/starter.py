import pygame

from settings import game_settings
from world import World


def game_loop():
    game_exit = False

    pygame.init()
    pygame.display.set_caption('Python Game')
    game_screen = pygame.display.set_mode(
        (game_settings.SCREEN_WIDTH, game_settings.SCREEN_HEIGHT),
        pygame.DOUBLEBUF | pygame.HWSURFACE,
        32,
    )
    game_world = World(game_screen)
    clock = pygame.time.Clock()

    while not game_exit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_exit = True
        time_passed = clock.tick(30)

        game_world.random_emit()
        game_world.process(time_passed)
        game_world.render(game_screen)

        pygame.display.update()


