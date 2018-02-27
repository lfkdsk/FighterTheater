import os
from random import randint

import psutil
import pygame
from gameobjects.vector2 import Vector2
import datetime
from settings import game_settings
from states import HERO_STATES


def draw_background_with_tiled_map(game_screen, game_map):
    # draw map data on screen
    for layer in game_map.visible_layers:
        for x, y, gid, in layer:
            tile = game_map.get_tile_image_by_gid(gid)
            if not tile:
                continue

            game_screen.blit(
                tile,
                (x * game_map.tilewidth,
                 y * game_map.tileheight)
            )


def load_alpha_image(resource_img):
    path = os.path.join(
        game_settings.BASE_DIR,
        'img/{}'.format(resource_img),
    )

    return pygame.image.load(path)


green_hero_img = load_alpha_image('green_hero.png')
red_hero_img = load_alpha_image('red_hero.png')
graves_img = load_alpha_image('graves.png')

HERO_TYPES = ('red', 'green')

green_energy_img = load_alpha_image('green_energy.png')
red_energy_img = load_alpha_image('red_energy.png')
ENERGY_IMAGES = {
    'green-store': green_energy_img,
    'red-store': red_energy_img,
}


def display_message(screen, text, size, color, rect):
    largeText = pygame.font.Font(None, size)
    TextSurf, TextRect = text_objects(text, largeText, color)
    TextRect.left = rect[0]
    TextRect.top = rect[1]
    screen.blit(TextSurf, TextRect)


def text_objects(text, font, color):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()


def get_left_random_location():
    x, y = game_settings.LEFT_HOME_LOCATION
    randX, randY = randint(x, x + 80), randint(80, game_settings.SCREEN_HEIGHT - 40)
    return Vector2(randX, randY)


def get_right_random_location():
    x, y = game_settings.RIGHT_HOME_LOCATION
    randX, randY = randint(x - 80, x), randint(80, game_settings.SCREEN_HEIGHT - 40)
    return Vector2(randX, randY)


def create_hero(world, hero_type):
    if hero_type == 'green':
        location = get_left_random_location()
        image = green_hero_img
        hero_name = 'green-hero'
    elif hero_type == 'red':
        location = get_right_random_location()
        image = red_hero_img
        hero_name = 'red-hero'
    else:
        raise KeyError("error type")

    from entities import Hero
    hero = Hero(world, image, graves_img, hero_type)
    hero.location = location
    hero.name = hero_name
    hero.brain.set_state(HERO_STATES[0])
    world.add_entity(hero)

    return hero


def create_random_store(world):
    rand_type = 0 if randint(0, 100) % 2 == 0 else 1
    energy_img, energy_type = ENERGY_IMAGES.values()[rand_type], ENERGY_IMAGES.keys()[rand_type]
    from entities import EnergyStore
    energy_store = EnergyStore(world, energy_img, energy_type)
    w, h = game_settings.SCREEN_SIZE
    energy_store.location = Vector2(randint(60, w - 60), randint(60, h - 60))
    world.add_energy_store(energy_store)

    return energy_store


def create_random_heroes(world):
    if randint(0, 100) == 80 and len(world.entities) < game_settings.MAX_ENTITIES:
        create_hero(world, HERO_TYPES[randint(0, 1)])
        create_hero(world, world.min_hero_type())


def create_random_stores(world):
    if randint(1, 20) == 10 and len(world.energy_stores) < 40:
        store = create_random_store(world)
        world.energy_stores[store.id] = store


def has_close_entities(world, item):
    entities = world.entities
    for entity in entities.values():
        item_location = entity.location
        if item.id != entity.id and item_location.get_distance_to(item.location) < 30:
            return True

    return False


def initial_heroes(world):
    green_hero_nums = game_settings.DEFAULT_HERO_NUM
    for _ in range(green_hero_nums):
        item = create_hero(world, 'green')
        while has_close_entities(world, item):
            item.location = get_left_random_location()

    red_hero_nums = game_settings.DEFAULT_HERO_NUM
    for _ in range(red_hero_nums):
        item = create_hero(world, 'red')
        while has_close_entities(world, item):
            item.location = get_right_random_location()

    store_nums = game_settings.DEFAULT_HERO_NUM
    for _ in range(store_nums):
        create_random_store(world)


start_time = datetime.datetime.now()


def render_score_message(surface):
    # render scores
    display_message(
        text='G:{}'.format(game_settings.left_score),
        color=(255, 255, 255),
        size=22,
        rect=(20, 20),
        screen=surface
    )

    display_message(
        text='R:{}'.format(game_settings.right_score),
        color=(255, 255, 255),
        size=22,
        rect=(20, 40),
        screen=surface
    )

    display_message(
        text='Memory: {}'.format(psutil.Process(os.getpid()).memory_info().rss),
        color=(255, 255, 255),
        size=22,
        rect=(20, 60),
        screen=surface
    )

    display_message(
        text='Time: {}'.format(datetime.datetime.now() - start_time),
        color=(255, 255, 255),
        size=22,
        rect=(20, 80),
        screen=surface
    )
