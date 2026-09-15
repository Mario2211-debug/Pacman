from collections import deque
from enum import Enum

from .types import Direction, GameStatus
from .display import ImgData

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .game import Game

class GhostStatus(Enum):
  ACTIVE = 1
  EDIBLE = 2
  DEATH = 3


class Ghost:
    def __init__(self, image: ImgData, mask: ImgData, x: int = 0, y: int = 0) -> None:
        self.image = image
        self.mask = mask
        self.start_x = x
        self.start_y = y
        self.x = x
        self.y = y
        self.next_x = x
        self.next_y = y
        self.x_px = x
        self.y_px = y
        self.speed = 2
        self.direction = Direction.RIGHT
        self.status = GhostStatus.ACTIVE
        self.freeze = False
        self.game: Game

    def set_start_position(self, x: int, y: int) -> None:
        self.start_x = x
        self.start_y = y
        self.x = x
        self.y = y
        self.next_x = x
        self.next_y = y
        self.x_px = x * (self.game.display.corridor_width + self.game.display.wall_width)
        self.y_px = y  * (self.game.display.corridor_width + self.game.display.wall_width)

    def find_next_position(self, end_x: int, end_y: int, ghosts_positions: list[tuple[int]] = []) -> tuple[int]:
        moves = [(0, -1, 1), (1, 0, 2),
                 (0, 1, 4), (-1, 0, 8)]
        start = (self.x, self.y)
        goal = (end_x, end_y)
        prev: dict = {start: None}
        queue = deque([start])
        while queue:
            x, y = queue.popleft()
            if (x, y) == goal:
                break
            for dx, dy, code in moves:
                nx, ny = x + dx, y + dy
                if (nx, ny) in ghosts_positions:
                    continue
                if (0 <= nx < self.game.maze_width and 0 <= ny < self.game.maze_height
                        and (self.game.maze[y][x] & code) == 0
                        and (nx, ny) not in prev):
                    prev[(nx, ny)] = ((x, y))
                    queue.append((nx, ny))
        if goal not in prev:
            return (self.x, self.y)
        parents = []
        cur = goal
        while prev[cur] is not None:
            parent = prev[cur]
            parents.append(parent)
            cur = parent


        if len(parents) > 1:
            # print(parents)
            self.next_x = parents[-2][0]
            self.next_y = parents[-2][1]
            return parents[-2]
        else:
            self.next_x = goal[0]
            self.next_y = goal[1]
            return goal

    def move(self):
        if self.status == GhostStatus.ACTIVE:
            self.x, self.y = self.next_x, self.next_y
            # print(f"Ghost {self.image} position: {self.x}, {self.y}")
            ghosts_next_positions = [(ghost.next_x, ghost.next_y) for ghost in self.game.ghosts if ghost is not self]
            move_to_x, move_to_y = self.find_next_position(self.game.pacman.next_x, self.game.pacman.next_y, ghosts_next_positions)
            self.next_x, self.next_y = move_to_x, move_to_y

            if move_to_x - self.x == 1:
                self.direction = Direction.RIGHT
            elif move_to_x - self.x == -1:
                self.direction = Direction.LEFT
            elif move_to_y - self.y == 1:
                self.direction = Direction.BOTTOM
            elif move_to_y - self.y == -1:
                self.direction = Direction.TOP
            else:
                print("Ghost can't move")

            # print(f"Ghost {self.image} move to {move_to_x} {move_to_y}")

