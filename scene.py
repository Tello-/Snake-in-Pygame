

from os import truncate
from typing import Tuple
from pygame import Surface
import pygame
from pygame import time
from config import GAME_SPEED
from config import WINDOW_WIDTH,WINDOW_HEIGHT
from color import LOGO_COLOR_1,LOGO_COLOR_2,LOGO_COLOR_3,LOGO_COLOR_4,LOGO_COLOR_5
from pygame import rect


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

    def _process_input(self, keys):
        pass
    def _update_state(self) ->bool:
        pass
        
    def _render_scene(self, window:Surface):
        pass
