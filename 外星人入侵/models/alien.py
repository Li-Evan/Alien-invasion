import pygame
from pygame.sprite import Sprite
from conf import settings

class Alien(Sprite):

    def __init__(self, ai_obj):
        super().__init__()
        self.screen = ai_obj.screen

        self.image = pygame.image.load(settings.alien_picture_source)
        self.rect = self.image.get_rect()

        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        self.x = float(self.rect.x)

        self.speed = settings.alien_speed
        self.fleet_drop_speed = settings.fleet_drop_speed

    def check_edge(self):
        # 检查是否撞到了边缘
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= screen_rect.left:
            return True

    def check_bottom(self):
        # 检查是否撞到底部
        srceen_rect = self.screen.get_rect()
        if self.rect.bottom >= srceen_rect.bottom + 100:
            return True

    def update(self):

        # 向左或右移动外星人
        self.x += self.speed * settings.fleet_direction
        self.rect.x = self.x