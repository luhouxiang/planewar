# -*- coding: utf-8 -*-

import pygame
import pygamepkg
import sys
from myplane import MyPlane
from enemy import Enemy
import enemy
from bullet import Bullet
from ground import Ground
from score import Score
from pygame.locals import QUIT


class MyGame:
    bg_size = Ground.get_bg_size()
    background = Ground.get_background()
    screen = Ground.get_screen()
    life_num = 2  # 我方飞机命的条数
    bullet_num = 32 # 我方飞机子弹数

    def __init__(self):
        pass

    @classmethod
    def start(cls):

        # 生成我方飞机
        me = MyPlane(cls.bg_size)
        # 生成敌机

        enemies = enemy.gen_enemies(cls.bg_size, 45)

        # 中弹图片索引
        MyPlane.me_destroy_index = 0
        Enemy.e1_destroy_index = 0

        life_num = MyPlane.life_num
        Score.reset()

        clock = pygame.time.Clock()

        # 用于替换图片
        switch_image = True

        # 用于延迟显示
        delay = 100

        running = True

        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

            cls.screen.blit(cls.background, (0, 0))

            if life_num:
                # 操作我的飞机
                MyPlane.operation(me)

                # 发射子弹
                Bullet.operation(delay, me, enemies)

                # 检测我方飞机是否被撞
                cls.check_plane_crash(enemies, me)

                # 绘制敌机
                Enemy.draw(delay, enemies)

                # 绘制我方飞机
                life_num = MyPlane.draw(delay, life_num, me, switch_image)

                # 绘制分数
                Score.draw_score()

            # 绘制游戏结束画面
            elif life_num <= 0:
                pygame.mixer.music.stop()
                pygame.mixer.stop()

                Score.draw_last()
                Score.deal_mouse()

            if not (delay % 5):
                switch_image = not switch_image

            delay -= 1

            if not delay:
                delay = 100

            pygame.display.flip()
            clock.tick(60)

    @classmethod
    def check_plane_crash(cls, enemies, me):
        enemies_down = pygame.sprite.spritecollide(me, enemies, False, pygame.sprite.collide_mask)
        if enemies_down:
            me.active = False
            for e in enemies_down:
                e.active = False







