import sys
from conf import settings
import pygame
from models import ship,bullet,alien
import random
import time
from db import game_stats,scoreboard
from interface import button

class AlienInvasion:
    '''
    管理游戏资源和行为的类
    '''

    def __init__(self):
        # 基本项目配置
        pygame.init()

        self.screen = settings.screen
        self.bg_color = settings.bg_color

        pygame.display.set_caption('外星人入侵')  # 左上角显示的文字

        self.fclock = pygame.time.Clock()

        # 音乐及音效配置
        pygame.mixer.music.load(settings.bg_music_source)
        pygame.mixer.music.set_volume(settings.bg_music_volume)

        self.boom_sound = pygame.mixer.Sound(settings.boom_music_source)
        self.boom_sound.set_volume(settings.boom_music_volume)
        self.bullet_sound = pygame.mixer.Sound(settings.bullet_music_source)
        self.bullet_sound.set_volume(settings.bullet_music_volume)

        # 初始化数据登记信息
        self.stats = game_stats.GameStats(self)
        self.scoreboard = scoreboard.ScoreBoard(self)

        # 初始化飞船，子弹，外星人并创造飞船
        self.ship = ship.Ship(self)
        self.bullets = pygame.sprite.Group()  # 可以自动帮我们管理所有子弹
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

        # 创建按钮
        self.button = button.Button(self)

        # # 设置背景图片
        # self.bg_picture = pygame.image.load(settings.bg_picture_source)

        pygame.mixer.music.play(-1)


    '''与监听相关方法'''
    def _check_events(self): # 事件监听循环

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                self.save_highest_score()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_events_keydown(event)
            elif event.type == pygame.KEYUP:
                self._check_events_keyup(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self._check_events_mousebuttondown(event)

    def _check_events_keydown(self,event):
        '''响应方向键按下'''
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_a:
            self._fire_bullet()
        elif event.key == pygame.K_p:
            self._play_game()
        elif event.key == pygame.K_s:
            self.stats.stop_active = not self.stats.stop_active
            # self.button.show_stop_icon()
            # self._update_screen()


    def _check_events_keyup(self,event):
        '''响应方向键松开'''
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False


    def _check_events_mousebuttondown(self,event):
        mouse_pos = pygame.mouse.get_pos()
        if self.button.button_rect.collidepoint(mouse_pos) and self.stats.game_active == False: # 如果鼠标点击了play按钮且游戏未开始
            self._play_game()


    '''与子弹相关方法'''
    # 开火
    def _fire_bullet(self):
        if self.stats.game_active:
            if len(self.bullets) < settings.bullet_allow:
                new_bullet = bullet.Bullet(self)
                self.bullets.add(new_bullet)
                self.bullet_sound.play()
    # # 持续射击
    # def continue_fire(self):
    #
    #             self._fire_bullet()
    #             time.sleep(0.1)


    '''与外星人相关方法'''
    # 用于创建一行外星人
    def _create_fleet(self):

        # 创建一个外星人实例，用于计算一行一共放多少个,一共放多少列外星人，该外星人实例不进入编组
        alien0 = alien.Alien(self)
        alien0_width,alien0_height = alien0.rect.size

        # 计算一行几个
        available_space_x = settings.screen_width - 2 * alien0_width
        number_aliens = available_space_x // (2 * alien0_width) # 每两个外星人之间的间隔是一个外星人（2-1）的宽度，可以调整

        # 计算几行
        available_space_y = settings.screen_height - 2 * alien0_height - self.ship.rect.height
        number_rows = available_space_y // (2 * alien0_height)

        # 根据计算得到的外星人数量进行外星人实例创建
        for row_number in range(number_rows):
            for alien_number in range(number_aliens):
                self._create_alien(alien_number,row_number)

    # 用于创建单个外星人
    def _create_alien(self,alien_number,row_number):

        # 计算第alien_number[每行第几个],row_number[第几行]个外星人的位置并加入编组
        alien_i = alien.Alien(self)
        alien_i_width,alien_i_height = alien_i.rect.size

        alien_i.x = alien_i_width + 2 * alien_i_width * alien_number
        alien_i.rect.x = alien_i.x
        alien_i.y = alien_i_height + 2 * alien_i_height * row_number
        alien_i.rect.y = alien_i.y

        # 随机生成外星人
        # check = random.randint(0,1)
        # if check:
        #     self.aliens.add(alien_i)
        self.aliens.add(alien_i)



    '''检测 及 检测相关响应 相关方法'''
    # 检查外星人是否撞到了边缘
    def _check_fleet_edge(self):

        for alien_i in self.aliens.sprites():
            if alien_i.check_edge():
                self._change_fleet_direction()
                break


    # 检查外星人是否到达底部
    def _check_fleet_bottom(self):

        for alien_i in self.aliens.sprites():
            if alien_i.check_bottom():
                return True

    # 检测外星人和子弹是否发生碰撞并响应
    def _check_aliens_and_bullets_collision(self):

        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens,False, True) # 得到groupcollide返回的crashed字典

        self._result_collide(collisions)

        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()
            self.increse_speed()
            self.stats.level += 1
            self.scoreboard.make_level()



    '''响应相关方法'''
    # 下坠并改变左右移动的方向(响应撞到了边缘)
    def _change_fleet_direction(self):

        for alien_i in self.aliens.sprites():
            alien_i.rect.y += alien_i.fleet_drop_speed

        settings.fleet_direction *= -1

    # 响应外星人和飞船发生碰撞
    def _result_alien_collide_ship(self):

        # 看看还有没有生命
        if self.stats.ship_left > 1:
            self.stats.ship_left -= 1

            self.aliens.empty()
            self.bullets.empty()

            self._create_fleet()
            self.ship.set_new_ship()

            time.sleep(0.5)
        else:
            self.stats.game_active = False

    # 响应鼠标点击play事件
    def _play_game(self):

        # 重置相关设置信息
        settings.alien_speed = 1.0
        settings.ship_speed = 1.5
        settings.bullet_speed = 1.0

        # 重置数据信息
        self.stats.reset_stats()
        self.stats.game_active = True
        self.scoreboard.make_score()
        self.scoreboard.make_level()

        # 清空外星人和子弹
        self.aliens.empty()
        self.bullets.empty()

        # 加载外星人和初始化飞船位置，游戏重新开始
        self._create_fleet()
        self.ship.set_new_ship()

    # 关闭时保存最高分
    def save_highest_score(self):
        with open(settings.highest_score_source,'wt') as f:
            f.write(str(self.stats.highest_score))

    # 响应碰撞相关方法
    def _result_collide(self,collisions):

        # 加分
        if collisions:
            for aliens in collisions.values():
                self.stats.score += settings.alien_point * len(aliens)
            self.scoreboard.make_score()

            # # 爆炸音效
            self.boom_sound.play()




    '''游戏升级相关方法'''
    def increse_speed(self):
        self.ship.speed *= settings.speed_up_scale
        settings.alien_speed *= settings.speed_up_scale
        settings.bullet_speed *= settings.speed_up_scale
        settings.alien_point *= settings.speed_up_scale



    '''与屏幕更新主循环相关方法'''
    def _update_bullets(self):
        # self.fire()

        self.bullets.update()  # 更新子弹编组内所有子弹位置
        # 删除消失的子弹
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        # print(len(self.bullets))

        # 更新完子弹的位置立刻检测子弹和外星人之间的碰撞
        self._check_aliens_and_bullets_collision()

    def _update_aliens(self):

        self._check_fleet_edge() # 检查是否触碰边缘
        self.aliens.update() # 更新外星人编组内所有外星人位置

        if pygame.sprite.spritecollideany(self.ship,self.aliens) or self._check_fleet_bottom(): # 飞船和外星人相撞或外星人到达底部
            # print('shit!!!')
            self._result_alien_collide_ship()

    def _update_screen(self): # 屏幕刷新循环

        # 每次循环都重新绘制屏幕
        self.screen.fill(self.bg_color)

        # # 刷新背景图片
        # self.screen.blit(self.bg_picture,(0,0))

        if self.stats.stop_active:
            self.button.show_stop_icon()

        # 刷新飞船，子弹，外星人
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)

        # 展示当前分数，当前等级，历史最高分
        self.scoreboard.show_score()
        self.scoreboard.check_high_score()

        # 如果没有开始游戏则展示“play”按钮
        if self.stats.game_active == False:
            self.button.show_button()

        # 控制屏幕刷新帧率
        # self.fclock.tick(settings.fps)

        # 让最近刷新的屏幕可见
        pygame.display.flip()

    def run(self):

        while True:

            self._check_events() # 事件监听循环
            if self.stats.game_active is True and self.stats.stop_active is False:
                self.ship.update() # 飞船刷新
                self._update_bullets() # 子弹刷新
                self._update_aliens() # 外星人刷新
            self._update_screen() # 屏幕刷新循环


