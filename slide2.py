# encoding: utf-8

import sys
import pygame
import random
from pygame.locals import *
from common import *


ENEMYMISSILESPEED = 5
PLAYERMISSILESPEED = -5

class Missile:
    def __init__(self, pos, screen, missile_speed = 5):
        self.screen = screen
        self.area = self.screen.get_rect()
        self.pos = pos
        self.missile_speed = missile_speed
        self.image = pygame.image.load('pics/missile.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(pos)

    def refresh(self):
        newpos = self.rect.move((0, self.missile_speed))
        if self.area.contains(newpos):
            self.rect = newpos
            self.pos = (self.pos[0], self.pos[1] + self.missile_speed)

    def render(self):
        self.screen.blit(self.image, self.rect)


class Enemy:
    def __init__(self, pos, screen):
        self.screen = screen
        self.area = self.screen.get_rect()
        self.pos = pos
        self.image = pygame.image.load('pics/enemy.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(pos)
        self.alive = True

    def shoot(self):
        return Missile(self.pos, self.screen, ENEMYMISSILESPEED)

    def move(self, speed):
        newpos = self.rect.move((speed, 0))
        if self.area.contains(newpos):
            self.rect = newpos
            self.pos = (self.pos[0] + speed, self.pos[1])

    def render(self):
        if self.alive:
		    self.screen.blit(self.image, self.rect)

    def die(self):
        self.alive = False


class InvaderPlayer(PlayerObject):
    def shoot(self):
        return Missile(self.pos, self.screen, PLAYERMISSILESPEED)


class Invaders():
    def __init__(self, screen, player1, player2, score, number_of_enemies):
        self.enemies = []
        self.screen = screen
        self.init_enemies(number_of_enemies)
        self.enemy_missiles = []
        self.player1 = player1
        self.player2 = player2
        self.player1missile = None
        self.player2missile = None
        self.score = score
        self.enemy_speed = 3

    def init_enemies(self, number):
        for i in range(0, number):
            self.enemies.append(Enemy((10 + i*35, 10), self.screen))

    def playershoot(self, player, missile):
        if player.name == self.player1.name and self.player1missile == None:
            self.player1missile = missile
        elif player.name == self.player2.name and self.player2missile == None:
            self.player2missile = missile

    def refresh(self):
        if self.enemies[len(self.enemies) - 1].pos[0] + self.enemy_speed > 590:
            self.enemy_speed = -3
        if self.enemies[0].pos[0] + self.enemy_speed < 10:
            self.enemy_speed = 3

        for enemy in self.enemies:
            if not self.player1missile == None:
                if enemy.rect.colliderect(self.player1missile.rect):
                    enemy.die()
                    self.score.increase(self.player1.name)
                    self.player1missile = None
            if not self.player2missile == None:
                if enemy.rect.colliderect(self.player2missile.rect):
                    enemy.die()
                    self.score.increase(self.player2.name)
                    self.player2missile = None
            if enemy.alive:
                enemy.move(self.enemy_speed)
                enemy.render()
                if random.randint(1,100) > 99:
                    self.enemy_missiles.append(enemy.shoot())
            else:
                self.enemies.remove(enemy)

        if not self.player1missile == None:
            self.player1missile.refresh()
            self.player1missile.render()
            if self.player1missile.pos[1] < 10:
                self.player1missile = None
        if not self.player2missile == None:
            self.player2missile.refresh()
            self.player2missile.render()
            if self.player2missile.pos[1] < 10:
                self.player2missile = None

        for missile in self.enemy_missiles:
            if self.player1.rect.colliderect(missile.rect):
                self.score.decrease(self.player1.name)
                self.enemy_missiles.remove(missile)
            elif self.player2.rect.colliderect(missile.rect):
                self.score.decrease(self.player2.name)
                self.enemy_missiles.remove(missile)
            elif missile.pos[1] > 455:
                self.enemy_missiles.remove(missile)
            else:
                missile.refresh()
                missile.render()

        if len(self.enemies) == 0:
            self.init_enemies(10)


class Slide2(Slide):
    def __init__(self, screen):
        # screen
        self.screen = screen

        # players
        player1image = pygame.image.load('pics/player1.png').convert_alpha()
        player1altimage = pygame.image.load('pics/altplayer1.png').convert_alpha()
        player2image = pygame.image.load('pics/player2.png').convert_alpha()
        player2altimage = pygame.image.load('pics/altplayer2.png').convert_alpha()
        self.player1 = InvaderPlayer('1', player1image, player1altimage, (0, 455))
        self.player2 = InvaderPlayer('2', player2image, player2altimage, (590, 455))

        # background
        self.background = Background('pics/slide2.png')

        # local scoreboards
        self.scoreboard = ScoreBoard(0, 0)
        self.overall_scoreboard = ScoreBoard(0, 0, (500, 20), (0, 255, 0))

        # draw players and background to the screen
        screen.blit(self.background.image, (0, 0), self.background.rect)
        screen.blit(self.scoreboard.image, self.scoreboard.rect)
        pygame.display.update([self.background.rect, self.scoreboard.rect])

        # init game
        self.game = Invaders(self.screen, self.player1, self.player2, self.scoreboard, 10)

         # init clock
        self.clock = pygame.time.Clock()

        # counter
        self.counter = Countdowner(99)
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
                        self.player1.moveright()
                    elif event.key == K_DOWN:
                        self.player1.moveleft()
                    elif event.key == K_LEFT:
                        self.player1.moveleft()
                    elif event.key == K_RIGHT:
                        self.player1.moveright()
                    elif event.key == K_RSHIFT:
                        self.game.playershoot(self.player1, self.player1.shoot())
                    # player 2
                    if event.key == K_w:
                        self.player2.moveright()
                    elif event.key == K_s:
                        self.player2.moveleft()
                    elif event.key == K_a:
                        self.player2.moveleft()
                    elif event.key == K_d:
                        self.player2.moveright()
                    elif event.key == K_LSHIFT:
                        self.game.playershoot(self.player2, self.player2.shoot())

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
            for enemy in self.game.enemies:
                self.screen.blit(self.background.image, enemy.rect, enemy.rect)
            for missile in self.game.enemy_missiles:
                self.screen.blit(self.background.image, missile.rect, missile.rect)
            self.player1.update()
            self.player2.update()
            if not self.game.player1missile == None:
                self.screen.blit(self.background.image, self.game.player1missile.rect, self.game.player1missile.rect)
            if not self.game.player2missile == None:
                self.screen.blit(self.background.image, self.game.player2missile.rect, self.game.player2missile.rect)
            self.game.refresh()
            self.screen.blit(self.player1.image, self.player1.rect)
            self.screen.blit(self.player2.image, self.player2.rect)
            self.screen.blit(self.overall_scoreboard.image, self.overall_scoreboard.rect)
            self.screen.blit(self.scoreboard.image, self.scoreboard.rect)
            self.screen.blit(self.counter.image, self.counter.rect)
            pygame.display.update()
            if self.counter.time == 0:
                self.overall_scoreboard.increase(self.scoreboard.get_winner())
                self.scoreboard.reset()

        return self.overall_scoreboard.get_winner()    
