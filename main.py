import pygame as pg
from random import randint, choice
from math import sqrt

WIDTH = 500
HEIGHT = 500
PAUSE = 25


class Salut:
    START_RADIUS = 3
    MAX_RADIUS = 100
    RAND_COLOR = lambda : (randint( 20, 255 ),
                        randint( 20, 255 ),
                        randint( 20, 255 ) )
    START = ( (WIDTH//2, HEIGHT//2), START_RADIUS )
    CIRCLES = [ [ RAND_COLOR(), *START ] ]
    def draw(window):
        if len( Salut.CIRCLES ) >= 100:
            Salut.CIRCLES = [ [ Salut.RAND_COLOR(), *Salut.START ] ]
            return
        new = []
        for c in Salut.CIRCLES:
            c[2] += 3
            if c[2] < Salut.MAX_RADIUS:
                new.append( c )
            else:
                for i in range( 3 ):
                    color = Salut.RAND_COLOR()
                    x = randint( - c[2], c[2] ) *\
                        choice( (1, -1) )
                    y = int( sqrt( c[2] ** 2 - x ** 2 ) ) *\
                        choice( (1, -1) )
                    new.append( [color, (c[1][0] + x, c[1][1] + y),
                                 Salut.START_RADIUS] )
        Salut.CIRCLES = new
        for c in Salut.CIRCLES:
            pg.draw.circle( window, c[0], c[1], c[2], 1 )


class Ball:
    RA = 10
    LEN = 5
    def __init__(self):
        self.x = 0
        self.y = 0
        self.v_x = 0
        self.v_y = 0
        self.score = [0, 0]
        self.score_text = pg.Surface((0, 0))
        self.start()

    def start(self, left=0, right=0):
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        l = self.LEN
        self.v_x = randint(1, l - 1) * choice((1, -1))
        self.v_y = int(sqrt(l ** 2 - self.v_x ** 2)) * choice((1, -1))
        self.score[0] += int(right)
        self.score[1] += int(left)
        font = pg.font.SysFont('Arial', 14)
        self.score_text = font.render(
            f'Счет 1: {self.score[0]}\t Счет 2: {self.score[1]}',
            1, (255, 255, 255))

    def move(self, rac_1, rac_2):
        x = self.x + self.v_x
        if x + self.RA >= WIDTH or x - self.RA < 0:
            #self.v_x = -self.v_x
            self.start(x - self.RA < 0, x + self.RA >= WIDTH)

        y = self.y + self.v_y
        if y + self.RA >= HEIGHT or y - self.RA < 0:
            self.v_y = -self.v_y

        rac_touch = self.rac_touch_hard
        rac_touch(rac_1)
        rac_touch(rac_2)

        self.x += self.v_x
        self.y += self.v_y

    def rac_touch_easy(self, rac):
        if rac.y - rac.RA <= self.y + self.v_y <= rac.y + rac.RA\
                and abs(self.x + self.v_x - rac.x) < 10:
            self.v_x = -self.v_x

    def rac_touch_hard(self, rac):
        normal = pg.Vector2(self.x - rac.x, self.y - rac.y)
        if normal.length() <= rac.RA + self.RA:
            speed = pg.Vector2(self.v_x, self.v_y)
            new = speed.reflect(normal)
            new.scale_to_length(new.length() + 1)
            self.v_x, self.v_y = int(new.x), int(new.y)
            while normal.length() <= rac.RA + self.RA:
                self.x += self.v_x
                self.y += self.v_y
                normal = pg.Vector2(self.x - rac.x, self.y - rac.y)


    def draw(self, screen):
        screen.blit(self.score_text, (WIDTH // 2 - 60, 5))
        pg.draw.circle(screen, (255, 0, 0), (self.x, self.y), Ball.RA)


class Raquet:
    RA = 20
    STEP = 10
    def __init__(self, x):
        self.x = x
        self.y = HEIGHT // 2
        self.draw = self.draw_hard

    def move(self, dir):
        if 0 <= self.y + dir * self.STEP < HEIGHT:
            self.y += dir * self.STEP

    def draw_easy(self, screen):
        pg.draw.line(screen, (255, 255, 255),
                     (self.x, self.y - self.RA),
                     (self.x, self.y + self.RA), 8)

    def draw_hard(self, screen):
        pg.draw.circle(screen, (255, 255, 255), (self.x, self.y), self.RA)


def game(screen):
    ball = Ball()
    rac_left = Raquet(10)
    rac_right = Raquet(WIDTH - 11)

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return

        keys_pressed = pg.key.get_pressed()
        if keys_pressed[pg.K_UP]:
            rac_right.move(-1)
        if keys_pressed[pg.K_DOWN]:
            rac_right.move(1)
        if keys_pressed[pg.K_w]:
            rac_left.move(-1)
        if keys_pressed[pg.K_s]:
            rac_left.move(1)

        ball.move(rac_left, rac_right)

        screen.fill((0, 0, 0))
        #Salut.draw(screen)
        ball.draw(screen)
        rac_left.draw(screen)
        rac_right.draw(screen)
        pg.display.flip()
        pg.time.wait(PAUSE)


pg.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
game(screen)
pg.quit()