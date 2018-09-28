# -*- coding: utf-8 -*-

import pygame
import pygamepkg
import sys
from plane import Plane
from enemy import Enemy
import enemy
from bullet import Bullet
from ground import Ground
from score import Score
from pygame.locals import QUIT


class Game:
    bg_size = Ground.get_bg_size()
    background = Ground.get_background()
    screen = Ground.get_screen()
    delay = 100

    def __init__(self):
        pass

    @classmethod
    def start(cls):

        # 生成我方飞，敌机，完成准备工作
        clock, me, enemies = cls.ready()

        while True:
            # 接受系统消息，完成退出
            cls.response_system_request()

            # 绘制背景色
            cls.draw_background()

            if me.has_life():
                # 操作我的飞机
                Plane.operation(me)

                # 发射子弹
                Bullet.operation(cls.delay, me, enemies)

                # 检测我方飞机是否被撞
                Plane.check_plane_crash(me, enemies)

                # 绘制敌机
                Enemy.draw(cls.delay, enemies)

                # 绘制我方飞机
                Plane.draw(cls.delay, me)

                # 绘制分数
                Score.draw_score()

            # 处理结束状态
            else:
                cls.deal_end()

            # 系统默认处理
            cls.system_default_process(clock)

    @classmethod
    def ready(cls):
        clock = pygame.time.Clock()
        # 生成我方飞机
        me = Plane(cls.bg_size)
        # 生成敌机
        enemies = enemy.gen_enemies(cls.bg_size, 45)
        Score.reset()
        return clock, me, enemies

    @classmethod
    def draw_background(cls):
        cls.screen.blit(cls.background, (0, 0))

    @classmethod
    def system_default_process(cls, clock):
        cls.delay -= 1
        if not cls.delay:
            cls.delay = 100
        pygame.display.flip()
        clock.tick(60)

    @classmethod
    def response_system_request(cls):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

    @classmethod
    def deal_end(cls):
        pygame.mixer.music.stop()
        pygame.mixer.stop()
        Score.draw_last()
        Score.deal_mouse()

    @classmethod
    def dec_delay(cls, delay):
        delay -= 1
        if not delay:
            delay = 100
        return delay









