# -*- coding: utf-8 -*-
# 负责初始化pyame
import pygame


def init():
    pygame.init()
    pygame.mixer.init()


def quit():
    pygame.quit()


init()

