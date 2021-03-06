# encoding: utf-8

import sys
import pygame
import random
import time
from pygame.locals import *
from common import *



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
        offset1 = (random.randint(-295, 295), random.randint(-227, 227))
        offset2 = (offset1[0] * -1, offset1[1] * -1)
        self.cat.move(offset1)
        self.mouse.move(offset2)
        self.cat, self.mouse = self.mouse, self.cat

    def timeout(self):
        self.score.increase(self.mouse.name)
        self.cat.swapimage()
        self.mouse.swapimage()
        offset1 = (random.randint(-295, 295), random.randint(-227, 227))
        offset2 = (offset1[0] * -1, offset1[1] * -1)
        self.cat.move(offset1)
        self.mouse.move(offset2)
        self.cat, self.mouse = self.mouse, self.cat


class Slide1(Slide):
    def __init__(self, screen):
        # screen
        self.screen = screen

        # players
        player1image = pygame.image.load('pics/player1.png').convert_alpha()
        player1altimage = pygame.image.load('pics/altplayer1.png').convert_alpha()
        player2image = pygame.image.load('pics/player2.png').convert_alpha()
        player2altimage = pygame.image.load('pics/altplayer2.png').convert_alpha()
        self.player1 = PlayerObject('1', player1image, player1altimage, (0, 0))
        self.player2 = PlayerObject('2', player2image, player2altimage, (590, 455))

        # background
        self.background = Background('pics/slide1.png')

        # local scoreboard
        self.scoreboard = ScoreBoard(0, 0)

        # draw players and background to the screen
        screen.blit(self.background.image, (0, 0), self.background.rect)
        screen.blit(self.scoreboard.image, self.scoreboard.rect)
        pygame.display.update()

        # init game
        self.game = CatMouse(self.player1, self.player2, self.scoreboard)

        # init clock
        self.clock = pygame.time.Clock()

        # counter
        self.counter = Countdowner(5)
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

            # redraw screen
            self.screen.blit(self.background.image, self.player1.rect, self.player1.rect)
            self.screen.blit(self.background.image, self.player2.rect, self.player2.rect)
            self.screen.blit(self.background.image, self.scoreboard.rect, self.scoreboard.rect)
            self.screen.blit(self.background.image, self.counter.rect, self.counter.rect)
            self.player1.update()
            self.player2.update()
            if self.player1.rect.colliderect(self.player2.rect):
                self.game.catched()
                self.counter.reset()
            if self.counter.time == 0:
                self.game.timeout()
                self.counter.reset()
            self.screen.blit(self.player1.image, self.player1.rect)
            self.screen.blit(self.player2.image, self.player2.rect)
            self.screen.blit(self.scoreboard.image, self.scoreboard.rect)
            self.screen.blit(self.counter.image, self.counter.rect)
            pygame.display.update()

        return self.scoreboard.get_winner()
