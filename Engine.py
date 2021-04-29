import pygame
import config

class Snake_Engine:
    def __init__(self):
        self._window = pygame.display.set_mode((config.WINDOW_WIDTH, config.WINDOW_HEIGHT))
        self._clock = pygame.time.Clock()
        self._GRID_LAYER = pygame.Surface((config.WINDOW_WIDTH,config.WINDOW_HEIGHT))
        self._SNAKE_LAYER = pygame.Surface((config.PLAYER_WIDTH, config.PLAYER_HEIGHT))
        self.snake = [config.DEFAULT_HEAD_COORD, (config.DEFAULT_HEAD_COORD[0] + 1, config.DEFAULT_HEAD_COORD[1]),(config.DEFAULT_HEAD_COORD[0] + 2, config.DEFAULT_HEAD_COORD[1]) ]
    
    def Reset(self):
        pass

    def Run(self):
        self._drawFilledBG(config.ZORA_SKIN, self._GRID_LAYER)
        self._drawGridOverlay(config.DARK_BLUE, self._GRID_LAYER)
        self._drawSnake()

        pygame.display.flip()
        running=True


        while running:
            self._clock.tick(60)
            # Did the user click the window close button?
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    pressed = pygame.key.get_pressed()
                    if pressed[pygame.K_UP]:
                        self._UpPressed()
                    if pressed[pygame.K_DOWN]:
                        self._DownPressed()
                    if pressed[pygame.K_LEFT]:
                        self._LeftPressed()
                    if pressed[pygame.K_RIGHT]:
                        self._RightPressed()
                    if pressed[pygame.K_ESCAPE]:
                        running = False

            
            self._window.blit(self._GRID_LAYER, (0,0))
            self._drawSnake()
            
            
                
            #self._window.blits(self._SNAKE_LAYER, self._snake)

            # Flip the display
            pygame.display.flip()
        pygame.quit()

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
            pygame.draw.rect(self._window, config.SALMON, [(self.snake[i])[0] * config.CELL_WIDTH, (self.snake[i])[1] * config.CELL_HEIGHT, config.PLAYER_WIDTH, config.PLAYER_HEIGHT], 0)

    def _UpPressed(self):
        pass
    def _DownPressed(self):
        pass
    def _LeftPressed(self):
        pass
    def _RightPressed(self):
        pass