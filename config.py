
from typing import Text
import pygame
import os
from sys import platform
import random

random.seed()
pygame.init()

# Default Color Scheme
DARK_BLUE =  [20, 117, 135]
SALMON = [250, 126, 92]
OLD_SNOW = [243, 236, 229]
FADED_SCHOOLBUS = [254, 203, 95]
ZORA_SKIN = [99, 204, 200]

LOGO_COLOR_1 = [255,0,0]
LOGO_COLOR_2 = [255,175,0]
LOGO_COLOR_3 = [0,255,0]
LOGO_COLOR_4 = [0,255,175]
LOGO_COLOR_5 = [0,0,255]


USER_OS = None
CMD = None

if platform == "linux" or platform == "linux2":
    ''' linux'''
    USER_OS = "linux"
    CMD = "clear"
    font = pygame.font.SysFont("", 32)
    

elif platform == "win32":
    '''Windows...'''
    USER_OS = "win"
    CMD = "cls"
    font = pygame.font.SysFont("", 32)




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
LOGO_FONT = pygame.font.Font("alba.super.ttf",75 )



LOGO_TEXT = LOGO_FONT.render("PySnake", True, [255,0,0])
LOGO_RECT = LOGO_TEXT.get_rect()
LOGO_RECT.center = (WINDOW_WIDTH/2, WINDOW_HEIGHT * .20)
LOGO_CURRENT_COLOR = LOGO_COLOR_1


def Generate_Random_Coord() -> list[int]:
    x = random.randint(0, CELLS_ACROSS-1)
    y = random.randint(0, CELLS_DOWN-1)
    return [x,y]

# !!!!!!!!!!!!!!!!!!!!!!!!!!
DEBUG_MODE_ON = True            # SET TRUE TO ENABLE DEBUG MODE #
# !!!!!!!!!!!!!!!!!!!!!!!!!!


if DEBUG_MODE_ON:

    def convertMillis(millis):
     seconds=(millis/1000)%60
     minutes=(millis/(1000*60))%60
     hours=(millis/(1000*60*60))%24
     return hours, minutes, seconds

    # Debug Mode Color Scheme
    DB_GREEN =  [118,166,22]
    DB_BLUE = [31, 101, 242]
    DB_SNOT = [164, 242, 7]
    DB_ORANGE = [242, 65, 31]
    DB_BRICKRED = [166, 37, 13]

    DEBUG_MODE_MESG = Text("DEBUG MODE ON")


    DEBUG_SNAKE = [DEFAULT_HEAD_COORD, \
                [DEFAULT_HEAD_COORD[0] + 1, DEFAULT_HEAD_COORD[1]], \
                [DEFAULT_HEAD_COORD[0] + 2, DEFAULT_HEAD_COORD[1]], \
                [DEFAULT_HEAD_COORD[0] + 3, DEFAULT_HEAD_COORD[1]], \
                [DEFAULT_HEAD_COORD[0] + 4, DEFAULT_HEAD_COORD[1]], \
                [DEFAULT_HEAD_COORD[0] + 4, DEFAULT_HEAD_COORD[1]+1], \
                [DEFAULT_HEAD_COORD[0] + 4, DEFAULT_HEAD_COORD[1]+2] ]
    
            

    EVENT_CALL_COUNTER = int(0)
    
    
    
    
    def DB_CLEAR():
        os.system(CMD)

    text = font.render(DEBUG_MODE_MESG, True, DB_BRICKRED)
    textRect = text.get_rect()
    textRect.center = (WINDOW_WIDTH / 2,WINDOW_HEIGHT * .9)
    
    def DRAW_DEBUG_MSG(surf:pygame.Surface):
        surf.blit(text, textRect)
        pygame.display.update()

# :::::::::::::::: END DEBUG RELATED DECLARATIONS :::::::::::::::::::::::





