import pygame
import neat
import time
import os
import random

WIN_WIDTH = 500
WIN_HEIGHT = 800

DINO_IMGS = [pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "Dino1.png")))
             , pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "Dino2.png")))
             , pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "Jump.png")))
             , pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "Crouch1.png")))
             , pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "Crouch2.png")))
             , pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "Dead.png")))]

BASE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "Base.png")))

CLOUD_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "Cloud.png")))

BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "BG.png")))

OBS_IMGS = [pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "Cacti1.png")))
            , pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "Cacti2.png")))
            , pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "Cacti3.png")))
            , pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "Cacti4.png")))
            , pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "Cacti5.png")))
            , pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "Cacti6.png")))
            , pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "Bird1.png")))
            , pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "Bird2.png")))]


class Dino:
    IMGS = DINO_IMGS
    ANIMATION_TIME = 5

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tick_count = 0
        self.vel = 0
        self.height = self.y
        self.img_count = 0
        self.img = self.IMGS[0]

    def jump(self):
        self.vel = -11
        self.tick_count = 0
        self.height = self.y

    def move(self):
        self.tick_count += 1

        d = self.vel * self.tick_count + 1.5 * self.tick_count ** 2

        self.y = self.y + d

    def draw(self, win):
        self.img_count += 1

        if self.img_count < self.ANIMATION_TIME:
            self.img = self.IMGS[0]
        elif self.img_count < self.ANIMATION_TIME*2:
            self.img = self.IMGS[1]
        elif self.img_count < self.ANIMATION_TIME*2+1:
            self.img = self.IMGS[0]
            self.img_count = 0

        rect = self.img.get_rect(center=self.img.get_rect(topleft=(self.x, self.y)).center)
        win.blit(self.img, rect.topleft)

    def get_mask(self):
        return pygame.mask.from_surface(self.img)


def draw_window(win, dino):
    win.blit(BG_IMG, (0, 0))

    dino.draw(win)

    pygame.display.update()


def main():
    dino = Dino(100, 100)
    clock = pygame.time.Clock()
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

    run = True
    while run:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()

        dino.move()

        draw_window(win, dino)


main()
