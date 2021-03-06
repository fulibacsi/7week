# encoding: utf-8

import sys
import pygame
import random
import time
from pygame.locals import *
from common import *

BALLSPEED = 3


class Ball():
    def __init__(self, pos, screen, x_speed, y_speed):
        self.screen = screen
        self.area = self.screen.get_rect()
        self.pos = pos
        self.x_speed = x_speed
        self.y_speed = y_speed
        self.image = pygame.image.load('pics/missile.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(pos)

    def pong(self):
        self.x_speed *= -1

    def ping(self):
        self.y_speed *= -1

    def reset(self):
        newpos = self.rect.move(320 - self.pos[0], 240 - self.pos[1])
        if self.area.contains(newpos):
            self.rect = newpos
            self.pos = (320, 240)
            self.y_speed *= -1
        self.refresh()

    def refresh(self):
        newpos = self.rect.move(self.y_speed, self.x_speed)
        if self.area.contains(newpos):
            self.rect = newpos
            self.pos = (self.pos[0] + self.y_speed, self.pos[1] + self.x_speed)

    def render(self):
        self.screen.blit(self.image, self.rect)


class Pong():
    def __init__(self, screen, player1, player2, score):
        self.screen = screen
        self.score = score
        self.player1 = player1
        self.player2 = player2
        self.ball = Ball((320, 240), self.screen, BALLSPEED, BALLSPEED)

    def refresh(self):
        if self.ball.pos[1] < 10 or self.ball.pos[1] > 460:
            self.ball.pong()
        if self.ball.pos[0] < 10:
            if not self.player1.rect.colliderect(self.ball.rect):
                self.score.increase(self.player2.name)
                self.ball.reset()
            else:
                self.ball.ping()
        elif self.ball.pos[0] > 620:
            if not self.player2.rect.colliderect(self.ball.rect):
                self.score.increase(self.player1.name)
                self.ball.reset()
            else:
                self.ball.ping()

        if self.player2.rect.colliderect(self.ball.rect) or self.player1.rect.colliderect(self.ball.rect):
            self.ball.ping()

        self.ball.refresh()
        self.ball.render()


class Slide3(Slide):
    def __init__(self, screen):
        # screen
        self.screen = screen

        # players
        player1image = pygame.image.load('pics/player1.png').convert_alpha()
        player1altimage = pygame.image.load('pics/altplayer1.png').convert_alpha()
        player2image = pygame.image.load('pics/player2.png').convert_alpha()
        player2altimage = pygame.image.load('pics/altplayer2.png').convert_alpha()
        self.player1 = PlayerObject('1', player1image, player1altimage, (0, 455))
        self.player2 = PlayerObject('2', player2image, player2altimage, (590, 455))

        # background
        self.background = Background('pics/slide3.png')

        # local scoreboards
        self.scoreboard = ScoreBoard(0, 0)
        self.overall_scoreboard = ScoreBoard(0, 0, (500, 20), (0, 255, 0))

        # draw players and background to the screen
        screen.blit(self.background.image, self.background.rect)
        screen.blit(self.scoreboard.image, self.scoreboard.rect)
        pygame.display.update()

        # init game
        self.game = Pong(self.screen, self.player1, self.player2, self.scoreboard)

         # init clock
        self.clock = pygame.time.Clock()

        # counter
        self.counter = Countdowner(45)
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
                        self.player1.movedown()
                    elif event.key == K_RIGHT:
                        self.player1.moveup()

                    # player 2
                    if event.key == K_w:
                        self.player2.moveup()
                    elif event.key == K_s:
                        self.player2.movedown()
                    elif event.key == K_a:
                        self.player2.movedown()
                    elif event.key == K_d:
                        self.player2.moveup()

                elif event.type == KEYUP:
                    if event.key in (K_UP, K_LEFT, K_RIGHT, K_DOWN):
                        self.player1.reinit()
                    if event.key in (K_w, K_s, K_a, K_d):
                        self.player2.reinit()


            # redraw screen
            self.screen.blit(self.background.image, self.player1.rect, self.player1.rect)
            self.screen.blit(self.background.image, self.player2.rect, self.player2.rect)
            self.screen.blit(self.background.image, self.scoreboard.rect, self.scoreboard.rect)
            self.screen.blit(self.background.image, self.overall_scoreboard.rect, self.overall_scoreboard.rect)
            self.screen.blit(self.background.image, self.counter.rect, self.counter.rect)
            self.screen.blit(self.background.image, self.game.ball.rect, self.game.ball.rect)
            self.player1.update()
            self.player2.update()
            self.game.refresh()
            self.screen.blit(self.player1.image, self.player1.rect)
            self.screen.blit(self.player2.image, self.player2.rect)
            self.screen.blit(self.overall_scoreboard.image, self.overall_scoreboard.rect)
            self.screen.blit(self.scoreboard.image, self.scoreboard.rect)
            self.screen.blit(self.counter.image, self.counter.rect)
            self.screen.blit(self.game.ball.image, self.game.ball.rect)
            pygame.display.update()
            if self.counter.time == 0:
                self.overall_scoreboard.increase(self.scoreboard.get_winner())
                if abs(self.game.ball.y_speed) < 8:
                    self.game.ball.y_speed = int(self.game.ball.y_speed * 1.5)
                    self.game.ball.x_speed = int(self.game.ball.x_speed * 1.5)
                self.counter.reset()
                self.scoreboard.reset()

        return self.overall_scoreboard.get_winner()    
