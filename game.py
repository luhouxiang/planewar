# -*- coding: utf-8 -*-

import pygame
import pygamepkg
import sys
from myplane import MyPlane
from enemy import Enemy
from bullet import Bullet
from ground import Ground

from pygame.locals import *


class Game:
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

        # 游戏结束画面
        gameover_font = pygame.font.Font("font/font.TTF", 48)
        again_image = pygame.image.load("images/again.png").convert_alpha()
        again_rect = again_image.get_rect()
        gameover_image = pygame.image.load("images/gameover.png").convert_alpha()
        gameover_rect = gameover_image.get_rect()

        # 生成普通子弹
        bullet_list = []
        for i in range(cls.bullet_num):
            bullet_list.append(Bullet(me.rect.midtop))

        # 统计得分
        score = 0
        score_font = pygame.font.Font("font/font.ttf", 36)

        clock = pygame.time.Clock()

        # 用于替换图片
        switch_image = True

        # 用于延迟显示
        delay = 100

        running = True

        paused = False

        # 用于限制重复打开记录文件
        recorded = False

        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

            cls.screen.blit(cls.background, (0, 0))

            if life_num and not paused:
                # 操作我的飞机
                cls.opt_plane(me)

                # 发射子弹
                cls.opt_bullet(bullet_list, delay, me, enemies)

                # 检测我方飞机是否被撞
                enemies_down = pygame.sprite.spritecollide(me, enemies, False, pygame.sprite.collide_mask)
                if enemies_down:
                    me.active = False
                    for e in enemies_down:
                        e.active = False

                # 绘制敌机
                score = cls.draw_enemies(delay, enemies, score)

                # 绘制我方飞机
                life_num = cls.draw_plane(delay, life_num, me, switch_image)

                score_text = score_font.render("Score : %s" % str(score), True, Ground.WHITE)
                cls.screen.blit(score_text, (10, 5))

            # 绘制游戏结束画面
            elif life_num <= 0:
                pygame.mixer.music.stop()
                pygame.mixer.stop()
                # 读取历史最高得分
                if not recorded:
                    recorded = True
                    with open("record.txt", "r") as f:
                        record_score = int(f.read())
                    if score > record_score:
                        with open("record.txt", "w") as f:
                            f.write(str(score))

                # 绘制结束界面
                record_score_text = score_font.render("Best : %d" % record_score, True, (255, 255, 255))
                cls.screen.blit(record_score_text, (50, 50))

                gameover_text1 = gameover_font.render("Your Score", True, (255, 255, 255))
                gameover_text1_rect = gameover_text1.get_rect()
                gameover_text1_rect.left, gameover_text1_rect.top = (Ground.width - gameover_text1_rect.width) // 2, Ground.height // 3
                cls.screen.blit(gameover_text1, gameover_text1_rect)

                gameover_text2 = gameover_font.render(str(score), True, (255, 255, 255))
                gameover_text2_rect = gameover_text2.get_rect()
                gameover_text2_rect.left, gameover_text2_rect.top = (Ground.width - gameover_text2_rect.width) // 2, gameover_text1_rect.bottom + 10
                cls.screen.blit(gameover_text2, gameover_text2_rect)

                again_rect.left, again_rect.top = (Ground.width - again_rect.width) // 2, gameover_text2_rect.bottom + 50
                cls.screen.blit(again_image, again_rect)

                gameover_rect.left, gameover_rect.top = (Ground.width - again_rect.width) // 2, again_rect.bottom + 10
                cls.screen.blit(gameover_image, gameover_rect)

                # 检测用户的鼠标操作
                # 如果用户按下鼠标左键
                if pygame.mouse.get_pressed()[0]:
                    # 获取鼠标坐标
                    pos = pygame.mouse.get_pos()
                    # 如果用户点击“重新开始”
                    if again_rect.left < pos[0] < again_rect.right and again_rect.top < pos[1] < again_rect.bottom:
                        # 调用main函数，重新开始游戏
                        Game.start()
                    # 如果用户点击“结束游戏”
                    elif gameover_rect.left < pos[0] < gameover_rect.right and gameover_rect.top < pos[
                        1] < gameover_rect.bottom:
                        # 退出游戏
                        pygamepkg.quit()
                        sys.exit()

            if not (delay % 5):
                switch_image = not switch_image

            delay -= 1

            if not delay:
                delay = 100

            pygame.display.flip()
            clock.tick(60)

    @classmethod
    def draw_plane(cls, delay, life_num, me, switch_image):
        destroy_image_size = len(me.destroy_images)
        if me.active:
            if switch_image:
                cls.screen.blit(me.image1, me.rect)
            else:
                cls.screen.blit(me.image2, me.rect)
        else:
            if not (delay % 3):
                if MyPlane.me_destroy_index == 0:
                    MyPlane.play_sound()
                cls.screen.blit(me.destroy_images[MyPlane.me_destroy_index], me.rect)
                MyPlane.me_destroy_index = (MyPlane.me_destroy_index + 1) % destroy_image_size
                if MyPlane.me_destroy_index == 0:
                    life_num -= 1
                    me.reset()
        return life_num

    @classmethod
    def draw_enemies(cls, delay, enemies, score):
        # 绘制敌机
        for each in enemies:
            if each.active:
                each.move()
                cls.screen.blit(each.image, each.rect)
            else:
                # 毁灭
                if not (delay % 3):
                    if Enemy.e1_destroy_index == 0:
                        Enemy.play_sound()
                    cls.screen.blit(each.destroy_images[Enemy.e1_destroy_index], each.rect)
                    Enemy.e1_destroy_index = (Enemy.e1_destroy_index + 1) % 4
                    if Enemy.e1_destroy_index == 0:
                        score += 1000
                        each.reset()
        return score

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

    @classmethod
    def opt_plane(cls, me):
        # 使用键盘操作我方飞机
        key_pressed = pygame.key.get_pressed()
        if key_pressed[K_UP]:
            me.move_up()
        if key_pressed[K_DOWN]:
            me.move_down()
        if key_pressed[K_LEFT]:
            me.move_left()
        if key_pressed[K_RIGHT]:
            me.move_right()



