import pygame
import config
from enum import Enum

class Direction(Enum):
    NONE = 0,
    UP = 1,
    DOWN = 2,
    LEFT = 3,
    RIGHT = 4


class Snake_Engine:
    def __init__(self):
        self._window = pygame.display.set_mode((config.WINDOW_WIDTH, config.WINDOW_HEIGHT))
        self._clock = pygame.time.Clock()
        self._GRID_LAYER = pygame.Surface((config.WINDOW_WIDTH,config.WINDOW_HEIGHT))
        self._SNAKE_LAYER = pygame.Surface((config.PLAYER_WIDTH, config.PLAYER_HEIGHT))
        self.snake = [config.DEFAULT_HEAD_COORD, (config.DEFAULT_HEAD_COORD[0] + 1, config.DEFAULT_HEAD_COORD[1]),(config.DEFAULT_HEAD_COORD[0] + 2, config.DEFAULT_HEAD_COORD[1]) ]
        self._isRunning = True
        self._currentDir = Direction.NONE
        self._pendingGrowth = False
        self._hitDetected = False
    def Reset(self):
        pass
    def Run(self):
        self._drawFilledBG(config.ZORA_SKIN, self._GRID_LAYER)
        self._drawGridOverlay(config.DARK_BLUE, self._GRID_LAYER)
        self._drawSnake()
        

        pygame.display.flip()


        while self._isRunning:
            self._clock.tick(config.GAME_SPEED)
            self._processevents()
            print("{} , {}".format(self.snake[0][0], self.snake[0][1]))
            self._updateState()
            self._render()
            
        pygame.quit()
    def _processevents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._isRunning = False
            elif event.type == pygame.KEYDOWN:
                pressed = pygame.key.get_pressed()
                if pressed[pygame.K_UP]:
                    self._UpPressed()
                elif pressed[pygame.K_DOWN]:
                    self._DownPressed()
                elif pressed[pygame.K_LEFT]:
                    self._LeftPressed()
                elif pressed[pygame.K_RIGHT]:
                    self._RightPressed()
                elif pressed[pygame.K_ESCAPE]:
                    running = False
    def _updateState(self):

        selfHit = False
        #TODO fix this logic for finding a self hit
        for ele in self.snake:
            if ele > 0 and self.snake[0] == self.snake[ele]:
                selfHit = True 
                break

        if (self.snake[0][0] < 0) or \
        (self.snake[0][0] >= config.CELLS_ACROSS - 1) or \
        (self.snake[0][1] < 0) or \
        (self.snake[0][1] >= config.CELLS_DOWN -1) or \
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
    def _render(self):
        self._window.blit(self._GRID_LAYER, (0,0))
        self._drawSnake()
        pygame.display.flip()
    def _drawFilledBG(self, rgb, surface):
        pygame.draw.rect(surface, rgb, [0, 0, config.WINDOW_WIDTH, config.WINDOW_HEIGHT], 0)
    def _drawGridOverlay(self,rgb, surface):
        for i in range(config.CELLS_ACROSS):
            for j in range(config.CELLS_DOWN):
                x = i * config.CELL_WIDTH
                y = j * config.CELL_HEIGHT
                pygame.draw.rect(surface, rgb, [x + config.GRID_CELL_OFFSET_X, y + config.GRID_CELL_OFFSET_Y, config.GRID_CELL_WIDTH, config.GRID_CELL_HEIGHT], 0)
    def _drawSnake(self):
        for i in range(len(self.snake)):
            pixPos = self._CoordToPixel(self.snake[i])            
            pygame.draw.rect(self._window, config.SALMON, [pixPos[0], pixPos[1], config.PLAYER_WIDTH, config.PLAYER_HEIGHT], 0)
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
        