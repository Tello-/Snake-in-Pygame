

import os

import pygame
from pygame import Surface, surface

from pygame import time
from config import *
from color import *
from direction import Direction
import snake
from pygame.event import Event
from color import Color_Scheme


class Scene:

    def __init__(self, size:tuple, coord:tuple):
        self._scene_surface = Surface(size)
        self._scene_clock = time.Clock()
        self._shouldQuit = False
        self._sceneOver = False        

    def _process_input(self):
        pass
    def _update_state(self)->bool:
        pass
    def _render_scene(self, window:Surface, dest:tuple):
        pass
    def _end_scene(self):
        pass
    def _desired_frame_speed(self) -> int:
        pass


class Splash_Scene(Scene):
    def __init__(self, size:tuple, coord:tuple = (0,0)):
        super().__init__(size, coord)
        self._splash_over = False
        self.LOGO_CURRENT_COLOR = 1 # COLOR 1
        dirname = os.path.dirname(__file__)
        logoFontFileName = os.path.join(dirname, 'alba.super.ttf')
        self.LOGO_FONT = pygame.font.Font(logoFontFileName,100 )
        self.CONTROL_FONT = pygame.font.Font(logoFontFileName, 35)
        self.ANYKEY_FONT = pygame.font.Font(logoFontFileName, 25)
        self.LOGO_TEXT = self.LOGO_FONT.render("PySnake", True, LOGO_COLORS[self.LOGO_CURRENT_COLOR])
        self.LOGO_RECT = pygame.Rect(55,20, 0, 0)
        #self.LOGO_RECT.center = (0,0)

        self.CONTROL_TEXT = self.CONTROL_FONT.render("Turn Snake : Arrows", True, [255,255,255] )
        self.CONTROL_RECT = pygame.Rect(80,300, 0, 0)
        #self.CONTROL_RECT.topleft = (0, WINDOW_HEIGHT * .50)

        self.ANYKEY_TEXT = self.ANYKEY_FONT.render("Any key to continue...", True, [255,255,255] )
        self.ANYKEY_RECT = pygame.Rect(120,500, 0, 0)
        #self.ANYKEY_RECT.topleft = (15, WINDOW_HEIGHT * .65)


        self.FRAME_SPEED = 8
        


    def _desired_frame_speed(self) -> int:
        return self.FRAME_SPEED

    def _process_input(self):
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
        
        if self.LOGO_CURRENT_COLOR != len(LOGO_COLORS):
            self.LOGO_CURRENT_COLOR += 1
        
        if self.LOGO_CURRENT_COLOR == len(LOGO_COLORS):
            self.LOGO_CURRENT_COLOR = 1
        return False

    def _render_scene(self, window:Surface):
        #pygame.draw.rect(self._scene_surface, self.LOGO_CURRENT_COLOR, self.LOGO_RECT, True)
        self.LOGO_TEXT = self.LOGO_FONT.render("PySnake", True, LOGO_COLORS[self.LOGO_CURRENT_COLOR])
        self._scene_surface.blit(self.LOGO_TEXT, self.LOGO_RECT)
        self._scene_surface.blit(self.CONTROL_TEXT, self.CONTROL_RECT)
        self._scene_surface.blit(self.ANYKEY_TEXT, self.ANYKEY_RECT)
        window.blit(self._scene_surface, (self.LOGO_RECT.center))
        pygame.display.flip()



class Play_Scene(Scene):
    def __init__(self, size:tuple, coord:tuple = (0,0)):
        super().__init__(size, coord)
        self._play_over = False

        self._TIMED_POINT_INCREASE = pygame.USEREVENT + 1
        self._TIMED_POINT_INCREASE_EVENT = Event(self._TIMED_POINT_INCREASE)
        self._pointTimerExpired = False
        

        self.BG_WIDTH = int(WINDOW_WIDTH)
        self.BG_HEIGHT = self.BG_WIDTH
        self.CELLS_ACROSS = 21
        self.CELLS_DOWN = 21
        self.CELL_WIDTH = self.BG_WIDTH / self.CELLS_ACROSS
        self.CELL_HEIGHT = self.BG_HEIGHT / self.CELLS_DOWN
        self.GRID_CELL_WIDTH = .90 * self.CELL_WIDTH
        self.GRID_CELL_HEIGHT = .90 * self.CELL_HEIGHT
        self.GRID_CELL_OFFSET_X = .05 * self.CELL_WIDTH
        self.GRID_CELL_OFFSET_Y = .05 * self.CELL_HEIGHT
        self.PLAYER_CELL_OFFSET_X = .05 * self.CELL_WIDTH
        self.PLAYER_CELL_OFFSET_Y = .05 * self.CELL_HEIGHT
        self.PLAYER_WIDTH = .85 * self.CELL_WIDTH 
        self.PLAYER_HEIGHT = .8 * self.CELL_HEIGHT

        self.DEFAULT_HEAD_COORD = [10,10]
        self.SCORE_FONT = pygame.font.SysFont("", 64)
        

        self._points = 0
        self._score_text = self.SCORE_FONT.render("Points: {}".format(self._points), True, FADED_SCHOOLBUS)
        self._score_text_rect = self._score_text.get_rect()
        self._score_text_rect.topleft = (WINDOW_WIDTH * .05, WINDOW_HEIGHT * .90)
        

        self._GRID_LAYER = pygame.Surface((self.BG_WIDTH,self.BG_HEIGHT))
        self._SNAKE_LAYER = pygame.Surface((self.PLAYER_WIDTH, self.PLAYER_HEIGHT))
        self._SCORE_PANEL_LAYER = pygame.Surface((WINDOW_WIDTH, self.BG_HEIGHT ))

        self._snake = snake.Snake(self.DEFAULT_HEAD_COORD)
        self._currentDir = Direction.NONE
        self._pendingGrowth = False
        self._hitDetected = False
        
        self._points = 0
        
        self.apple = None # coord to hold where apple is at once it is known


        self._gameover = False        
        self._isRunning = True
        self._hasBegun = False
        self._timerBegun = False

        self.FRAME_SPEED = 10

        self._initFilledBG(BG_COLOR, self._GRID_LAYER)
        self._initGridOverlay(FG_COLOR, self._GRID_LAYER)

        
    def _desired_frame_speed(self) -> int:
        return self.FRAME_SPEED
    def _process_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._shouldQuit = True
                quit() # for now for debugging purposes
            if event.type == self._TIMED_POINT_INCREASE_EVENT.type:
                self._pointTimerExpired = True

        keys = pygame.key.get_pressed()
            
        # The extra conditional logic is to combat a glitch that allows you to do a 180 via multi key processing between frames
        if keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT] and not keys[pygame.K_UP] and not keys[pygame.K_DOWN]:
            self._LeftPressed()
            if not self._hasBegun:
                self._hasBegun = True
        if keys[pygame.K_RIGHT] and not keys[pygame.K_LEFT] and not keys[pygame.K_UP] and not keys[pygame.K_DOWN]:
            self._RightPressed()
            if not self._hasBegun:
                self._hasBegun = True
        if keys[pygame.K_UP] and not keys[pygame.K_RIGHT] and not keys[pygame.K_LEFT] and not keys[pygame.K_DOWN]:
            self._UpPressed()
            if not self._hasBegun:
                self._hasBegun = True
        if keys[pygame.K_DOWN] and not keys[pygame.K_RIGHT] and not keys[pygame.K_UP] and not keys[pygame.K_LEFT]:
            self._DownPressed()
            if not self._hasBegun:
                self._hasBegun = True
            
    def _update_state(self) ->bool:
        if self._hasBegun and not self._timerBegun:
            self._timerBegun = True
            time.set_timer(self._TIMED_POINT_INCREASE_EVENT, 3000)   
        if self.apple == None:
            self.apple = self._spawnApple()

        if self._checkAppleCollision():
            self._collectApple()

        selfHit = self._snakeSelfCollide()

        if (self._snake.snake_coords()[0][0] <= 0 and self._currentDir == Direction.LEFT) or \
        (self._snake.snake_coords()[0][0] >= self.CELLS_ACROSS - 1 and self._currentDir == Direction.RIGHT) or \
        (self._snake.snake_coords()[0][1] <= 0 and self._currentDir == Direction.UP) or \
        (self._snake.snake_coords()[0][1] >= self.CELLS_DOWN -1 and self._currentDir == Direction.DOWN) or \
        (selfHit == True):

            self._hitDetected = True
        else:    
            if self._currentDir == Direction.UP:
                self._snake.move(Direction.UP)
            elif self._currentDir == Direction.DOWN:
                self._snake.move(Direction.DOWN)
            elif self._currentDir == Direction.LEFT:
                self._snake.move(Direction.LEFT)
            elif self._currentDir == Direction.RIGHT:
                self._snake.move(Direction.RIGHT)
            elif self._currentDir == Direction.NONE:
                pass
        
        if self._hitDetected:
            time.set_timer(self._TIMED_POINT_INCREASE_EVENT, 0)
            return True
        
        if self._pointTimerExpired and not self._hitDetected:                
            self._points += 1
            self._pointTimerExpired = False
        
        return False # "state not done"
        
    def _render_scene(self, window:Surface):
        window.blit(self._GRID_LAYER, (0,0))
        self._drawSnake(window)
        if self.apple != None:
            if len(self.apple) > 0:
                self._drawApple(window)
            
        self._initScorePanel(self._SCORE_PANEL_LAYER)        
        window.blit(self._SCORE_PANEL_LAYER, (0, self.BG_HEIGHT))        
        window.blit(self._score_text, self._score_text_rect)

        
        pygame.display.flip()

    def _end_scene(self):
        pass
    def _initFilledBG(self, rgb, surface):
        rectColor = []
        
        rectColor = rgb

        pygame.draw.rect(surface, rectColor, [0, 0, self.BG_WIDTH, self.BG_HEIGHT], 0)

    def _initGridOverlay(self,rgb, surface):
        rectColor = []
        rectColor = rgb

        for i in range(self.CELLS_ACROSS):
            for j in range(self.CELLS_DOWN):
                x = i * self.CELL_WIDTH
                y = j * self.CELL_HEIGHT
                pygame.draw.rect(surface, rectColor, [x + self.GRID_CELL_OFFSET_X, y + self.GRID_CELL_OFFSET_Y, self.GRID_CELL_WIDTH, self.GRID_CELL_HEIGHT], 0)
    def _initScorePanel(self, surface):
        pygame.draw.rect(surface, SCORE_PANEL_COLOR, [0, 0, WINDOW_WIDTH, WINDOW_HEIGHT - self.BG_HEIGHT])
        self._score_text = self.SCORE_FONT.render("Points: {}".format(self._points), True, FADED_SCHOOLBUS)
    def _drawSnake(self, window:surface):
        snakeCoords = self._snake.snake_coords()
        for i in range(len(snakeCoords)):
            pixPos = self._CoordToPixel(snakeCoords[i])            
            pygame.draw.rect(window, SNAKE_COLOR, [pixPos[0], pixPos[1], self.PLAYER_WIDTH, self.PLAYER_HEIGHT], 0)

    def _drawApple(self, window:surface):
        

        pixPos = self._CoordToPixel(self.apple)            
        pygame.draw.rect(window, APPLE_COLOR, [pixPos[0], pixPos[1], self.PLAYER_WIDTH, self.PLAYER_HEIGHT], 0)

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
    
    def _CoordToPixel(self, coord:list[int]):
        x = coord[0] * self.CELL_WIDTH
        y = coord[1] * self.CELL_HEIGHT
        return [x,y]

    def _UpPressed(self):
        if self._currentDir != Direction.DOWN:
            self._currentDir = Direction.UP
    def _DownPressed(self):
        if self._currentDir != Direction.UP:
            self._currentDir = Direction.DOWN
    def _LeftPressed(self):
        if self._currentDir != Direction.RIGHT:
            self._currentDir = Direction.LEFT
    def _RightPressed(self):
       if self._currentDir != Direction.LEFT:
            self._currentDir = Direction.RIGHT

    def _snakeSelfCollide(self) -> bool:
        ''' Check if given list contains any duplicates '''
        snakeCoords = self._snake.snake_coords()
        if len(snakeCoords) >= 5:
            i = 1
            while i < len(snakeCoords):
                if snakeCoords[0][0] == snakeCoords[i][0] and snakeCoords[0][1] == snakeCoords[i][1]:
                    return True                
                i += 1
            return False