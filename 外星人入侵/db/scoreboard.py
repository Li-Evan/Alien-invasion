import pygame
from db import game_stats
from conf import settings


class ScoreBoard:

    def __init__(self,ai_obj):
        # 初始化参数
        self.screen = ai_obj.screen
        self.screen_rect = self.screen.get_rect()
        self.stats = ai_obj.stats

        # 设置字体及颜色参数
        self.font = pygame.font.SysFont(settings.score_font_style, settings.score_font_size)
        self.color = settings.score_color

        # 渲染分数
        self.make_score()
        self.make_highest_score()
        self.make_level()

    def make_score(self):
        # 将分数转化为字符串并进行渲染
        rounded_score = round(self.stats.score,-1)
        rounded_score = int(rounded_score)
        rounded_score_str = '{:,}'.format(rounded_score)

        self.score_image = self.font.render(rounded_score_str,True,self.color,settings.bg_color)
        self.score_image_rect = self.score_image.get_rect()

        # 设置得分板显示位置
        self.score_image_rect.right = self.screen_rect.right - 20
        self.score_image_rect.top = 20

    def make_highest_score(self):
        # 将最高分转化为字符串并进行渲染

        rounded_highest_score = round(self.stats.highest_score,-1)
        rounded_highest_score = int(rounded_highest_score)
        rounded_highest_score_str = '{:,}'.format(rounded_highest_score)

        self.highest_score_image = self.font.render(rounded_highest_score_str,True,self.color,settings.bg_color)
        self.highest_score_image_rect = self.highest_score_image.get_rect()

        # 设置最高分显示位置
        self.highest_score_image_rect.centerx = self.screen_rect.centerx # 水平居中
        self.highest_score_image_rect.top = self.score_image_rect.top # 跟得分板一样高

    def check_high_score(self):
        if self.stats.score > self.stats.highest_score:
            self.stats.highest_score = self.stats.score
            self.make_highest_score()

    def make_level(self):
        # 将等级转化为字符串并进行渲染

        rounded_level_str = f'level:{self.stats.level}'

        self.level_image = self.font.render(rounded_level_str,True,self.color,settings.bg_color)
        self.level_image_rect = self.level_image.get_rect()

        # 设置等级显示位置
        self.level_image_rect.right = self.score_image_rect.right
        self.level_image_rect.top = self.score_image_rect.bottom + 20

    def show_score(self):
        self.screen.blit(self.score_image,self.score_image_rect)
        self.screen.blit(self.highest_score_image, self.highest_score_image_rect)
        self.screen.blit(self.level_image,self.level_image_rect)


