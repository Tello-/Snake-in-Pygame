import pygame
from pygame import event
from pygame import time
import config
from enum import Enum
from direction import Direction
from snake import Snake
import color
from scene import Splash_Scene, Play_Scene

class Snake_Engine:
    def __init__(self):
        
        self._window = pygame.display.set_mode((config.WINDOW_WIDTH, config.WINDOW_HEIGHT))
        self._clock = pygame.time.Clock()  
        self._TIMED_POINT_INCREASE = pygame.USEREVENT + 1
        self._TIMED_POINT_INCREASE_EVENT = event.Event(self._TIMED_POINT_INCREASE)
        self._pointTimerExpired = False

        self._currentScene = 0 #always first spot in scene queue
        self._scene_queue = [Splash_Scene((config.WINDOW_WIDTH, config.WINDOW_HEIGHT)), Play_Scene((config.WINDOW_WIDTH, config.WINDOW_HEIGHT))]
        
        self._uptime = int(0)
        self._gameover = False
        
        self._isRunning = True
        self._hasBegun = False
        self._timerBegun = False
        self._stateFinished = False
        
        
    def Reset(self):
        pass
    
    def Run(self):
        self._clock.tick()        
        while not self._gameover:
            self._clock.tick(config.GAME_SPEED)
            if not self._isRunning:
                break

            self._uptime = time.get_ticks()

            self._scene_queue[self._currentScene]._process_input(None)
            self._stateFinished = self._scene_queue[self._currentScene]._update_state()
            self._scene_queue[self._currentScene]._render_scene(self._window)

            if self._stateFinished:
                self._scene_queue.pop(self._currentScene)
                self._stateFinished = False        
