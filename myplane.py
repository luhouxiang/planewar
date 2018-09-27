# -*- coding: utf-8 -*-
import pygame
from ground import Ground
from pygame.locals import K_UP, K_DOWN, K_LEFT, K_RIGHT


class MyPlane(pygame.sprite.Sprite):
    sound = pygame.mixer.Sound("sound/me_down.wav")
    sound.set_volume(0.4)
    me_destroy_index = 0
    screen = Ground.get_screen()

    def __init__(self, bg_size):
        pygame.sprite.Sprite.__init__(self)

        self.image1 = pygame.image.load("images/me1.png").convert_alpha()
        self.image2 = pygame.image.load("images/me2.png").convert_alpha()
        self.destroy_images = []
        self.active = True
        self.destroy_images.extend([
            pygame.image.load("images/me_destroy_1.png").convert_alpha(),
            pygame.image.load("images/me_destroy_2.png").convert_alpha(),
            pygame.image.load("images/me_destroy_3.png").convert_alpha(),
            pygame.image.load("images/me_destroy_4.png").convert_alpha()
        ])

        self.rect = self.image1.get_rect()
        self.width, self.height = bg_size[0], bg_size[1]
        self.rect.left, self.rect.top = \
            (self.width - self.rect.width) // 2, self.height - self.rect.height - 60
        self.speed = 10
        self.invincible = False
        self.mask = pygame.mask.from_surface(self.image1)

    def move_up(self):
        if self.rect.top > 0:
            self.rect.top -= self.speed
        else:
            self.rect.top = 0

    def move_down(self):
        if self.rect.bottom < self.height - 60:
            self.rect.top += self.speed
        else:
            self.rect.bottom = self.height - 60

    def move_left(self):
        if self.rect.left > 0:
            self.rect.left -= self.speed
        else:
            self.rect.left = 0

    def move_right(self):
        if self.rect.right < self.width:
            self.rect.left += self.speed
        else:
            self.rect.right = self.width

    def reset(self):
        self.rect.left, self.rect.top = \
            (self.width - self.rect.width) // 2, self.height - self.rect.height - 60
        self.active = True
        self.invincible = True

    @classmethod
    def get_sound(cls):
        return cls.sound

    @classmethod
    def play_sound(cls):
        cls.sound.play()

    @classmethod
    def draw(cls, delay, life_num, me, switch_image):
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
    def operation(cls, me):
        """
        使用键盘操作我方飞机
        :param me: 我方飞机的实例
        :return:
        """
        key_pressed = pygame.key.get_pressed()
        if key_pressed[K_UP]:
            me.move_up()
        if key_pressed[K_DOWN]:
            me.move_down()
        if key_pressed[K_LEFT]:
            me.move_left()
        if key_pressed[K_RIGHT]:
            me.move_right()




