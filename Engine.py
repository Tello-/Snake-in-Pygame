import pygame
from pygame import event
from pygame import time
import config
from enum import Enum
from direction import Direction
from snake import Snake
import color
from scene import Scene, Splash_Scene

if config.DEBUG_MODE_ON:
    import Debug




class Snake_Engine:
    def __init__(self):
        
        self._window = pygame.display.set_mode((config.WINDOW_WIDTH, config.WINDOW_HEIGHT))
        self._clock = pygame.time.Clock()
        
        self._GRID_LAYER = pygame.Surface((config.BG_WIDTH,config.BG_HEIGHT))
        self._SNAKE_LAYER = pygame.Surface((config.PLAYER_WIDTH, config.PLAYER_HEIGHT))
        self._SCORE_PANEL_LAYER = pygame.Surface((config.WINDOW_WIDTH, config.BG_HEIGHT ))
        self._SPLASH_LAYER = pygame.Surface((config.WINDOW_WIDTH, config.WINDOW_HEIGHT))
        
        self._currentScene = Splash_Scene((config.WINDOW_WIDTH, config.WINDOW_HEIGHT),(0,0))

        #self._snake = Snake()
        #self.apple = None # coord to hold where apple is at once it is known
        
        self._TIMED_POINT_INCREASE = pygame.USEREVENT + 1
        self._TIMED_POINT_INCREASE_EVENT = event.Event(self._TIMED_POINT_INCREASE)
        self._pointTimerExpired = False

        """self._currentDir = Direction.NONE

        self._pendingGrowth = False
        self._hitDetected = False

        self._points = 0
        
        self._uptime = int(0)
"""
        self._gameover = False
        
        self._isRunning = True
        self._hasBegun = False
        self._timerBegun = False
        self._stateFinished = False
        
        """self._score_text = config.SCORE_FONT.render("Points: {}".format(self._points), True, color.FADED_SCHOOLBUS)
        self._score_text_rect = self._score_text.get_rect()
        self._score_text_rect.topleft = (config.WINDOW_WIDTH * .05, config.WINDOW_HEIGHT * .90)"""
        
    def Reset(self):
        pass
    
    
    
    def Run(self):
        self._clock.tick()
        
        #The following 2 declarations initialize the surface named GRID_LAYER
        """self._initFilledBG(color.ZORA_SKIN, self._GRID_LAYER)
        self._initGridOverlay(color.DARK_BLUE, self._GRID_LAYER)"""

        
        while not self._gameover:
            self._clock.tick(config.GAME_SPEED)
            if not self._isRunning:
                break

            self._uptime = time.get_ticks()

            self._currentScene._process_input(None)
            self._stateFinished = self._currentScene._update_state()
            self._currentScene._render_scene(self._window)

            if config.DEBUG_MODE_ON:                
                Debug._DB_CONSOLE_UPDATE(self)
        
        """while self._gameover and self._isRunning:
            #This is where I could restart the game or reset the gamestate to start over
            self._processevents()"""
     
   # def _processevents(self):

        


        

        

    """ def _updateState(self):
        if not self._waitingOnSplash:
            if self._isRunning:            
                
                if self.apple == None:
                    self.apple = self._spawnApple()

                if self._checkAppleCollision():
                    self._collectApple()

                selfHit = self._checkForSelfBodyHit()

                if (self._snake.snake_coords()[0][0] <= 0 and self._currentDir == Direction.LEFT) or \
                (self._snake.snake_coords()[0][0] >= config.CELLS_ACROSS - 1 and self._currentDir == Direction.RIGHT) or \
                (self._snake.snake_coords()[0][1] <= 0 and self._currentDir == Direction.UP) or \
                (self._snake.snake_coords()[0][1] >= config.CELLS_DOWN -1 and self._currentDir == Direction.DOWN) or \
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
                    self._gameover = True
                
                if self._pointTimerExpired and not self._hitDetected:
                    if config.DEBUG_MODE_ON:
                        Debug.EVENT_CALL_COUNTER += 1
                    
                    self._points += 1
                    self._pointTimerExpired = False

    def _render(self):
        if self._waitingOnSplash:
            self._initSplash(self._SPLASH_LAYER)
            self._window.blit(self._SPLASH_LAYER, (0,0))            
            pygame.display.flip()
        else:
            self._window.blit(self._GRID_LAYER, (0,0))
            self._drawSnake()
            if self.apple != None:
                if len(self.apple) > 0:
                    self._drawApple()
            
            self._initScorePanel(self._SCORE_PANEL_LAYER)
            
            self._window.blit(self._SCORE_PANEL_LAYER, (0, config.BG_HEIGHT))
            self._score_text = config.SCORE_FONT.render("Points: {}".format(self._points), True, color.FADED_SCHOOLBUS)
            self._window.blit(self._score_text, self._score_text_rect)

            
            pygame.display.flip()

    

    def _initFilledBG(self, rgb, surface):
        rectColor = []
        if config.DEBUG_MODE_ON:
            rectColor = color.DB_GREEN
        else:
            rectColor = rgb

        pygame.draw.rect(surface, rectColor, [0, 0, config.BG_WIDTH, config.BG_HEIGHT], 0)

    def _initGridOverlay(self,rgb, surface):
        rectColor = []
        if config.DEBUG_MODE_ON:
            rectColor = color.DB_SNOT
        else:
            rectColor = rgb

        for i in range(config.CELLS_ACROSS):
            for j in range(config.CELLS_DOWN):
                x = i * config.CELL_WIDTH
                y = j * config.CELL_HEIGHT
                pygame.draw.rect(surface, rectColor, [x + config.GRID_CELL_OFFSET_X, y + config.GRID_CELL_OFFSET_Y, config.GRID_CELL_WIDTH, config.GRID_CELL_HEIGHT], 0)

    def _initSplash(self,surface):
        

        pygame.draw.rect(surface, config.LOGO_CURRENT_COLOR, [0, 0, config.WINDOW_WIDTH, config.WINDOW_HEIGHT], True)
        surface.blit(config.LOGO_TEXT, config.LOGO_RECT)
        
         

    def _initScorePanel(self, surface):
        pygame.draw.rect(surface, color.DARK_BLUE, [0, 0, config.WINDOW_WIDTH, config.WINDOW_HEIGHT - config.BG_HEIGHT])

    def _drawSnake(self):
        rectColor = []
        if config.DEBUG_MODE_ON:
            rectColor = color.DB_BLUE
        else:
            rectColor = color.SALMON

        snakeCoords = self._snake.snake_coords()
        for i in range(len(snakeCoords)):
            pixPos = self._CoordToPixel(snakeCoords[i])            
            pygame.draw.rect(self._window, rectColor, [pixPos[0], pixPos[1], config.PLAYER_WIDTH, config.PLAYER_HEIGHT], 0)

    def _drawApple(self):
        rectColor = []
        if config.DEBUG_MODE_ON:
            rectColor = color.DB_ORANGE
        else:
            rectColor = color.FADED_SCHOOLBUS

        pixPos = self._CoordToPixel(self.apple)            
        pygame.draw.rect(self._window, rectColor, [pixPos[0], pixPos[1], config.GRID_CELL_WIDTH, config.GRID_CELL_HEIGHT], 0)

    def _CoordToPixel(self, coord:list[int]):
        x = coord[0] * config.CELL_WIDTH
        y = coord[1] * config.CELL_HEIGHT
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

    def _spawnApple(self) -> list[int]:
        "Finds an open grid space at random and returns the coordinate"
        genAgain = True
        newCoord = None
        while genAgain:
            newCoord = config.Generate_Random_Coord()
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

  
    def _splashScreen(self):
        
        self._processevents()
        self._updateState()
        self._render() """

