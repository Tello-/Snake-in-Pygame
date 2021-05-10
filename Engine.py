import pygame
from pygame import time
import config
from scene import Scene, Splash_Scene, Play_Scene, GameOver_Scene

class Snake_Engine:
    def __init__(self):
        
        self._window = pygame.display.set_mode((config.WINDOW_WIDTH, config.WINDOW_HEIGHT))
        self._clock = pygame.time.Clock()  
        

        self._currentScene = 0 #always first spot in scene queue
        self._scene_queue = [Scene((0,0),(0,0))]#[Splash_Scene((config.WINDOW_WIDTH, config.WINDOW_HEIGHT)), Play_Scene((config.WINDOW_WIDTH, config.WINDOW_HEIGHT))]
        self.Reset()
        self._uptime = int(0)
        
        self._timerBegun = False
        self._stateFinished = False
        self._isRunning = True

        self._JSON_String = ""
        
    def Reset(self):
        self._window.fill([0,0,0])
        if len(self._scene_queue) > 0:
            del self._scene_queue[:]
        self._scene_queue = [(Splash_Scene((config.WINDOW_WIDTH, config.WINDOW_HEIGHT))), (Play_Scene((config.WINDOW_WIDTH, config.WINDOW_HEIGHT))), (GameOver_Scene((config.WINDOW_WIDTH, config.WINDOW_HEIGHT)))]

        pygame.display.flip()
    
    def Run(self):
        self._clock.tick()        
        while self._isRunning:
            """Usually I'd write the physics and graphics clock to be separate from each other. Since this game is 
            fairly trivial I am just usuing the method provided by pygame to control the framerate of everything. That being said, 
            I have given each Scene(Game State) the ability to set its own frame speed in order to suit that scene best."""
            self._clock.tick(self._scene_queue[self._currentScene]._desired_frame_speed())
            if not self._isRunning:
                break

            self._uptime = time.get_ticks()

            self._scene_queue[self._currentScene]._process_input()            
            self._stateFinished = self._scene_queue[self._currentScene]._update_state()
            self._scene_queue[self._currentScene]._render_scene(self._window)

            if self._stateFinished:
                self._scene_queue.pop(self._currentScene)
                self._stateFinished = False
                if len(self._scene_queue) == 0:
                    self.Reset()      
