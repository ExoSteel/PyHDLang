import pygame as pg
from pygame.locals import *

info = pg.display.Info()
worldWidth = info.current_w // 2
worldHeight = info.current_h // 2

win = pg.display.set_mode((worldWidth,worldHeight), RESIZABLE)

ALPHABET = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]

RED = (150,25,25)
GREEN = (25,150,25)
BLUE = (25,25,150)
WHITE = (200,200,200)
BLACK = (0,0,0)

BACKGROUND = (25,25,25)
BACKGROUND2 = (12,12,12)
BACKGROUND3 = (50,50,50)
BACKGROUND4 = (100,100,100)