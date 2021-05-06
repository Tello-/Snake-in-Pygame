import config
from direction import Direction

class Snake:
    
    def __init__(self):
        self._HEAD_IDX = 0
        self._curr_dir = None
        if config.DEBUG_MODE_ON:
            self._snake = config.DEBUG_SNAKE
        else:
            self._snake = [config.DEFAULT_HEAD_COORD]

    def snake_coords(self) -> list[list[int]]:
        return self._snake
    
    def __len__(self) -> int:
        return len(self._snake)

    def move(self, dir:Direction) -> bool:
        
        curr = self._curr_dir
        if dir == Direction.UP and curr == Direction.DOWN or \
            dir == Direction.DOWN and curr == Direction.UP or \
            dir == Direction.LEFT and curr == Direction.RIGHT or \
            dir == Direction.RIGHT and curr == Direction.LEFT:
                return False

        else:
            if dir == Direction.UP:
                self._move_up()
            if dir == Direction.DOWN:
                self._move_down()
            if dir == Direction.LEFT:
                self._move_left()
            if dir == Direction.RIGHT:
                self._move_right()
            return True
            
    def _move_up(self):
        pass
    def _move_down(self):
        pass
    def _move_left(self):
        pass
    def _move_right(self):
        pass

