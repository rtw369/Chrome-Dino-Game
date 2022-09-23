import pygame
import neat
import pickle
import os
import random

WIN_WIDTH = 1000
WIN_HEIGHT = 800

GEN = 0

pygame.font.init()
STAT_FONT = pygame.font.SysFont("comicsans", 50)

high_score = 0

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
        self.down_pressed = False

    def jump(self):
        self.down_pressed = False

        if self.y >= 500 - self.img.get_height() + 15:
            self.vel = -13
            self.tick_count = 0
        self.height = self.y

    def crouch(self):
        if self.y >= 500 - self.img.get_height() + 15:
            self.down_pressed = True

    def move(self):
        self.tick_count += 1

        d = self.vel * self.tick_count + 1.5 * self.tick_count ** 2

        # makes the dino fall slower.
        if d >= 16:
            d = 16

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
        else:
            self.y = 500 - self.img.get_height() + 15

        win.blit(self.img, (self.x, self.y))

    def draw_crouch(self, win):
        self.img_count += 1

        if self.img_count < self.ANIMATION_TIME:
            self.img = self.IMGS[3]
        elif self.img_count < self.ANIMATION_TIME * 2:
            self.img = self.IMGS[4]
        elif self.img_count < self.ANIMATION_TIME * 2 + 1:
            self.img = self.IMGS[3]
            self.img_count = 0

        self.y = 500 - self.img.get_height() + 15

        win.blit(self.img, (self.x, self.y))

    def draw_dead(self, win):
        self.img = self.IMGS[5]
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
        self.vel = 20 + score * 0.01

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
    ANIMATION_TIME = 5
    MAX_VEL = 30

    def __init__(self, x):
        self.x = x
        self.img_num = random.randrange(0, 8)
        self.img = OBS_IMGS[self.img_num]
        self.img_count = 0

        if self.img_num == 6 or self.img_num == 7:
            n = random.randrange(1, 5)
            if n == 1:
                self.y = 500 - self.img.get_height() + 15
            elif n == 2 or n == 3:
                self.y = 500 - self.img.get_height() + 15 - DINO_IMGS[0].get_height() - 20
            else:
                self.y = 500 - self.img.get_height() - DINO_IMGS[3].get_height() + 15
        else:
            self.y = 500 - self.img.get_height() + 15

        self.vel = 0

    def move(self, score):
        self.vel = 20 + score * 0.01

        if self.vel > self.MAX_VEL:
            self.vel = self.MAX_VEL

        self.x -= self.vel

    def draw(self, win):
        self.img_count += 1

        if self.img_num == 6 or self.img_num == 7:
            if self.img_count < self.ANIMATION_TIME:
                self.img = OBS_IMGS[6]
            elif self.img_count < self.ANIMATION_TIME * 2:
                self.img = OBS_IMGS[7]
            elif self.img_count < self.ANIMATION_TIME * 2 + 1:
                self.img = OBS_IMGS[6]
                self.img_count = 0

        win.blit(self.img, (self.x, self.y))

    def collide(self, dino):
        dino_mask = dino.get_mask()
        obs_mask = pygame.mask.from_surface(self.img)
        obs_offset = (self.x - dino.x, self.y - round(dino.y))
        is_overlap = dino_mask.overlap(obs_mask, obs_offset)

        if is_overlap:
            return True
        return False


def draw_window(win, dinos, base, obs, score):
    win.blit(BG_IMG, (0, 0))

    base.draw(win)

    for obstacle in obs:
        obstacle.draw(win)

    for dino in dinos:
        if dino.down_pressed:
            dino.draw_crouch(win)
        else:
            dino.draw(win)

    text = STAT_FONT.render(str(score), 1, (0, 0, 0))
    win.blit(text, (WIN_WIDTH - 10 - text.get_width(), 70))

    text = STAT_FONT.render("HI "+str(high_score), 1, (0, 0, 0))
    win.blit(text, (WIN_WIDTH - 10 - text.get_width(), 10))

    text = STAT_FONT.render("Gen: " + str(GEN), 1, (0, 0, 0))
    win.blit(text, (10, 10))

    text = STAT_FONT.render("Dino #: " + str(len(dinos)), 1, (0, 0, 0))
    win.blit(text, (10, 70))

    pygame.display.update()


def draw_default_win(win, dino, base, obs, score):
    win.blit(BG_IMG, (0, 0))

    base.draw(win)

    for obstacle in obs:
        obstacle.draw(win)

    if dino.down_pressed:
        dino.draw_crouch(win)
    else:
        dino.draw(win)

    text = STAT_FONT.render(str(score), 1, (0, 0, 0))
    win.blit(text, (WIN_WIDTH - 10 - text.get_width(), 70))

    text = STAT_FONT.render("HI " + str(high_score), 1, (0, 0, 0))
    win.blit(text, (WIN_WIDTH - 10 - text.get_width(), 10))

    pygame.display.update()


def play():
    global high_score

    base = Base(500)
    obs = [Obs(WIN_WIDTH + 100)]
    dinos = [Dino(100, 500 - DINO_IMGS[0].get_height() + 15)]
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

        for dino in dinos:
            dino.move()

            if pygame.key.get_pressed()[pygame.K_DOWN]:
                dino.crouch()
            else:
                dino.down_pressed = False

            if pygame.key.get_pressed()[pygame.K_SPACE] and not pygame.key.get_pressed()[pygame.K_DOWN]:
                dino.jump()

        for obstacle in obs:
            obstacle.move(score)

            for dino in dinos:
                if obstacle.collide(dino):
                    run = False

                    if score > high_score:
                        high_score = score

            if obstacle.x + obstacle.img.get_width() < 300 and len(obs) < 2:
                obs.append(Obs(WIN_WIDTH + random.randrange(0, 300)))

            if obstacle.x + obstacle.img.get_width() < -200:
                obs.remove(obstacle)

        base.move(score)

        draw_window(win, dinos, base, obs, score)

    while not run:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        for dino in dinos:
            dino.draw_dead(win)
        pygame.display.update()

        if pygame.key.get_pressed()[pygame.K_SPACE]:
            play()


def eval_gen(genomes, config):
    global GEN
    GEN += 1
    nets = []
    ge = []
    dinos = []

    for _, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        dinos.append(Dino(100, 500 - DINO_IMGS[0].get_height() + 15))
        g.fitness = 0
        ge.append(g)

    base = Base(500)
    obs = [Obs(WIN_WIDTH + 100)]
    clock = pygame.time.Clock()
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

    run = True
    global high_score
    score = 0

    while run:
        # clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()

        score += 1

        obs_ind = 0
        if len(dinos) > 0:
            if len(obs) > 1 and dinos[0].x > obs[0].x + obs[0].img.get_width():
                obs_ind = 1
        else:
            if score > high_score:
                high_score = score

            run = False
            break

        for x, dino in enumerate(dinos):
            dino.move()

            ge[x].fitness += 0.1

            output = nets[x].activate((obs[obs_ind].y - (500 - DINO_IMGS[0].get_height() + 15),
                                       abs(dino.x - obs[obs_ind].x), obs[obs_ind].vel))

            if output[1] > 0.5:
                dino.crouch()
            elif output[0] > 0.5:
                dino.down_pressed = False
                dino.jump()
            else:
                dino.down_pressed = False

        base.move(score)

        for obstacle in obs:
            obstacle.move(score)

            for x, dino in enumerate(dinos):
                if obstacle.collide(dino):
                    ge[x].fitness -= 1
                    dinos.pop(x)
                    nets.pop(x)
                    ge.pop(x)

                if score > 10000:
                    ge[x].fitness += 100
                    dinos.pop(x)
                    nets.pop(x)
                    ge.pop(x)

            if obstacle.x + obstacle.img.get_width() < 300 and len(obs) < 2:
                obs.append(Obs(WIN_WIDTH + random.randrange(0, 300)))

            if obstacle.x + obstacle.img.get_width() < -200:
                obs.remove(obstacle)

        draw_window(win, dinos, base, obs, score)


def run_genome(genomes, config):
    nets = []
    ge = []
    dinos = []

    for _, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        dinos.append(Dino(100, 500 - DINO_IMGS[0].get_height() + 15))
        g.fitness = 0
        ge.append(g)

    dino = dinos[0]

    base = Base(500)
    obs = [Obs(WIN_WIDTH + 100)]
    clock = pygame.time.Clock()
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

    run = True
    global high_score
    score = 0

    while run:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()

        score += 1

        obs_ind = 0
        if len(dinos) > 0:
            if len(obs) > 1 and dinos[0].x > obs[0].x + obs[0].img.get_width():
                obs_ind = 1
        else:
            run = False
            break

        dino.move()

        output = nets[0].activate((obs[obs_ind].y - (500 - DINO_IMGS[0].get_height() + 15),
                                   abs(dino.x - obs[obs_ind].x), obs[obs_ind].vel))

        if output[1] > 0.5:
            dino.crouch()
        elif output[0] > 0.5:
            dino.down_pressed = False
            dino.jump()
        else:
            dino.down_pressed = False

        base.move(score)

        for obstacle in obs:
            obstacle.move(score)

            if obstacle.collide(dino):
                run = False

                if score > high_score:
                    high_score = score

            if obstacle.x + obstacle.img.get_width() < 300 and len(obs) < 2:
                obs.append(Obs(WIN_WIDTH + random.randrange(0, 300)))

            if obstacle.x + obstacle.img.get_width() < -200:
                obs.remove(obstacle)

        draw_default_win(win, dino, base, obs, score)

    while not run:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        dino.draw_dead(win)
        pygame.display.update()

        if pygame.key.get_pressed()[pygame.K_SPACE]:
            run_genome(genomes, config)


def run(config_path):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet,
                                neat.DefaultStagnation, config_path)

    p = neat.Population(config)

    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    '''winner = p.run(eval_gen, 20)

    with open("DinoAI2.pickle", "wb") as f:
        pickle.dump(winner, f)'''

    pickle_in = open("DinoAI2.pickle", "rb")
    genome = pickle.load(pickle_in)
    genomes = [(1, genome)]

    run_genome(genomes, config)


if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config.txt")
    run(config_path)


# play()
