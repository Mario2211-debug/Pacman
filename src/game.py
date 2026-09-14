from .types import GameStatus
from .display import Display
from enum import Enum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .pacman import PacMan
    from .ghost import Ghost

class Game:
    def __init__(self):
        self.pacman: PacMan
        self.ghosts: list[Ghost]
        self.display: Display
        self.status = GameStatus.RUN