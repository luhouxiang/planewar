# -*- coding: utf-8 -*-

import pygame
import pygamepkg
import sys
from myplane import MyPlane
from enemy import Enemy
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
    def add_enemies(cls, enemy_list, num):
        for i in range(num):
            e1 = Enemy(cls.bg_size)
            enemy_list.add(e1)

    @classmethod
    def start(cls):
        life_num = cls.life_num
        # 生成我方飞机
        me = MyPlane(cls.bg_size)

        # 中弹图片索引

        MyPlane.me_destroy_index = 0
        Enemy.e1_destroy_index = 0

        enemies = pygame.sprite.Group()
        # 生成敌机
        cls.add_enemies(enemies, 45)

        # 生成普通子弹
        bullet_list = []
        for i in range(cls.bullet_num):
            bullet_list.append(Bullet(me.rect.midtop))

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
                cls.opt_bullet(bullet_list, delay, me, enemies)

                # 检测我方飞机是否被撞
                enemies_down = pygame.sprite.spritecollide(me, enemies, False, pygame.sprite.collide_mask)
                if enemies_down:
                    me.active = False
                    for e in enemies_down:
                        e.active = False

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
    def opt_bullet(cls, bullets, delay, me, enemies):
        """
        打子弹
        :param bullets:
        :param delay:
        :param me:
        :param enemies:
        :return:
        """
        bullet_size = len(bullets)
        if not (delay % 10):
            Bullet.play_sound()
            bullets[Bullet.bullet1_index].reset(me.rect.midtop)
            Bullet.bullet1_index = (Bullet.bullet1_index + 1) % bullet_size

        for b in bullets:
            if b.active:
                b.move()
                cls.screen.blit(b.image, b.rect)
                enemy_hit = pygame.sprite.spritecollide(b, enemies, False, pygame.sprite.collide_mask)
                if enemy_hit:
                    b.active = False
                    for e in enemy_hit:
                        e.active = False





