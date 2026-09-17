import random
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

class Behavior(Enum):
  PLAYER = 1
  CORNERS = 2
  RANDOM = 3
  TO_START = 4


class Ghost:
    def __init__(self, name: str, x: int = 0, y: int = 0) -> None:
        self.name = name
        self.image: ImgData
        self.mask: ImgData
        self.start_x = x
        self.start_y = y
        self.x = x
        self.y = y
        self.next_x = x
        self.next_y = y
        self.x_px = x
        self.y_px = y
        self.speed = 2
        self.behavior_standart = Behavior.PLAYER
        self.behavior = Behavior.PLAYER
        self.target: tuple
        self.direction = Direction.RIGHT
        self.status = GhostStatus.ACTIVE
        self.freeze = False
        self.game: Game

    def set_image(self, image_name) -> None:
        if self.game.display.images:
            self.image = self.game.display.images[image_name]
            self.mask = self.game.display.images[image_name + "_mask"]

    def set_behavior_standart(self, behavior: Behavior):
        self.behavior_standart = behavior

    def set_behavior(self, behavior: Behavior):
        self.behavior = behavior

    def set_start_position(self, x: int, y: int) -> None:
        self.start_x = x
        self.start_y = y
        self.x = x
        self.y = y
        self.next_x = x
        self.next_y = y
        self.x_px = x * (self.game.display.corridor_width + self.game.display.wall_width)
        self.y_px = y  * (self.game.display.corridor_width + self.game.display.wall_width)
        self.target = (x, y)

    def find_next_position(self, target: tuple, ghosts_positions: list[tuple[int]] = []) -> tuple[int]:
        moves = [(0, -1, 1), (1, 0, 2),
                 (0, 1, 4), (-1, 0, 8)]
        start = (self.x, self.y)
        goal = target
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

    def get_random_corner(self) -> tuple:
        corners = [(0, 0), (self.game.maze_width - 1, 0), (0, self.game.maze_height - 1), (self.game.maze_width - 1, self.game.maze_height - 1)]
        corners.remove((self.x, self.y))
        return random.choice(corners)

    def get_random_cell(self) -> tuple:
        rand_x = random.randint(0, self.game.maze_width - 1)
        rand_y = random.randint(0, self.game.maze_height - 1)
        if self.game.maze[rand_y][rand_x] !=  15:
            return (rand_x, rand_y)
        return self.get_random_cell()

    def move(self):
        if self.status == GhostStatus.ACTIVE:
            self.x, self.y = self.next_x, self.next_y
            self.x_px = self.x * self.game.display.cell_width
            self.y_px = self.y * self.game.display.cell_width
            # print(f"Ghost {self.image} position: {self.x}, {self.y}")
            ghosts_next_positions = [(ghost.next_x, ghost.next_y) for ghost in self.game.ghosts if ghost is not self]

            if self.behavior == Behavior.PLAYER:
                self.target = (self.game.pacman.next_x, self.game.pacman.next_y)
            elif self.behavior == Behavior.CORNERS:
                if self.target == (self.x, self.y):
                    self.target = self.get_random_corner()
            elif self.behavior == Behavior.RANDOM:
                if self.target == (self.x, self.y):
                    self.target = self.get_random_cell()
            elif self.behavior == Behavior.TO_START:
                if (self.x, self.y) != (self.start_x, self.start_y):
                    self.target = (self.start_x, self.start_y)
                else:
                    self.set_behavior(self.behavior_standart)
                    self.speed = 2
                    # print("self.target", self.target)

            move_to_x, move_to_y = self.find_next_position(self.target, ghosts_next_positions)
            self.next_x, self.next_y = move_to_x, move_to_y

            if move_to_x - self.x == 1:
                self.direction = Direction.RIGHT
            elif move_to_x - self.x == -1:
                self.direction = Direction.LEFT
            elif move_to_y - self.y == 1:
                self.direction = Direction.BOTTOM
            elif move_to_y - self.y == -1:
                self.direction = Direction.TOP
            # else:
            #     print("Ghost", self.name, self.x, self.y, "can't move to", self.target)
            #     print("Next position:", self.next_x, self.next_y)

            # print(f"Ghost {self.image} move to {move_to_x} {move_to_y}")

