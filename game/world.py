from gameobjects.vector2 import Vector2
from pytmx.util_pygame import load_pygame

from game_funcs import draw_background_with_tiled_map, initial_heroes, create_random_heroes, create_random_stores, \
    render_score_message
from settings import game_settings


class World(object):
    def __init__(self, screen):
        self.entities = {}
        self.entity_id = 0
        self.energy_stores = {}
        self.game_map = load_pygame(game_settings.MAP_DIR)
        self.screen = screen
        self.background = screen.subsurface(
            (0, 0, game_settings.SCREEN_WIDTH, game_settings.SCREEN_HEIGHT),
        )
        self.hero_nums = {"green": 0, "red": 0}
        # initial double-side heroes
        initial_heroes(self)

    def add_entity(self, entity):
        self.entities[self.entity_id] = entity
        entity.id = self.entity_id
        self.entity_id += 1
        self.hero_nums[entity.hero_type] += 1

    def remove_entity(self, entity):
        self.hero_nums[entity.hero_type] -= 1
        del self.entities[entity.id]

    def get(self, entity_id):
        if entity_id in self.entities:
            return self.entities[entity_id]

        return None

    def random_emit(self):
        create_random_heroes(self)
        create_random_stores(self)

    def process(self, time_passed):
        time_passed_seconds = time_passed / 1000.0
        for entity in self.entities.values():
            entity.process(time_passed_seconds)

    def render(self, surface):
        draw_background_with_tiled_map(surface, self.game_map)
        render_score_message(surface)

        # render entities
        for entity in self.energy_stores.values():
            entity.render(surface)

        for entity in self.entities.values():
            entity.render(surface)

    def get_close_entity(self, name, location, search_range=100.0):
        location = Vector2(*location)
        for entity in self.entities.values():
            if entity.name == name:
                distance = location.get_distance_to(entity.location)
                if distance < search_range:
                    return entity

        return None

    def get_close_energy(self, location, search_range=100.0):
        location = Vector2(*location)
        for entity in self.energy_stores.values():
            distance = location.get_distance_to(entity.location)
            if distance < search_range:
                return entity

        return None

    def get_energy_store(self, energy_id):
        if energy_id in self.energy_stores.keys():
            return self.energy_stores[energy_id]

        return None

    def add_energy_store(self, store):
        self.energy_stores[self.entity_id] = store
        store.id = self.entity_id
        self.entity_id += 1

    def remove_energy_store(self, store):
        if store in self.energy_stores.values():
            del self.energy_stores[store.id]

    def min_hero_type(self):
        if self.hero_nums['red'] < self.hero_nums['green']:
            return 'red'

        return 'green'
