# encoding: utf-8

import sys
import pygame
from pygame.locals import *
from common import *


class Slide0(Slide):
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
        self.p1start = False
        self.p2start = False
        self.p1caption = Caption((120, 120), "P1")
        self.p2caption = Caption((420, 120), "P2")
        # background
        self.background = Background('pics/background.png')

        # local scoreboard
        self.scoreboard = ScoreBoard(0, 0)

        # draw players and background to the screen
        screen.blit(self.background.image, (0, 0), self.background.rect)
        screen.blit(self.scoreboard.image, self.scoreboard.rect)
        pygame.display.update()

        # init clock
        self.clock = pygame.time.Clock()

        # colorchange event
        self.COLORCHANGE = USEREVENT + 1
        pygame.time.set_timer(self.COLORCHANGE, 250)
        # run flag
        self.running = True

    def play(self):
        while self.running:
            # 60fps FTW
            self.clock.tick(60)

            # event handling
            if pygame.event.get(self.COLORCHANGE):
                self.p1caption.change_color()
                self.p2caption.change_color()

            # event handling
            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit()
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE and self.p1start and self.p2start:
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
                    elif event.key == K_RSHIFT:
                        self.player1.swapimage()

                    # player 2
                    if event.key == K_w:
                        self.player2.moveup()
                    elif event.key == K_s:
                        self.player2.movedown()
                    elif event.key == K_a:
                        self.player2.moveleft()
                    elif event.key == K_d:
                        self.player2.moveright()
                    elif event.key == K_LSHIFT:
                        self.player2.swapimage()

                elif event.type == KEYUP:
                    if event.key in (K_UP, K_LEFT, K_RIGHT, K_DOWN):
                        self.player1.reinit()
                    if event.key in (K_w, K_s, K_a, K_d):
                        self.player2.reinit()
                    if event.key == K_RSHIFT:
                        self.player1.swapimage()
                    if event.key == K_LSHIFT:
                        self.player2.swapimage()


            if self.player1.rect.colliderect(self.p1caption.rect):
                self.screen.blit(self.background.image, self.p1caption.rect, self.p1caption.rect)
                self.p1start = True
                self.p1caption.change_text("Ready")
            else:
                self.screen.blit(self.background.image, self.p1caption.rect, self.p1caption.rect)
                self.p1start = False
                self.p1caption.change_text("P1")

            if self.player2.rect.colliderect(self.p2caption.rect):
                self.screen.blit(self.background.image, self.p2caption.rect, self.p2caption.rect)
                self.p2start = True
                self.p2caption.change_text("Ready")
            else:
                self.screen.blit(self.background.image, self.p2caption.rect, self.p2caption.rect)
                self.p2start = False
                self.p2caption.change_text("P2")

            # redraw screen
            self.screen.blit(self.background.image, self.player1.rect, self.player1.rect)
            self.screen.blit(self.background.image, self.player2.rect, self.player2.rect)
            self.screen.blit(self.background.image, self.scoreboard.rect, self.scoreboard.rect)
            self.player1.update()
            self.player2.update()
            self.screen.blit(self.p1caption.image, self.p1caption.rect)
            self.screen.blit(self.p2caption.image, self.p2caption.rect)
            self.screen.blit(self.player1.image, self.player1.rect)
            self.screen.blit(self.player2.image, self.player2.rect)
            self.screen.blit(self.scoreboard.image, self.scoreboard.rect)
            pygame.display.update()

        return self.scoreboard.get_winner()
