import pygame
from pygame.sprite import Sprite
from conf import settings


class Bullet(Sprite):

    def __init__(self,ai_obj):

        super().__init__()
        self.screen = ai_obj.screen
        self.bullet_speed = settings.bullet_speed
        self.bullet_width = settings.bullet_width
        self.bullet_heiget = settings.bullet_height
        self.bullet_color = settings.bullet_color

        # 创建一个表示子弹的矩形并将其移动到正确位置
        self.rect = pygame.Rect(0,0,self.bullet_width,self.bullet_heiget)
        self.rect.midtop = ai_obj.ship.rect.midtop

        # 提升子弹位置精确度
        self.y = float(self.rect.y)

    def update(self): # 更新子弹位置

        self.y -= self.bullet_speed

        self.rect.y = self.y

    def draw_bullet(self):
        pygame.draw.rect(self.screen,self.bullet_color,self.rect)