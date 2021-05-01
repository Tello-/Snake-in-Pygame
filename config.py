
from typing import Text
import pygame
import os
from sys import platform


pygame.init()

GAME_SPEED = 10
WINDOW_WIDTH = int(600)
WINDOW_HEIGHT = int(600)

CELLS_ACROSS = 20
CELLS_DOWN = 20

CELL_WIDTH = WINDOW_WIDTH / CELLS_ACROSS
CELL_HEIGHT = WINDOW_HEIGHT / CELLS_DOWN

GRID_CELL_WIDTH = .90 * CELL_WIDTH
GRID_CELL_HEIGHT = .90 * CELL_HEIGHT

GRID_CELL_OFFSET_X = .05 * CELL_WIDTH
GRID_CELL_OFFSET_Y = .05 * CELL_HEIGHT

PLAYER_CELL_OFFSET_X = .05 * CELL_WIDTH
PLAYER_CELL_OFFSET_Y = .05 * CELL_HEIGHT

PLAYER_WIDTH = .90 * CELL_WIDTH 
PLAYER_HEIGHT = .90 * CELL_HEIGHT 

DEFAULT_HEAD_COORD = (5,5)

# Default Color Scheme
DARK_BLUE =  [20, 117, 135]
SALMON = [250, 126, 92]
OLD_SNOW = [243, 236, 229]
FADED_SCHOOLBUS = [254, 203, 95]
ZORA_SKIN = [99, 204, 200]

DEBUG_MODE_ON = True
if DEBUG_MODE_ON:

    # Debug Mode Color Scheme
    DB_GREEN =  [118,166,22]
    DB_BLUE = [31, 101, 242]
    DB_LGREEN = [164, 242, 7]
    DB_ORANGE = [242, 65, 31]
    DB_BRICKRED = [166, 37, 13]

    DEBUG_MODE_MESG = Text("DEBUG MODE ON")



    USER_OS = None
    CMD = None

    if platform == "linux" or platform == "linux2":
        ''' linux'''
        USER_OS = "linux"
        CMD = "clear"
        

    elif platform == "win32":
        '''Windows...'''
        USER_OS = "win"
        CMD = "cls"
        font = pygame.font.SysFont("", 32)
            

    def DB_CLEAR():
        os.system(CMD)

    text = font.render(DEBUG_MODE_MESG, True, DB_BRICKRED)
    textRect = text.get_rect()
    textRect.center = (WINDOW_WIDTH / 2,WINDOW_HEIGHT * .9)
    
    def DRAW_DEBUG_MSG(surf:pygame.Surface):
        surf.blit(text, textRect)
        pygame.display.update()

# :::::::::::::::: END DEBUG RELATED DECLARATIONS :::::::::::::::::::::::





