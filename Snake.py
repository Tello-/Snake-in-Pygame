import config

class snake:
    
    def __init__(self):
        
        if config.DEBUG_MODE_ON:
            self._snake = 
        else:
            self._snake = [config.DEFAULT_HEAD_COORD]

    def snake_coords(self) -> list[list[int]]:
        return self._snake