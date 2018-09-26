# -*- coding: utf-8 -*-

import pygame
import pygamepkg
import sys
import myplane
import enemy
import bullet
from ground import Ground

from pygame.locals import *


class Game:
    bg_size = Ground.get_bg_size()
    background = Ground.get_background()
    screen = Ground.get_screen()
    life_num = 2

    def __init__(self):
        pass

    @classmethod
    def add_small_enemies(cls, group1, group2, num):
        for i in range(num):
            e1 = enemy.Enemy(cls.bg_size)
            group1.add(e1)
            group2.add(e1)

    @classmethod
    def start(cls):
        cls.life_num = 2
        # 生成我方飞机
        me = myplane.MyPlane(cls.bg_size)

        # 中弹图片索引
        e1_destroy_index = 0
        me_destroy_index = 0

        enemies = pygame.sprite.Group()
        # 生成敌方小型飞机
        small_enemies = pygame.sprite.Group()
        cls.add_small_enemies(small_enemies, enemies, 15)

        # 游戏结束画面
        gameover_font = pygame.font.Font("font/font.TTF", 48)
        again_image = pygame.image.load("images/again.png").convert_alpha()
        again_rect = again_image.get_rect()
        gameover_image = pygame.image.load("images/gameover.png").convert_alpha()
        gameover_rect = gameover_image.get_rect()

        # 生成普通子弹
        bullet1 = []
        bullet1_index = 0
        BULLET1_NUM = 4
        for i in range(BULLET1_NUM):
            bullet1.append(bullet.Bullet(me.rect.midtop))

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

            if cls.life_num and not paused:
                # 操作我的飞机
                cls.opt_myplane(me)

                # 发射子弹
                if not (delay % 10):
                    bullet.Bullet.play_sound()
                    bullets = bullet1
                    bullets[bullet1_index].reset(me.rect.midtop)
                    bullet1_index = (bullet1_index + 1) % BULLET1_NUM

                for b in bullets:
                    if b.active:
                        b.move()
                        cls.screen.blit(b.image, b.rect)
                        enemy_hit = pygame.sprite.spritecollide(b, enemies, False, pygame.sprite.collide_mask)
                        if enemy_hit:
                            b.active = False
                            for e in enemy_hit:
                                e.active = False

                # 检测我方飞机是否被撞
                enemies_down = pygame.sprite.spritecollide(me, enemies, False, pygame.sprite.collide_mask)
                if enemies_down:
                    me.active = False
                    for e in enemies_down:
                        e.active = False

                # 绘制小型敌机
                for each in small_enemies:
                    if each.active:
                        each.move()
                        cls.screen.blit(each.image, each.rect)
                    else:
                        # 毁灭
                        if not (delay % 3):
                            if e1_destroy_index == 0:
                                enemy.Enemy.play_sound()
                            cls.screen.blit(each.destroy_images[e1_destroy_index], each.rect)
                            e1_destroy_index = (e1_destroy_index + 1) % 4
                            if e1_destroy_index == 0:
                                score += 1000
                                each.reset()

                # 绘制我方飞机
                if me.active:
                    if switch_image:
                        cls.screen.blit(me.image1, me.rect)
                    else:
                        cls.screen.blit(me.image2, me.rect)
                else:
                    if not (delay % 3):
                        if me_destroy_index == 0:
                            myplane.MyPlane.play_sound()
                        cls.screen.blit(me.destroy_images[me_destroy_index], me.rect)
                        me_destroy_index = (me_destroy_index + 1) % 4
                        if me_destroy_index == 0:
                            cls.life_num -= 1
                            me.reset()
                score_text = score_font.render("Score : %s" % str(score), True, Ground.WHITE)
                cls.screen.blit(score_text, (10, 5))

            # 绘制游戏结束画面
            elif cls.life_num <= 0:
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
                        # pygame.quit()
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
    def opt_myplane(cls, me):
        # 检测用户的键盘操作
        key_pressed = pygame.key.get_pressed()
        if key_pressed[K_UP]:
            me.move_up()
        if key_pressed[K_DOWN]:
            me.move_down()
        if key_pressed[K_LEFT]:
            me.move_left()
        if key_pressed[K_RIGHT]:
            me.move_right()



