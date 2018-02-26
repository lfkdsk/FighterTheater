from random import randint

from gameobjects.vector2 import Vector2

from settings import game_settings


class State(object):
    def __init__(self, name):
        self.name = name

    def do_actions(self):
        pass

    def check_conditions(self):
        pass

    def entry_actions(self):
        pass

    def exit_actions(self):
        pass


class StateMachine(object):
    def __init__(self):
        self.states = {}
        self.active_state = None

    def add_state(self, state):
        self.states[state.name] = state

    def think(self):
        if self.active_state is None:
            return
        self.active_state.do_actions()
        new_state_name = self.active_state.check_conditions()

        if new_state_name is not None:
            self.set_state(new_state_name)

    def set_state(self, new_state_name):
        if self.active_state is not None:
            self.active_state.exit_actions()

        self.active_state = self.states[new_state_name]
        self.active_state.entry_actions()


ANT_STATES = (
    'exploring',
    'leaf',
)


class HeroStateExploring(State):
    def __init__(self, hero):
        State.__init__(self, 'exploring')
        self.hero = hero

    def random_destination(self):
        w, h = game_settings.screen_size
        self.hero.destination = Vector2(randint(0, w), randint(0, h))

    def do_actions(self):
        if randint(1, 20) == 1:
            self.random_destination()

    def check_conditions(self):
        energy_store = self.hero.world.get_close_entity("energy", self.hero.location)
        if energy_store is not None:
            self.hero.energy_id = energy_store.id
            return "seeking"

        # spider = self.hero.world.get_close_entity("green-hero", NEST_POSITION, NEST_SIZE)
        # if spider is not None:
        #     if self.hero.location.get_distance_to(spider.location) < 100.:
        #         self.hero.spider_id = spider.id
        #         return "hunting"
        return None

    def entry_actions(self):
        self.hero.speed = 120. + randint(-30, 30)
        self.random_destination()
