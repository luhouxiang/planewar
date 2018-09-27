# -*- coding: utf-8 -*-

import pygame
from ground import Ground


class Bullet(pygame.sprite.Sprite):
    """
    子弹类
    """
    num = 4
    sound = pygame.mixer.Sound("sound/bullet.wav")
    sound.set_volume(0.2)
    bullet1_index = 0
    screen = Ground.get_screen()

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

    @classmethod
    def operation(cls, delay, me, enemies):
        """
        打子弹
        :param bullets:
        :param delay:
        :param me:
        :param enemies:
        :return:
        """
        bullets = me.bullet_list
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

