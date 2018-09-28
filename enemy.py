import pygame
from random import *
from score import Score
from ground import Ground


def gen_enemies(bg_size, num):
    Enemy.e1_destroy_index = 0
    enemies = pygame.sprite.Group()
    for i in range(num):
        e1 = Enemy(bg_size)
        enemies.add(e1)
    return enemies


class Enemy(pygame.sprite.Sprite):
    """
    敌机
    """
    sound = pygame.mixer.Sound("sound/enemy1_down.wav")
    sound.set_volume(0.3)
    e1_destroy_index = 0
    screen = Ground.get_screen()

    def __init__(self, bg_size):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load("images/enemy1.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.destroy_images = []
        self.destroy_images.extend([
            pygame.image.load("images/enemy1_down1.png").convert_alpha(),
            pygame.image.load("images/enemy1_down2.png").convert_alpha(),
            pygame.image.load("images/enemy1_down3.png").convert_alpha(),
            pygame.image.load("images/enemy1_down4.png").convert_alpha()
        ])

        self.width, self.height = bg_size[0], bg_size[1]
        self.speed = 3
        self.active = True
        self.rect.left, self.rect.top = \
            randint(0, self.width - self.rect.width), randint((-5)*self.height, 0)
        self.mask = pygame.mask.from_surface(self.image)

    def move(self):
        if self.rect.top < self.height:
            self.rect.top += self.speed
        else:
            self.reset()

    def reset(self):
        self.active = True
        self.rect.left, self.rect.top = \
            randint(0, self.width - self.rect.width), randint((-5)*self.height, 0)

    @classmethod
    def get_sound(cls):
        return cls.sound

    @classmethod
    def play_sound(cls):
        cls.sound.play()

    @classmethod
    def draw(cls, delay, enemies):

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
                        Score.add(1000)
                        each.reset()