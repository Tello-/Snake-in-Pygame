import pygame
from pygame import event
from pygame import time
import config
from enum import Enum

class Direction(Enum):
    NONE = 0,
    UP = 1,
    DOWN = 2,
    LEFT = 3,
    RIGHT = 4

TIMED_POINT_INCREASE = pygame.USEREVENT + 1
TIMED_POINT_INCREASE_EVENT = event.Event(TIMED_POINT_INCREASE)
time.set_timer(TIMED_POINT_INCREASE_EVENT, 3000) # Create custom event to be called every 3 seconds

class Snake_Engine:
    def __init__(self):
        self._window = pygame.display.set_mode((config.WINDOW_WIDTH, config.WINDOW_HEIGHT))
        self._clock = pygame.time.Clock()
        self._GRID_LAYER = pygame.Surface((config.WINDOW_WIDTH,config.WINDOW_HEIGHT))
        self._SNAKE_LAYER = pygame.Surface((config.PLAYER_WIDTH, config.PLAYER_HEIGHT))
        self.apple = [] # coord to hold where apple is at once it is known
        self._isRunning = True
        self._currentDir = Direction.NONE
        self._pendingGrowth = False
        self._hitDetected = False
        self._points = 0
        self.pointTimerExpired = False
        self._uptime = int(0)
        self._gameover = False

        pygame.event.Event
        
        if config.DEBUG_MODE_ON:
            self.snake = [config.DEFAULT_HEAD_COORD, \
                         (config.DEFAULT_HEAD_COORD[0] + 1, config.DEFAULT_HEAD_COORD[1]), \
                         (config.DEFAULT_HEAD_COORD[0] + 2, config.DEFAULT_HEAD_COORD[1]), \
                         (config.DEFAULT_HEAD_COORD[0] + 3, config.DEFAULT_HEAD_COORD[1]), \
                         (config.DEFAULT_HEAD_COORD[0] + 4, config.DEFAULT_HEAD_COORD[1]), \
                         (config.DEFAULT_HEAD_COORD[0] + 4, config.DEFAULT_HEAD_COORD[1]+1), \
                         (config.DEFAULT_HEAD_COORD[0] + 4, config.DEFAULT_HEAD_COORD[1]+2) ]
            self.pixelPos = []
        else:
            self.snake = [config.DEFAULT_HEAD_COORD]

    def Reset(self):
        pass
    def Run(self):
        self._clock.tick()
        self._drawFilledBG(config.ZORA_SKIN, self._GRID_LAYER)
        self._drawGridOverlay(config.DARK_BLUE, self._GRID_LAYER)
        self._drawSnake()
        pygame.display.flip()


        while not self._gameover:
            if not self._isRunning:
                break

            self._clock.tick(config.GAME_SPEED)
            self._uptime = time.get_ticks() 
            self._processevents()
            
            self._updateState()
            self._render()

            if config.DEBUG_MODE_ON:
                
                self._DB_CONSOLE_UPDATE()
        
        while self._gameover and self._isRunning:
            self._processevents()

        
    def _processevents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._isRunning = False
                break
            elif event.type == TIMED_POINT_INCREASE_EVENT.type:
                pointTimerExpired = True     
                    

            elif event.type == pygame.KEYDOWN:
                pressed = pygame.key.get_pressed()
                
                if pressed[pygame.K_ESCAPE]:
                    running = False

                keys = pygame.key.get_pressed()
                if keys[pygame.K_UP]:
                    self._UpPressed()
                elif keys[pygame.K_DOWN]:
                    self._DownPressed()
                elif keys[pygame.K_LEFT]:
                    self._LeftPressed()
                elif keys[pygame.K_RIGHT]:
                    self._RightPressed()
                elif keys[pygame.K_SPACE]:
                    if config.DEBUG_MODE_ON:
                        self._currentDir = Direction.NONE
                
    def _updateState(self):

        if self._isRunning:            

            selfHit = self._checkForBodyHit()

            if (self.snake[0][0] <= 0 and self._currentDir == Direction.LEFT) or \
            (self.snake[0][0] >= config.CELLS_ACROSS - 1 and self._currentDir == Direction.RIGHT) or \
            (self.snake[0][1] <= 0 and self._currentDir == Direction.UP) or \
            (self.snake[0][1] >= config.CELLS_DOWN -1 and self._currentDir == Direction.DOWN) or \
            (selfHit == True):

                self._hitDetected = True
            else:    
                if self._currentDir == Direction.UP:
                    self._MoveSnakeUp()
                elif self._currentDir == Direction.DOWN:
                    self._MoveSnakeDown()
                elif self._currentDir == Direction.LEFT:
                    self._MoveSnakeLeft()
                elif self._currentDir == Direction.RIGHT:
                    self._MoveSnakeRight()
                elif self._currentDir == Direction.NONE:
                    pass
            
            if self._hitDetected:
                time.set_timer(TIMED_POINT_INCREASE_EVENT, 0)
                self._gameover = True
            elif self.pointTimerExpired:
                config.EVENT_CALL_COUNTER += 1
                self._points += 1
                self.pointTimerExpired = False

    def _render(self):
        self._window.blit(self._GRID_LAYER, (0,0))
        self._drawSnake()
        pygame.display.flip()

    def _DB_CONSOLE_UPDATE(self):
        config.DB_CLEAR()
        print("pos: {} , {}".format(self.snake[0][0], self.snake[0][1]))
        self.pixelPos = self._CoordToPixel(self.snake[0]) 
        print("Pixel Pos: {}, {}".format(self.pixelPos[0], self.pixelPos[1]))
        print("len: {}".format(len(self.snake)))
        config.DRAW_DEBUG_MSG(self._window)
        print("Score Events Called: {}".format(config.EVENT_CALL_COUNTER))
        print("Points: {}".format(self._points))
        print("Hit Detected: {}".format(self._hitDetected))

        upt = config.convertMillis(self._uptime)
        
        
        print("Uptime: {}:{}:{}".format(int(upt[0]), int(upt[1]), int(upt[2])))

    def _drawFilledBG(self, rgb, surface):
        rectColor = []
        if config.DEBUG_MODE_ON:
            rectColor = config.DB_GREEN
        else:
            rectColor = rgb

        pygame.draw.rect(surface, rectColor, [0, 0, config.WINDOW_WIDTH, config.WINDOW_HEIGHT], 0)

    def _drawGridOverlay(self,rgb, surface):
        rectColor = []
        if config.DEBUG_MODE_ON:
            rectColor = config.DB_SNOT
        else:
            rectColor = rgb

        for i in range(config.CELLS_ACROSS):
            for j in range(config.CELLS_DOWN):
                x = i * config.CELL_WIDTH
                y = j * config.CELL_HEIGHT
                pygame.draw.rect(surface, rectColor, [x + config.GRID_CELL_OFFSET_X, y + config.GRID_CELL_OFFSET_Y, config.GRID_CELL_WIDTH, config.GRID_CELL_HEIGHT], 0)
    def _drawSnake(self):
        rectColor = []
        if config.DEBUG_MODE_ON:
            rectColor = config.DB_BLUE
        else:
            rectColor = config.SALMON

        for i in range(len(self.snake)):
            pixPos = self._CoordToPixel(self.snake[i])            
            pygame.draw.rect(self._window, rectColor, [pixPos[0], pixPos[1], config.PLAYER_WIDTH, config.PLAYER_HEIGHT], 0)
    def _CoordToPixel(self, coord):
        x = coord[0] * config.CELL_WIDTH
        y = coord[1] * config.CELL_HEIGHT
        return (x,y)
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
    def _MoveSnakeUp(self):
        self.snake.insert(0, (self.snake[0][0], self.snake[0][1] - 1))
        if self._pendingGrowth == False:
            self.snake.pop()
    def _MoveSnakeDown(self):
        self.snake.insert(0, (self.snake[0][0], self.snake[0][1] + 1))
        if self._pendingGrowth == False:
            self.snake.pop()
    def _MoveSnakeLeft(self):
        self.snake.insert(0, (self.snake[0][0] - 1, self.snake[0][1]))
        if self._pendingGrowth == False:
            self.snake.pop()
    def _MoveSnakeRight(self):
        self.snake.insert(0, (self.snake[0][0] + 1, self.snake[0][1]))
        if self._pendingGrowth == False:
            self.snake.pop()
    def _checkForBodyHit(self) -> bool:
        ''' Check if given list contains any duplicates '''
        if len(self.snake) == len(set(self.snake)):
            return False
        else:
            return True

    def _spawnApple(self):
        pass