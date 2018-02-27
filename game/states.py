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

    def __unicode__(self):
        return self.name

    __str__ = __unicode__


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


HERO_STATES = (
    'exploring',
    'seeking',
    'fighting',
    'delivering'
)


class HeroStateExploring(State):
    def __init__(self, hero):
        State.__init__(self, HERO_STATES[0])
        self.hero = hero

    def random_destination(self):
        w, h = game_settings.SCREEN_SIZE
        self.hero.destination = Vector2(randint(60, w - 60), randint(60, h - 60))

    def do_actions(self):
        if randint(1, 20) == 1:
            self.random_destination()

    def check_conditions(self):
        location = self.hero.location
        world = self.hero.world

        enemy_type = self.hero.get_enemy_type()
        enemy = world.get_close_entity(
            enemy_type,
            location,
            game_settings.DEFAULT_SEARCH_RANGE,
        )

        # exploring --> fighting
        if enemy is not None and location.get_distance_to(enemy.location) < 100.:
            self.hero.enemy_id = enemy.id
            return HERO_STATES[2]

        energy_store = world.get_close_energy(self.hero.location)

        # exploring --> seeking
        if energy_store is not None:
            self.hero.energy_id = energy_store.id
            return HERO_STATES[1]

        return None

    def entry_actions(self):
        self.hero.speed = 120. + randint(-30, 30)
        self.random_destination()


class HeroStateSeeking(State):
    def __init__(self, hero):
        State.__init__(self, HERO_STATES[1])
        self.hero = hero
        self.energy_id = None

    def check_conditions(self):
        world = self.hero.world
        location = self.hero.location
        energy_store = world.get_energy_store(self.hero.energy_id)

        if energy_store is None:
            return HERO_STATES[0]

        if location.get_distance_to(energy_store.location) < 5.0:
            self.hero.carry(energy_store.image)
            self.hero.world.remove_energy_store(energy_store)
            return HERO_STATES[3]

        self.hero.destination = energy_store.location
        return None

    def entry_actions(self):
        energy_store = self.hero.world.get(self.hero.energy_id)
        if energy_store is not None:
            self.hero.destination = energy_store.location
            self.hero.speed = 160. + randint(-20, 20)


class HeroStateDelivering(State):
    def __init__(self, hero):
        State.__init__(self, HERO_STATES[3])
        self.hero = hero

    def check_conditions(self):
        location = self.hero.location
        world = self.hero.world
        home_location = Vector2(*self.hero.get_home_location())
        distance_to_home = home_location.get_distance_to(location)

        if distance_to_home < game_settings.DROP_RANGE or not self.hero.in_center():
            if randint(1, 10) == 1:
                self.hero.drop(world.background_layer)
                self.hero.add_energy_score()
                return HERO_STATES[0]

        return None

    def entry_actions(self):
        home_location = Vector2(*self.hero.get_home_location())
        self.hero.speed = 60.0
        random_offset = Vector2(randint(-20, 20), randint(-20, 20))
        self.hero.destination = home_location + random_offset


class HeroStateFighting(State):
    def __init__(self, hero):
        State.__init__(self, HERO_STATES[2])
        self.hero = hero
        self.got_kill = False

    def do_actions(self):
        world = self.hero.world
        enemy = world.get(self.hero.enemy_id)
        if enemy is None:
            return

        self.hero.destination = enemy.location
        offset = self.hero.location.get_distance_to(enemy.location) < 15.
        random_seed = randint(1, 5) == 1

        if offset and random_seed:
            enemy.bitten()
            if enemy.health <= 0:
                enemy.dead()
                world.remove_entity(enemy)
                self.got_kill = True

    def check_conditions(self):
        if self.got_kill:
            return HERO_STATES[3]

        enemy = self.hero.world.get(self.hero.enemy_id)

        if enemy is None:
            return HERO_STATES[0]

        if self.hero.health < 2 / 3 * game_settings.MAX_HEALTH:
            self.hero.destination = self.hero.get_home_location()
            return HERO_STATES[0]

        return None

    def entry_actions(self):
        self.speed = 160. + randint(0, 50)

    def exit_actions(self):
        self.got_kill = False
