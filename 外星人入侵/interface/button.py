import pygame.font
from conf import settings


class Button:

    def __init__(self,ai_obj,msg='PLAY'):
        # 初始化屏幕
        self.screen = ai_obj.screen
        self.screen_rect = self.screen.get_rect()

        # 设置按钮及文本相关参数
        self.width = settings.button_width
        self.height = settings.button_height

        self.button_color = settings.button_color
        self.text_color = settings.text_color

        self.font = pygame.font.SysFont(settings.button_font_style,settings.button_font_size)

        # 创建按钮对象并使之居中
        self.button_rect = pygame.Rect(0,0,self.width,self.height)
        self.button_rect.center = self.screen_rect.center

        # 创建按钮上面的文本
        self._make_msg(msg)

        # 加载暂停图标并获取其外接矩形
        self.stop_image = pygame.image.load(settings.stop_icon_source)
        self.stop_rect = self.stop_image.get_rect()

        self.stop_rect.center = self.screen_rect.center


    def _make_msg(self,msg):
        # 渲染文本为图像并使之居中
        self.msg_image = self.font.render(msg,True,self.text_color,self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.button_rect.center

    # 将按钮显示到屏幕上
    def show_button(self):
        self.screen.fill(self.button_color,self.button_rect)
        self.screen.blit(self.msg_image,self.msg_image_rect)

    # 将暂停图标显示到屏幕上
    def show_stop_icon(self):
        self.screen.blit(self.stop_image,self.stop_rect)
