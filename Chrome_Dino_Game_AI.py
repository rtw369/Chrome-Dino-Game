import pygame
import neat
import time
import os
import random

WIN_WIDTH = 1000
WIN_HEIGHT = 800

pygame.font.init()
STAT_FONT = pygame.font.SysFont("comicsans", 50)

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
        if self.y >= 500 - self.img.get_height() + 15:
            self.vel = -12
            self.tick_count = 0
        self.height = self.y

    def move(self):
        self.tick_count += 1

        d = self.vel * self.tick_count + 1.5 * self.tick_count ** 2

        # makes the dino fall slower.
        if d >= 12:
            d = 12

        if d < 0:
            d -= 2

        if d > 0 and self.y >= 500 - self.img.get_height() + 15:
            self.vel = 0
            d = 0

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

        if self.y < 500 - self.img.get_height() + 15:
            self.img = self.IMGS[2]

        win.blit(self.img, (self.x, self.y))

    def get_mask(self):
        return pygame.mask.from_surface(self.img)


class Base:
    MAX_VEL = 30
    WIDTH = BASE_IMG.get_width()
    IMG = BASE_IMG

    def __init__(self, y):
        self.y = y
        self.vel = 0
        self.tick_count = 0
        self.x1 = 0
        self.x2 = self.WIDTH

    def move(self, score):
        self.vel = 10 + score * 0.02

        if self.vel > self.MAX_VEL:
            self.vel = self.MAX_VEL

        self.x1 -= self.vel
        self.x2 -= self.vel

        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH

        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH

    def draw(self, win):
        win.blit(self.IMG, (self.x1, self.y))
        win.blit(self.IMG, (self.x2, self.y))


class Obs:
    MAX_VEL = 30

    def __init__(self, x):
        self.x = x
        self.img = OBS_IMGS[random.randrange(0, 5)]
        self.y = 500 - self.img.get_height() + 15
        self.vel = 0

    def move(self, score):
        self.vel = 10 + score * 0.02

        if self.vel > self.MAX_VEL:
            self.vel = self.MAX_VEL

        self.x -= self.vel

    def draw(self, win):
        win.blit(self.img, (self.x, self.y))

    def collide(self, dino):
        dino_mask = dino.get_mask()
        obs_mask = pygame.mask.from_surface(self.img)
        obs_offset = (self.x - dino.x, self.y - round(dino.y))
        is_overlap = dino_mask.overlap(obs_mask, obs_offset)

        if is_overlap:
            return True
        return False


def draw_window(win, dino, base, obs, score):
    win.blit(BG_IMG, (0, 0))

    base.draw(win)

    for obstacle in obs:
        obstacle.draw(win)

    dino.draw(win)

    text = STAT_FONT.render(str(score), 1, (0, 0, 0))
    win.blit(text, (WIN_WIDTH - 10 - text.get_width(), 10))

    pygame.display.update()


def main():
    base = Base(500)
    obs = [Obs(WIN_WIDTH + 100)]
    dino = Dino(100, 500 - DINO_IMGS[0].get_height() + 15)
    clock = pygame.time.Clock()
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

    run = True
    score = 0
    while run:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()

        score += 1

        dino.move()

        # dino.jump()

        for obstacle in obs:
            obstacle.move(score)
            if obstacle.x + obstacle.img.get_width() < -200:
                obs.remove(obstacle)
                obs.append(Obs(WIN_WIDTH + 100))

        base.move(score)

        draw_window(win, dino, base, obs, score)


main()
