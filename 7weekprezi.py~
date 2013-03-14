# encoding: utf-8

# imports
import sys
import pygame
import random
import time
from pygame.locals import *
import slide0
import slide1
import slide2
import slide3
import slide4
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
    pygame.display.init()

    # scoreboard
    overall_scoreboard = common.ScoreBoard(0, 0)

    # presentation

    # play slide 0
    slide_zero = slide0.Slide0(screen)
    slidewinner = slide_zero.play()
    if not slidewinner == 0:
        overall_scoreboard.increase(slidewinner)


    # play slide 1
    slide_one = slide1.Slide1(screen)
    slidewinner = slide_one.play()
    if not slidewinner == 0:
        overall_scoreboard.increase(slidewinner)


    # play slide 2
    slide_two = slide2.Slide2(screen)
    slidewinner = slide_two.play()
    if not slidewinner == 0:
        overall_scoreboard.increase(slidewinner)


    # play slide 3
    slide_three = slide3.Slide3(screen)
    slidewinner = slide_three.play()
    if not slidewinner == 0:
        overall_scoreboard.increase(slidewinner)

    # play slide 4
    slide_four = slide4.Slide4(screen, overall_scoreboard.get_winner())
    slidewinner = slide_four.play()

# run
if __name__ == '__main__':
    main()
