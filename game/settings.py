import os


class Settings(object):

    def __init__(self):
        """initialize the settings of game."""

        # screen settings
        self.SCREEN_WIDTH = 960
        self.SCREEN_HEIGHT = 640
        self.SCREEN_SIZE = (self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
        self.BG_COLOR = (100, 100, 100)
        self.BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.MAP_DIR = os.path.join(self.BASE_DIR, "img/game.tmx")
        self.MAX_HEALTH = 25
        self.HEALTH_COLOR = (255, 0, 0)
        self.HEALTH_COVER_COLOR = (0, 255, 0)
        self.LEFT_HOME_LOCATION = (65, self.SCREEN_HEIGHT / 2)
        self.RIGHT_HOME_LOCATION = (self.SCREEN_WIDTH - 65, self.SCREEN_HEIGHT / 2)
        self.DEFAULT_HERO_NUM = 10
        self.DEFAULT_STORE_NUM = 10
        self.DEFAULT_SCORE = 5
        self.DEFAULT_SEARCH_RANGE = 100.0
        self.DROP_RANGE = 30.0
        self.MAX_ENTITIES = 20
        self.left_score = 0
        self.right_score = 0


game_settings = Settings()
