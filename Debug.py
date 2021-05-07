import config
import os
from sys import platform
from typing import Text
import pygame


USER_OS = None
CMD = None

if platform == "linux" or platform == "linux2":
    ''' linux'''
    USER_OS = "linux"
    CMD = "clear"
    font = pygame.font.SysFont("", 32)
    

elif platform == "win32":
    '''Windows...'''
    USER_OS = "win"
    CMD = "cls"
    font = pygame.font.SysFont("", 32)

    def convertMillis(millis):
     seconds=(millis/1000)%60
     minutes=(millis/(1000*60))%60
     hours=(millis/(1000*60*60))%24
     return hours, minutes, seconds

    # Debug Mode Color Scheme
    DB_GREEN =  [118,166,22]
    DB_BLUE = [31, 101, 242]
    DB_SNOT = [164, 242, 7]
    DB_ORANGE = [242, 65, 31]
    DB_BRICKRED = [166, 37, 13]

    DEBUG_MODE_MESG = Text("DEBUG MODE ON")


    DEBUG_SNAKE = [config.DEFAULT_HEAD_COORD, \
                [config.DEFAULT_HEAD_COORD[0] + 1, config.DEFAULT_HEAD_COORD[1]], \
                [config.DEFAULT_HEAD_COORD[0] + 2, config.DEFAULT_HEAD_COORD[1]], \
                [config.DEFAULT_HEAD_COORD[0] + 3, config.DEFAULT_HEAD_COORD[1]], \
                [config.DEFAULT_HEAD_COORD[0] + 4, config.DEFAULT_HEAD_COORD[1]], \
                [config.DEFAULT_HEAD_COORD[0] + 4, config.DEFAULT_HEAD_COORD[1]+1], \
                [config.DEFAULT_HEAD_COORD[0] + 4, config.DEFAULT_HEAD_COORD[1]+2] ]
    
            

    EVENT_CALL_COUNTER = int(0)
    
    
    
    
    def DB_CLEAR():
        os.system(CMD)

    text = font.render(DEBUG_MODE_MESG, True, DB_BRICKRED)
    textRect = text.get_rect()
    textRect.center = (config.WINDOW_WIDTH / 2,config.WINDOW_HEIGHT * .9)
    
    def DRAW_DEBUG_MSG(surf:pygame.Surface):
        surf.blit(text, textRect)
        pygame.display.update()



def _DB_CONSOLE_UPDATE(self):
        DB_CLEAR()
        print("pos: {} , {}".format(self._snake.snake_coords()[0][0], self._snake.snake_coords()[0][1]))
        self.pixelPos = self._CoordToPixel(self._snake.snake_coords()[0]) 
        print("Pixel Pos: {}".format(self._CoordToPixel(self._snake.snake_coords()[0])))
        print("len: {}".format(len(self._snake.snake_coords())))
        DRAW_DEBUG_MSG(self._window)
        print("Score Events Called: {}".format(EVENT_CALL_COUNTER))
        print("Points: {}".format(self._points))
        print("Hit Detected: {}".format(self._hitDetected))
        if self.apple != None:
            if len(self.apple) > 0:
                print("Apple Coord: {},{}".format(self.apple[0], self.apple[1]))
        print("Pending Growth?: {}".format(self._snake._pending_Growth))

        upt = convertMillis(self._uptime)        
        print("Uptime: {}:{}:{}".format(int(upt[0]), int(upt[1]), int(upt[2])))