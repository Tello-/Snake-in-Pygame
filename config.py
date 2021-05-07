
from typing import Text
import pygame

import random
from enum import Enum

from pygame.mixer import fadeout

import color

random.seed()
pygame.init()



GAME_SPEED = 10
WINDOW_WIDTH = int(600)
WINDOW_HEIGHT = int(700)

BG_WIDTH = int(WINDOW_WIDTH)
BG_HEIGHT = BG_WIDTH

CELLS_ACROSS = 21
CELLS_DOWN = 21

CELL_WIDTH = BG_WIDTH / CELLS_ACROSS
CELL_HEIGHT = BG_HEIGHT / CELLS_DOWN

GRID_CELL_WIDTH = .90 * CELL_WIDTH
GRID_CELL_HEIGHT = .90 * CELL_HEIGHT


GRID_CELL_OFFSET_X = .05 * CELL_WIDTH
GRID_CELL_OFFSET_Y = .05 * CELL_HEIGHT

PLAYER_CELL_OFFSET_X = .05 * CELL_WIDTH
PLAYER_CELL_OFFSET_Y = .05 * CELL_HEIGHT

PLAYER_WIDTH = .85 * CELL_WIDTH 
PLAYER_HEIGHT = .8 * CELL_HEIGHT 

DEFAULT_HEAD_COORD = [10,10]
SCORE_FONT = pygame.font.SysFont("", 64)



def Generate_Random_Coord() -> list[int]:
    x = random.randint(0, CELLS_ACROSS-1)
    y = random.randint(0, CELLS_DOWN-1)
    return [x,y]




# !!!!!!!!!!!!!!!!!!!!!!!!!!
DEBUG_MODE_ON = False            # SET TRUE TO ENABLE DEBUG MODE #
# !!!!!!!!!!!!!!!!!!!!!!!!!!








