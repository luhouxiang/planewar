# -*- coding: utf-8 -*-
import pygame


class Bullet(pygame.sprite.Sprite):
    sound = pygame.mixer.Sound("sound/bullet.wav")
    sound.set_volume(0.2)

    def __init__(self, position):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load("images/bullet1.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = position
        self.speed = 12
        self.active = False
        self.mask = pygame.mask.from_surface(self.image)

    def move(self):
        self.rect.top -= self.speed

        if self.rect.top < 0:
            self.active = False

    def reset(self, position):
        self.rect.left, self.rect.top = position
        self.active = True

    @classmethod
    def get_sound(cls):
        return cls.sound

    @classmethod
    def play_sound(cls):
        cls.sound.play()

