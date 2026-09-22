"""Enumerations shared by the game modules."""

from enum import Enum


class Direction(Enum):
    """Direction pacman or a ghost is facing."""
    TOP = 0
    RIGHT = 1
    BOTTOM = 2
    LEFT = 3


class GameStatus(Enum):
    """State of the game loop."""
    RUN = 1
    PAUSED = 2
    GAME_OVER = 3
    VICTORY = 3
    ERROR = 4


class PacManStatus(Enum):
    """Pacman state: normal, invisible (cheat) or fast."""
    NORMAL = 1
    INVISIBLE = 2


class GhostStatus(Enum):
    """Ghost state: active, edible or dead."""
    ACTIVE = 1
    EDIBLE = 2
    DEATH = 3


class GhostBehavior(Enum):
    """How a ghost chooses its target."""
    PLAYER = 1
    CORNERS = 2
    RANDOM = 3
    TO_START = 4
    SCARED = 5
    DEATH = 6
