# -*- coding: utf-8 -*-
# 计分体系
from ground import Ground
import sys
import pygame
import mygame


class Score:
    """
    计分类
    """
    num = 0  # 分数
    font = pygame.font.Font("font/font.ttf", 36)
    screen = Ground.get_screen()

    # 游戏结束画面
    gameover_font = pygame.font.Font("font/font.TTF", 48)
    again_image = pygame.image.load("images/again.png").convert_alpha()
    again_rect = again_image.get_rect()
    gameover_image = pygame.image.load("images/gameover.png").convert_alpha()
    gameover_rect = gameover_image.get_rect()

    def __init__(self):
        pass

    @classmethod
    def add(cls, num):
        cls.num += num

    @classmethod
    def reset(cls):
        cls.num = 0

    @classmethod
    def draw_score(cls):
        """
        绘制当前成绩
        :return:
        """
        text = cls.font.render("Score : %s" % str(cls.num), True, Ground.WHITE)
        cls.screen.blit(text, (10, 5))

    @classmethod
    def draw_last(cls):
        """
        绘制结束时的分数
        :return:
        """
        with open("record.txt", "r") as f:
            best_num = int(f.read())
        if cls.num > best_num:
            with open("record.txt", "w") as f:
                f.write(str(cls.num))

        best_text = cls.font.render("Best : %d" % best_num, True, (255, 255, 255))
        cls.screen.blit(best_text, (50, 50))

        gameover_text1 = cls.gameover_font.render("Your Score", True, (255, 255, 255))
        gameover_text1_rect = gameover_text1.get_rect()
        gameover_text1_rect.left = (Ground.width - gameover_text1_rect.width) // 2
        gameover_text1_rect.top = Ground.height // 3

        cls.screen.blit(gameover_text1, gameover_text1_rect)

        gameover_text2 = cls.gameover_font.render(str(cls.num), True, (255, 255, 255))
        gameover_text2_rect = gameover_text2.get_rect()
        gameover_text2_rect.left = (Ground.width - gameover_text2_rect.width) // 2
        gameover_text2_rect.top = gameover_text1_rect.bottom + 10
        cls.screen.blit(gameover_text2, gameover_text2_rect)

        cls.again_rect.left = (Ground.width - cls.again_rect.width) // 2
        cls.again_rect.top = gameover_text2_rect.bottom + 50
        cls.screen.blit(cls.again_image, cls.again_rect)

        cls.gameover_rect.left = (Ground.width - cls.again_rect.width) // 2
        cls.gameover_rect.top = cls.again_rect.bottom + 10
        cls.screen.blit(cls.gameover_image, cls.gameover_rect)

    @classmethod
    def deal_mouse(cls):
        # 检测用户的鼠标操作
        # 如果用户按下鼠标左键
        if pygame.mouse.get_pressed()[0]:
            # 获取鼠标坐标
            pos = pygame.mouse.get_pos()
            # 如果用户点击“重新开始”
            if cls.again_rect.left < pos[0] < cls.again_rect.right and \
                    cls.again_rect.top < pos[1] < cls.again_rect.bottom:
                # 调用main函数，重新开始游戏
                mygame.MyGame.start()
            # 如果用户点击“结束游戏”
            elif cls.gameover_rect.left < pos[0] < cls.gameover_rect.right and cls.gameover_rect.top < pos[
                1] < cls.gameover_rect.bottom:
                # 退出游戏
                pygame.quit()
                sys.exit()

