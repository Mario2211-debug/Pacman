from enum import Enum

class Direction(Enum):
  TOP = 0
  RIGHT = 1
  BOTTOM = 2
  LEFT = 3

class GameStatus(Enum):
  RUN = 1
  PAUSED = 2
  GAME_OVER = 3
  VICTORY = 3
  ERROR = 4

class PacManStatus(Enum):
  NORMAL = 1
  INVISIBLE = 2

class GhostStatus(Enum):
  ACTIVE = 1
  EDIBLE = 2
  DEATH = 3
#   FREEZE = 4

class GhostBehavior(Enum):
  PLAYER = 1
  CORNERS = 2
  RANDOM = 3
  TO_START = 4
  SCARED = 5
  DEATH = 6