# encoding: utf-8

# imports
import sys
import pygame
import random
import time
from pygame.locals import *
import slide1
import slide2
import common


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
    overall_scoreboard = common.ScoreBoard(0, 0)

    # init presentation
    slide_one = slide1.Slide1(screen)
    slide_two = slide2.Slide2(screen)

    # play slide 1
    slidewinner = slide_one.play()
    if not slidewinner == 0:
        overall_scoreboard.increase(slidewinner)

    # play slide 2
    slidewinner = slide_two.play()
    if not slidewinner == 0:
        overall_scoreboard.increase(slidewinner)

    print overall_scoreboard.get_winner()

# run
if __name__ == '__main__':
    main()
