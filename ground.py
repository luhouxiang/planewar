# -*- coding: utf-8 -*-
import pygame


class Ground:
    bg_size = width, height = 400, 700
    screen = pygame.display.set_mode(bg_size)
    background = pygame.image.load("images/background.png").convert()
    pygame.display.set_caption("飞机大战")
    WHITE = (255, 255, 255)

    def __init__(self):
        pass

    @classmethod
    def get_bg_size(cls):
        return cls.bg_size

    @classmethod
    def get_background(cls):
        return cls.background

    @classmethod
    def get_screen(cls):
        return cls.screen



