from enum import Enum

class PacManStatus(Enum):
  NORMAL = 1
  INVISIBLE = 2
  FAST = 3

class PacManDirection(Enum):
  TOP = 1
  RIGHT = 2
  BOTTOM = 3
  LEFT = 3

class PacMan:
    def __init__(self, x: int = 0, y: int = 0, maze: list[list[int]] = []) -> None:
        self.start_x = x
        self.start_y = y
        self.x = x
        self.y = y
        self.next_x = x
        self.next_y = y
        self.x_px = x * 10
        self.y_px = y * 10
        self.status = PacManStatus.NORMAL
        self._maze = maze
        if maze:
            self._maze_width = len(maze[0])
            self._maze_height = len(maze)

    def set_maze(self, maze: list[list[int]]) -> None:
        self._maze = maze
        if maze:
            self._maze_width = len(maze[0])
            self._maze_height = len(maze)