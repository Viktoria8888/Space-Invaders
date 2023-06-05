import pygame
from pygame.locals import *
import operator
import sys
from Labels import Label
from Button import Button
import random
import math
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800

SPEED = 20 # ships's walking speed
def AddVectors(v1,v2):
    return list(map(operator.add,v1,v2))

DIRECTIONS = {
    "UP": [0, -10],
    "DOWN": [0, 0.5],
    "RIGHT" : [0.75, 0],
    "LEFT" : [-0.75, 0]
}
