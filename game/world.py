from random import randint

from gameobjects.vector2 import Vector2
from pytmx.util_pygame import load_pygame

from game_funcs import draw_background_with_tiled_map, initial_heroes, create_random_store
from settings import game_settings


class World(object):
    def __init__(self):
        self.entities = {}
        self.entity_id = 0
        self.energy_stores = {}
        self.game_map = load_pygame(game_settings.map_dir)
        # initial double-side heroes
        initial_heroes(self)
        # self.background.fill((255, 255, 255))
        # pygame.draw.circle(self.background, (200, 255, 200), NEST_POSITION, int(NEST_SIZE))

    def add_entity(self, entity):
        self.entities[self.entity_id] = entity
        entity.id = self.entity_id
        self.entity_id += 1

    def remove_entity(self, entity):
        del self.entities[entity.id]

    def get(self, entity_id):
        if entity_id in self.entities:
            return self.entities[entity_id]
        else:
            return None

    def random_emit(self):
        if randint(1, 20) == 10 and len(self.energy_stores) < 40:
            store = create_random_store(self)
            self.energy_stores[store.id] = store

    def process(self, time_passed):
        time_passed_seconds = time_passed / 1000.0
        for entity in self.entities.values():
            entity.process(time_passed_seconds)

    def render(self, surface):
        draw_background_with_tiled_map(surface, self.game_map)
        for entity in self.entities.values():
            entity.render(surface)

    def get_close_entity(self, name, location, range=100.):
        location = Vector2(*location)
        for entity in self.entities.values():
            if entity.name == name:
                distance = location.get_distance_to(entity.location)
                if distance < range:
                    return entity
        return None
