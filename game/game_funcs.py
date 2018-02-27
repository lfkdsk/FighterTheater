import os
from random import randint

import pygame
from gameobjects.vector2 import Vector2

from entities import EnergyStore
from game.entities import Hero
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
        game_settings.base_dir,
        'img/{}'.format(resource_img),
    )

    return pygame.image.load(path)


green_hero_img = load_alpha_image('green_hero.png')
red_hero_img = load_alpha_image('red_hero.png')

green_energy_img = load_alpha_image('green_energy.png')
red_energy_img = load_alpha_image('red_energy.png')
energy_imgs = {
    'green-store': green_energy_img,
    'red-store': red_energy_img,
}


def get_left_random_location():
    x, y = game_settings.left_home_location
    randX, randY = randint(x, x + 80), randint(80, game_settings.screen_height - 40)
    return Vector2(randX, randY)


def get_right_random_location():
    x, y = game_settings.right_home_location
    randX, randY = randint(x - 80, x), randint(80, game_settings.screen_height - 40)
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

    hero = Hero(world, image, None, hero_type)
    hero.location = location
    hero.name = hero_name
    hero.brain.set_state(HERO_STATES[0])
    world.add_entity(hero)

    return hero


def create_random_store(world):
    rand_type = 0 if randint(0, 100) % 2 == 0 else 1
    energy_img, energy_type = energy_imgs.values()[rand_type], energy_imgs.keys()[rand_type]
    energy_store = EnergyStore(world, energy_img, energy_type)
    w, h = game_settings.screen_size
    energy_store.location = Vector2(randint(60, w - 60), randint(60, h - 60))
    world.add_entity(energy_store)

    return energy_store


def has_close_entities(world, item):
    entities = world.entities
    for entity in entities.values():
        item_location = entity.location
        if item.id != entity.id and item_location.get_distance_to(item.location) < 30:
            return True

    return False


def initial_heroes(world):
    green_hero_nums = game_settings.default_hero_num
    for _ in range(green_hero_nums):
        item = create_hero(world, 'green')
        while has_close_entities(world, item):
            item.location = get_left_random_location()

    red_hero_nums = game_settings.default_hero_num
    for _ in range(red_hero_nums):
        item = create_hero(world, 'red')
        while has_close_entities(world, item):
            item.location = get_right_random_location()
