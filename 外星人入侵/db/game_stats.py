import pygame
from conf import settings


class GameStats:

    def __init__(self,ai_obj):
        self.reset_stats()
        self.game_active = False
        self.stop_active = False
        self.highest_score = settings.highest_score

    def reset_stats(self):
        self.ship_left = settings.ship_limit
        self.score = 0
        self.level = 1
