from enum import Enum

class Direction(Enum):
  TOP = 0
  RIGHT = 1
  BOTTOM = 2
  LEFT = 3

class GameStatus(Enum):
  RUN = 1
  PAUSED = 2
  DEAD = 3