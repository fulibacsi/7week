# encoding: utf-8

# imports
import sys
import pygame
import random
import time
from pygame.locals import *


class PlayerObject():
    def __init__(self, name, image, altimage, pos):
        self.name = name
        self.image = image
        self.altimage = altimage
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(pos)
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.speed = 10
        self.state = "still"
        self.score = 0
        self.reinit()

    def reinit(self):
        self.state = "still"
        self.movepos = [0,0]

    def update(self):
        newpos = self.rect.move(self.movepos)
        if self.area.contains(newpos):
            self.rect = newpos
        pygame.event.pump()

    def moveup(self):
        self.movepos[1] = self.movepos[1] - (self.speed)
        self.state = "moveup"

    def movedown(self):
        self.movepos[1] = self.movepos[1] + (self.speed)
        self.state = "movedown"

    def moveleft(self):
        self.movepos[0] = self.movepos[0] - (self.speed)
        self.state = "moveleft"

    def moveright(self):
        self.movepos[0] = self.movepos[0] + (self.speed)
        self.state = "moveright"

    def reposition(self, pos):
        newpos = self.rect.move(pos)
        if self.area.contains(newpos):
            self.rect = newpos
        pygame.event.pump()
        self.reinit()

    def swapimage(self):
        self.image, self.altimage = self.altimage, self.image


class ScoreBoard():
    def __init__(self, score1, score2):
        self.score1 = score1
        self.score2 = score2
        self.font = pygame.font.SysFont("Ubuntu Sans", 24)
        self.image = self.font.render("P1: {0}   P2: {1}".format(self.score1, self.score2), 1, (255, 255, 0))
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(300,20)

    def increase(self, player):
        if player == '1':
            self.score1 += 1
        else:
            self.score2 += 1
        self.image = self.font.render("P1: {0}   P2: {1}".format(self.score1, self.score2), 1, (255, 255, 0))
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(300,20)

    def get_winner(self):
        if self.score1 > self.score2:
            return 1
        elif self.score2 > self.score1:
            return 2
        else:
            return 0

class Countdowner():
    def __init__(self):
        self.time = 10
        self.font = pygame.font.SysFont("Ubuntu Sans", 24)
        self.image = self.font.render("{0:0=2d}".format(self.time), 1, (255, 255, 0))
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(300, 460)

    def refresh(self):
        self.time -= 1
        if self.time == -1:
            self.time = 10
        self.image = self.font.render("{0:0=2d}".format(self.time), 1, (255, 255, 0))
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(300, 460)

    def reset(self):
        self.time = 10
        self.image = self.font.render("{0:0=2d}".format(self.time), 1, (255, 255, 0))
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(300, 460)


class CatMouse():
    def __init__(self, player1, player2, score):
        self.cat = player1
        self.cat.swapimage()
        self.mouse = player2
        self.score = score

    def catched(self):
        self.score.increase(self.cat.name)
        self.cat.swapimage()
        self.mouse.swapimage()
        self.cat, self.mouse = self.mouse, self.cat
        offset1 = (random.randint(-295, 295), random.randint(-227, 227))
        offset2 = (offset1[0] * -1, offset1[1] * -1)
        self.cat.reposition(offset1)
        self.mouse.reposition(offset2)


class Background():
    def __init__(self, imagefile):
        self.image = pygame.image.load(imagefile).convert()
        self.rect = self.image.get_rect()

    def change(self, imagefile):
        self.image = pygame.image.load(imagefile).convert()
        self.rect = self.image.get_rect()


class Slide():
    def __init__(self, screen):
        # screen
        self.screen = screen

        # players
        player1image = pygame.image.load('pics/player1.png').convert()
        player1altimage = pygame.image.load('pics/altplayer1.png').convert()
        player2image = pygame.image.load('pics/player2.png').convert()
        player2altimage = pygame.image.load('pics/altplayer2.png').convert()
        self.player1 = PlayerObject('1', player1image, player1altimage, (0, 0))
        self.player2 = PlayerObject('2', player2image, player2altimage, (590, 455))

        # background
        self.background = Background('pics/background.png')

        # local scoreboard
        self.scoreboard = ScoreBoard(0, 0)

        # draw players and background to the screen
        screen.blit(self.background.image, (0, 0))
        screen.blit(self.scoreboard.image, self.scoreboard.rect)
        pygame.display.update()

        # init game1
        self.game = CatMouse(self.player1, self.player2, self.scoreboard)

        # init clock
        self.clock = pygame.time.Clock()

        # counter
        self.counter = Countdowner()
        self.TIMECOUNTDOWN = USEREVENT + 1
        pygame.time.set_timer(self.TIMECOUNTDOWN, 1000)
        self.running = True


    def play(self):
        while self.running:
            # 60fps FTW
            self.clock.tick(60)

            # event handling
            if pygame.event.get(self.TIMECOUNTDOWN):
                self.counter.refresh()

            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit()
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.running = False
                    # player 1
                    elif event.key == K_UP:
                        self.player1.moveup()
                    elif event.key == K_DOWN:
                        self.player1.movedown()
                    elif event.key == K_LEFT:
                        self.player1.moveleft()
                    elif event.key == K_RIGHT:
                        self.player1.moveright()
                    # player 2
                    if event.key == K_w:
                        self.player2.moveup()
                    elif event.key == K_s:
                        self.player2.movedown()
                    elif event.key == K_a:
                        self.player2.moveleft()
                    elif event.key == K_d:
                        self.player2.moveright()
                elif event.type == KEYUP:
                    if event.key in (K_UP, K_LEFT, K_RIGHT, K_DOWN):
                        self.player1.reinit()
                    if event.key in (K_w, K_s, K_a, K_d):
                        self.player2.reinit()

            # redraw
            self.screen.blit(self.background.image, self.player1.rect, self.player1.rect)
            self.screen.blit(self.background.image, self.player2.rect, self.player2.rect)
            self.screen.blit(self.background.image, self.scoreboard.rect, self.scoreboard.rect)
            self.screen.blit(self.background.image, self.counter.rect, self.counter.rect)
            self.player1.update()
            self.player2.update()
            if self.player1.rect.colliderect(self.player2.rect) or self.counter.time == 0:
                self.game.catched()
                self.counter.refresh()
            self.screen.blit(self.player1.image, self.player1.rect)
            self.screen.blit(self.player2.image, self.player2.rect)
            self.screen.blit(self.scoreboard.image, self.scoreboard.rect)
            self.screen.blit(self.counter.image, self.counter.rect)
            pygame.display.update()

        return self.scoreboard.get_winner()


def main():
    # init
    # pygame
    pygame.init()
    pygame.font.init()

    # random
    random.seed(time.time())

    # screen
    screen = pygame.display.set_mode((640, 480))

    # scoreboard
    overall_scoreboard = ScoreBoard(0, 0)

    # init presentation
    slide1 = Slide(screen)
    slide1winner = slide1.play()
    if not slide1winner == 0:
        overall_scoreboard.increase(slide1winner)

    print overall_scoreboard.get_winner()

# run
if __name__ == '__main__':
    main()
