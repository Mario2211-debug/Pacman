from enum import Enum

from .display import ImgData
from .types import Direction
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .game import Game

class PacManStatus(Enum):
  NORMAL = 1
  INVISIBLE = 2
  FAST = 3

class PacMan:
    def __init__(self, name: str = "pacman", x: int = 0, y: int = 0) -> None:
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
        self.speed = 3
        self.direction = None
        self.direction_next = None
        self.status = PacManStatus.NORMAL
        self.game: Game

    def set_image(self, image_name):
        if self.game.display.images:
            self.image = self.game.display.images[image_name]
            self.mask = self.game.display.images[image_name + "_mask"]

    def set_start_position(self, x: int, y: int) -> None:
        if self.game.maze[y][x] == 15:
            x += 1
        if self.game.maze[y][x] == 15:
            y -= 1
        self.start_x = x
        self.start_y = y
        self.x = x
        self.y = y
        self.next_x = x
        self.next_y = y
        self.x_px = x * (self.game.display.corridor_width + self.game.display.wall_width)
        self.y_px = y  * (self.game.display.corridor_width + self.game.display.wall_width)

    def death(self):
        # Clear old
        pos_x = self.game.display.cell_width + 5 + self.x_px
        pos_y = self.game.display.cell_width + 5 + self.y_px
        self.game.display.show(self.mask, pos_x, pos_y)

        self.set_start_position(self.start_x, self.start_y)
        self.direction = None
        self.direction_next = None
        self.set_image("pacman_right")

    def eat(self):
        if self.game.pacgums[self.y][self.x] == 2:
            self.game.pacgums[self.y][self.x] = 0
            self.game.stats.increase_score(100)
        elif self.game.pacgums[self.y][self.x] == 1:
            # self.game.stats.score += 1
            self.game.pacgums[self.y][self.x] = 0
            self.game.stats.increase_score(1)
            # print(self.game.points)

    def move(self):
        moves = [(0, -1, 1), (1, 0, 2),
                 (0, 1, 4), (-1, 0, 8)]
        self.x, self.y = self.next_x, self.next_y
        self.x_px = self.x * (self.game.display.corridor_width + self.game.display.wall_width)
        self.y_px = self.y * (self.game.display.corridor_width + self.game.display.wall_width)
        self.eat()
        # print(f"PacMan position: {self.x}, {self.y} ({self.points} points)")
        dx, dy, code = moves[self.direction_next.value]
        nx, ny = self.x + dx, self.y + dy
        if (0 <= nx < self.game.maze_width and 0 <= ny < self.game.maze_height
            and (self.game.maze[self.y][self.x] & code) == 0):
            self.next_x, self.next_y = nx, ny
            self.direction = self.direction_next
            # print(f"PacMan change {self.direction_next.name} to {nx}, {ny}")
            return
        dx, dy, code = moves[self.direction.value]
        nx, ny = self.x + dx, self.y + dy
        if (0 <= nx < self.game.maze_width and 0 <= ny < self.game.maze_height
            and (self.game.maze[self.y][self.x] & code) == 0):
            self.next_x, self.next_y = nx, ny
            # print(f"PacMan move {self.direction.name} to {nx}, {ny}")
            return
        # print("PacMan CAN'T move", self.direction, self.direction_next, self.x, self.y)
        # print(self.next_x, self.next_y)

        # if direction == PacManDirection.TOP:
        #     nx, ny = self.x, self.y - 1
        #     if (0 <= nx < self._maze_width and 0 <= ny < self._maze_height
        #         and (self._maze[self.y][self.x] & 1) == 0):
        #         self.next_x, self.next_y = nx, ny
        #         print("PacMan move TOP")
        #         return
        #     print("PacMan CAN'T move")
        # elif direction == PacManDirection.RIGHT:
        #     nx, ny = self.x + 1, self.y
        #     if (0 <= nx < self._maze_width and 0 <= ny < self._maze_height
        #         and (self._maze[self.y][self.x] & 2) == 0):
        #         self.next_x, self.next_y = nx, ny
        #         print("PacMan move RIGHT")
        #         return
        #     print("PacMan CAN'T move")
        # elif direction == PacManDirection.BOTTOM:
        #     nx, ny = self.x + 1, self.y
        #     if (0 <= nx < self._maze_width and 0 <= ny < self._maze_height
        #         and (self._maze[self.y][self.x] & 4) == 0):
        #         self.next_x, self.next_y = nx, ny
        #         print("PacMan move BOTTOM")
        #         return
        #     print("PacMan CAN'T move")
        # elif direction == PacManDirection.LEFT:
        #     nx, ny = self.x + 1, self.y
        #     if (0 <= nx < self._maze_width and 0 <= ny < self._maze_height
        #         and (self._maze[self.y][self.x] & 8) == 0):
        #         self.next_x, self.next_y = nx, ny
        #         print("PacMan move LEFT")
        #         return
        #     print("PacMan CAN'T move")