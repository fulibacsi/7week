# encoding: utf-8

import sys
import pygame
import random
import time
from pygame.locals import *


class PlayerObject():
    def __init__(self, name, image, altimage, pos):
        self.name = name
        self.pos = pos
        self.image = image
        self.altimage = altimage
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(pos)
        self.screen = pygame.display.get_surface()
        self.area = self.screen.get_rect()
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
            self.pos = (self.pos[0] + self.movepos[0], self.pos[1] + self.movepos[1])
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

    def move(self, offset):
        newpos = self.rect.move(offset)
        if self.area.contains(newpos):
            self.rect = newpos
            self.pos = (self.pos[0] + offset[0], self.pos[1] + offset[1])

    def shoot(self):
        pass

    def swapimage(self):
        self.image, self.altimage = self.altimage, self.image


class ScoreBoard():
    def __init__(self, score1, score2, pos = None, color = None):
        self.score1 = score1
        self.score2 = score2
        if color == None:
            self.color = (255, 255, 0)
        else:
            self.color = color
        self.font = pygame.font.SysFont("Ubuntu Sans", 24)
        self.image = self.font.render("P1: {0}   P2: {1}".format(self.score1, self.score2), 1, self.color)
        self.rect = self.image.get_rect()
        if pos == None:
            self.defpos = (300,20)
        else:
            self.defpos = pos
        self.rect = self.rect.move(self.defpos[0], self.defpos[1])

    def refresh(self):
        self.image = self.font.render("P1: {0}   P2: {1}".format(self.score1, self.score2), 1, self.color)
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(self.defpos[0], self.defpos[1])

    def increase(self, player):
        if str(player) == '1':
            self.score1 += 1
        elif str(player) == '2':
            self.score2 += 1
        self.refresh()

    def decrease(self, player):
        if str(player) == '1':
            self.score1 -= 1
        elif str(player) == '2':
            self.score2 -= 1
        self.refresh()

    def get_winner(self):
        if self.score1 > self.score2:
            return 1
        elif self.score2 > self.score1:
            return 2
        else:
            return 0

    def reset(self):
        self.score1, self.score2 = 0, 0
        self.refresh()

class Countdowner():
    def __init__(self, start_time = 10):
        self.start_time = start_time
        self.time = self.start_time
        self.font = pygame.font.SysFont("Ubuntu Sans", 24)
        self.image = self.font.render("{0:0=2d}".format(self.time), 1, (255, 255, 0))
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(300, 460)

    def refresh(self):
        self.time -= 1
        if self.time == -1:
            self.time = self.start_time
        self.image = self.font.render("{0:0=2d}".format(self.time), 1, (255, 255, 0))
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(300, 460)

    def reset(self):
        self.time = self.start_time
        self.image = self.font.render("{0:0=2d}".format(self.time), 1, (255, 255, 0))
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(300, 460)



class Background():
    def __init__(self, imagefile):
        self.image = pygame.image.load(imagefile).convert()
        self.rect = self.image.get_rect()

    def change(self, imagefile):
        self.image = pygame.image.load(imagefile).convert()
        self.rect = self.image.get_rect()


class Caption():
    def __init__(self, pos, text):
        self.text = text
        self.pos = pos
        self.color = self.randomcolor()
        self.font = pygame.font.SysFont("Ubuntu Sans", 72)
        self.image = self.font.render(self.text, 1, self.color)
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(self.pos[0], self.pos[1])

    def change_text(self, text):
        self.text = text
        self.refresh()

    def change_color(self):
        self.color = self.randomcolor()
        self.refresh()

    def refresh(self):
        self.image = self.font.render(self.text, 1, self.color)
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(self.pos[0], self.pos[1])

    def randomcolor(self):
        return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))


class Slide():
    def __init__(self):
        pass
    def play(self):
        pass
