import pygame

#  屏幕相关参数
# 屏幕展示模式一：展示一个1200*800的屏幕框
screen_width = 1200
screen_height = 800
screen = pygame.display.set_mode((screen_width,screen_height))

# 屏幕展示模式二：展示全屏
# screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)

bg_color = (230,230,230)
# fps = 60

# 关联资源相关参数
ship_picture_source = 'source/飞船.png'
alien_picture_source = 'source/外星人.png'
highest_score_source = 'source/highest_score.txt'
bg_picture_source = 'source/背景备选/1.jpg'
bg_music_source = 'source/AgNo3 - Fragmentary（背景音乐）.mp3'
boom_music_source = 'source/爆炸声.mp3'
bullet_music_source = 'source/子弹发射声.mp3'
stop_icon_source = 'source/暂停.png'


# 音乐与音效相关
bg_music_volume = 0.2
boom_music_volume = 0.2
bullet_music_volume = 0.2




# 飞船相关参数
ship_speed = 1.5
ship_limit = 1 # 有几条命

# 子弹相关参数
bullet_speed = 1.0
bullet_width = 3
bullet_height = 15
bullet_color = (60,60,60)
bullet_allow = 16

# 外星人相关参数
alien_speed = 1.0
fleet_drop_speed = 10
fleet_direction = 1
alien_point = 50

# 按钮相关参数
button_width = 200
button_height = 50
button_color = (252, 250, 237)
text_color = (7, 7, 99)
button_font_style = None
button_font_size = 48

# 游戏节奏相关参数
speed_up_scale = 1.1

# 得分显示相关参数
score_color = (30,30,30)
score_font_style = None
score_font_size = 48

# 历史最高分相关参数
with open(highest_score_source,'rt') as f:
    score = f.read()
    if score != '':
        highest_score = int(eval(score))
    else:
        highest_score = 0