

from os import truncate
from typing import Tuple
from pygame import Surface
import pygame
from pygame import time
from config import *
from color import *
from pygame import rect
import Debug


class Scene:

    def __init__(self, size:tuple, coord:tuple):
        self._scene_surface = Surface(size)
        self._scene_clock = time.Clock()
        self._shouldQuit = False
        self._sceneOver = False        

    def _process_input(self, keys):
        pass
    def _update_state(self):
        pass
    def _render_scene(self, window:Surface, dest:tuple):
        pass


class Splash_Scene(Scene):
    def __init__(self, size:tuple, coord:tuple = (0,0)):
        super().__init__(size, coord)
        self._splash_over = False
        self.LOGO_CURRENT_COLOR = LOGO_COLOR_1
        self.LOGO_FONT = pygame.font.Font("alba.super.ttf",75 )
        self.LOGO_TEXT = self.LOGO_FONT.render("PySnake", True, self.LOGO_CURRENT_COLOR)
        self.LOGO_RECT = self.LOGO_TEXT.get_rect()
        self.LOGO_RECT.topleft = (coord)       

    def _process_input(self, keys):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._shouldQuit = True
            if event.type == pygame.KEYUP:
                self._splash_over = True
    def _update_state(self) ->bool:
        if self._splash_over:
            return True
        if self._shouldQuit:
            quit()
        if self.LOGO_CURRENT_COLOR == LOGO_COLOR_1:
            self.LOGO_CURRENT_COLOR = LOGO_COLOR_2
        elif self.LOGO_CURRENT_COLOR == LOGO_COLOR_2: 
            self.LOGO_CURRENT_COLOR = LOGO_COLOR_3
        elif self.LOGO_CURRENT_COLOR == LOGO_COLOR_3:
            self.LOGO_CURRENT_COLOR = LOGO_COLOR_4
        elif self.LOGO_CURRENT_COLOR == LOGO_COLOR_4:
            self.LOGO_CURRENT_COLOR = LOGO_COLOR_5
        else:
            self.LOGO_CURRENT_COLOR = LOGO_COLOR_1
        return False

    def _render_scene(self, window:Surface):
        #pygame.draw.rect(self._scene_surface, self.LOGO_CURRENT_COLOR, self.LOGO_RECT, True)
        self.LOGO_TEXT = self.LOGO_FONT.render("PySnake", True, self.LOGO_CURRENT_COLOR)
        self._scene_surface.blit(self.LOGO_TEXT, self.LOGO_RECT)
        window.blit(self._scene_surface, (self.LOGO_RECT.center))
        pygame.display.flip()



class Play_Scene(Scene):
    def __init__(self, size:tuple, coord:tuple = (0,0)):
        super().__init__(size, coord)
        self._splash_over = False

        self.BG_WIDTH = int(WINDOW_WIDTH)
        self.BG_HEIGHT = self.BG_WIDTH

        self.self.CELLS_ACROSS = 21
        self.self.CELLS_DOWN = 21

        self.self.CELL_WIDTH = self.BG_WIDTH / self.self.CELLS_ACROSS
        self.self.CELL_HEIGHT = self.BG_HEIGHT / self.self.CELLS_DOWN

        self.GRID_self.CELL_WIDTH = .90 * self.self.CELL_WIDTH
        self.GRID_self.CELL_HEIGHT = .90 * self.self.CELL_HEIGHT


        self.self.GRID_CELL_OFFSET_X = .05 * self.self.CELL_WIDTH
        self.self.GRID_CELL_OFFSET_Y = .05 * self.self.CELL_HEIGHT

        self.PLAYER_CELL_OFFSET_X = .05 * self.self.CELL_WIDTH
        self.PLAYER_CELL_OFFSET_Y = .05 * self.self.CELL_HEIGHT

        self.PLAYER_WIDTH = .85 * self.self.CELL_WIDTH 
        self.PLAYER_HEIGHT = .8 * self.self.CELL_HEIGHT 

        self.DEFAULT_HEAD_COORD = [10,10]
        self.SCORE_FONT = pygame.font.SysFont("", 64)    

    def _process_input(self, keys):
        pass
    def _update_state(self) ->bool:
        pass
        
    def _render_scene(self, window:Surface):
        self.window.blit(self._GRID_LAYER, (0,0))
        self._drawSnake()
        if self.apple != None:
            if len(self.apple) > 0:
                self._drawApple()
            
        self._initScorePanel(self._SCORE_PANEL_LAYER)
        
        window.blit(self._SCORE_PANEL_LAYER, (0, self.BG_HEIGHT))
        self._score_text = self._SCORE_FONT.render("Points: {}".format(self._points), True, FADED_SCHOOLBUS)
        window.blit(self._score_text, self._score_text_rect)

        
        pygame.display.flip()

    def _initFilledBG(self, rgb, surface):
        rectColor = []
        if Debug.DEBUG_MODE_ON:
            rectColor = DB_GREEN
        else:
            rectColor = rgb

        #pygame.draw.rect(surface, rectColor, [0, 0, config.BG_WIDTH, config.BG_HEIGHT], 0)

    def _initGridOverlay(self,rgb, surface):
        rectColor = []
        if Debug.DEBUG_MODE_ON:
            rectColor = DB_SNOT
        else:
            rectColor = rgb

        for i in range(self.CELLS_ACROSS):
            for j in range(self.CELLS_DOWN):
                x = i * self.CELL_WIDTH
                y = j * self.self.CELL_HEIGHT
                pygame.draw.rect(surface, rectColor, [x + self.GRID_CELL_OFFSET_X, y + self.GRID_CELL_OFFSET_Y, self.GRID_CELL_WIDTH, self.GRID_self.CELL_HEIGHT], 0)

    def _drawSnake(self):
        rectColor = []
        if Debug.DEBUG_MODE_ON:
            rectColor = color.DB_BLUE
        else:
            rectColor = color.SALMON

        snakeCoords = self._snake.snake_coords()
        for i in range(len(snakeCoords)):
            pixPos = self._CoordToPixel(snakeCoords[i])            
            pygame.draw.rect(self._window, rectColor, [pixPos[0], pixPos[1], self.PLAYER_WIDTH, self.PLAYER_HEIGHT], 0)

    def _drawApple(self):
        rectColor = []
        if DEBUG_MODE_ON:
            rectColor = color.DB_ORANGE
        else:
            rectColor = color.FADED_SCHOOLBUS

        pixPos = self._CoordToPixel(self.apple)            
        pygame.draw.rect(self._window, rectColor, [pixPos[0], pixPos[1], self.GRID_self.CELL_WIDTH, self.GRID_self.CELL_HEIGHT], 0)

    def _spawnApple(self) -> list[int]:
        "Finds an open grid space at random and returns the coordinate"
        genAgain = True
        newCoord = None
        while genAgain:
            newCoord = self.Generate_Random_Coord()
            if newCoord in self._snake.snake_coords():
                genAgain = True
            else:
                genAgain = False
        return newCoord

    def _collectApple(self):
        "Consumes the current apple so to say and triggers a new spawn and a point increment"
        self._points += 10
        self.apple.clear()
        self.apple = None
        self._snake._toggleGrow()
        
    def _checkAppleCollision(self)->bool:
        if self.apple != None:
            if len(self.apple) > 0:
                for elem in self._snake.snake_coords():
                    if elem[0] == self.apple[0] and elem[1] == self.apple[1]:
                        return True
                
            return False

    def Generate_Random_Coord(self) -> list[int]:
        x = random.randint(0, self.CELLS_ACROSS-1)
        y = random.randint(0, self.CELLS_DOWN-1)
        return [x,y]
    