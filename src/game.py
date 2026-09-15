from .types import GameStatus
from .display import Display
from enum import Enum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .pacman import PacMan
    from .ghost import Ghost
    from .config import Config

class Game:
    def __init__(self):
        self.config: Config
        self.pacman: PacMan
        self.ghosts: list[Ghost]
        self.display: Display
        self.status = GameStatus.RUN
        self.points = 0
        self.maze: list[list[int]] = []
        if self.maze:
            self.maze_width = len(self.maze[0])
            self.maze_height = len(self.maze)
        self.pacgums: list[list[int]] = []

    def set_maze(self, maze: list[list[int]]) -> None:
        self.maze = maze
        if maze:
            self.maze_width = len(maze[0])
            self.maze_height = len(maze)