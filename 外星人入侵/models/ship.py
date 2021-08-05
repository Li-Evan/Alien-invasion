import pygame
from conf import settings
from models import bullet

class Ship:

    def __init__(self,ai_obj):

        # 初始化飞船并设置其初始位置
        self.screen = ai_obj.screen
        self.screen_rect = ai_obj.screen.get_rect()

        self.speed = settings.ship_speed
        # 加载飞船图像并获取其外接矩形
        self.image = pygame.image.load(settings.ship_picture_source)
        self.rect = self.image.get_rect() # 可以认为是获得了一个包裹着飞船图像的矩形，以后在处理的时候认为这个矩形就飞船

        # 对于每一艘飞船，都放在屏幕底部的中央
        self.rect.midbottom = self.screen_rect.midbottom # rect和screen_rect后面的参数midbottom可以换，设置飞船在屏幕的位置

        # 将飞船属性x储存小数值（rect只能存整数值）
        self.x = float(self.rect.x)

        # 移动标志
        self.moving_right = False
        self.moving_left = False



    # 用于响应飞船撞毁后出现新的飞船
    def set_new_ship(self):

        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)


    # 更新图像及刷新
    def update(self): # 如果移动标志为真就一直移动
        if self.moving_right and self.rect.right < self.screen_rect.right: # 移动且不超过屏幕
            self.x += self.speed # 以飞船移动速度为最小移动像素单位
        if self.moving_left and self.rect.left > self.screen_rect.left:
            self.x -= self.speed

        self.rect.x = self.x

    def blitme(self):

        self.screen.blit(self.image,self.rect) # 在指定位置放置飞船