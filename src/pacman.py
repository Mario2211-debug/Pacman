from enum import Enum

from .display import ImgData
from .types import PacManStatus, GhostStatus, GhostBehavior
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .game import Game

class PacMan:
    def __init__(self, name: str = "pacman", x: int = 0, y: int = 0) -> None:
        self.name = name
        self.image: ImgData
        self.mask: ImgData
        self.image_sprite: int = 1
        self.image_sprite_direction: int = 1
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

    def set_image(self, image_direction: str) -> None:
        image_name = self.name + "_" + str(self.image_sprite) + "_" + image_direction
        if not self.game.display.images.get(image_name):
            return

        self.image = self.game.display.images[image_name]
        self.mask = self.game.display.images[image_name + "_mask"]

        if self.image_sprite_direction:
            self.image_sprite += 1
            if self.image_sprite > 4:
                self.image_sprite = 4
                self.image_sprite_direction = 0
        else:
            self.image_sprite -= 1
            if self.image_sprite < 1:
                self.image_sprite = 1
                self.image_sprite_direction = 1

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
        self.x_px = x * self.game.display.cell_width
        self.y_px = y  * self.game.display.cell_width

    def death(self) -> None:
        # Clear old
        pos_x = self.game.display.cell_width + 5 + self.x_px
        pos_y = self.game.display.cell_width + 5 + self.y_px
        # self.game.display.show(self.mask, pos_x, pos_y)
        self.game.display.add_to_bitmap("maze_screen", self.mask.name, pos_x, pos_y)

        self.set_start_position(self.start_x, self.start_y)
        self.direction = None
        self.direction_next = None
        self.set_image("right")

    def move(self) -> None:
        moves = [(0, -1, 1), (1, 0, 2),
                 (0, 1, 4), (-1, 0, 8)]
        self.x, self.y = self.next_x, self.next_y
        self.x_px = self.x * self.game.display.cell_width
        self.y_px = self.y * self.game.display.cell_width
        self.game.eat_pacgum(self.x, self.y)
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

    def increase_speed(self, num: int = 1) -> None:
        self.speed += num
        if self.speed > 10:
            self.speed = 3

    def invisible(self) -> None:
        if self.status == PacManStatus.NORMAL:
            print("INVISIBLE")
            self.status = PacManStatus.INVISIBLE
            for ghost in self.game.ghosts:
                if ghost.status != GhostStatus.DEATH:
                    ghost.set_behavior(GhostBehavior.RANDOM)
        else:
            print("VISIBLE")
            self.status = PacManStatus.NORMAL
            for ghost in self.game.ghosts:
                if ghost.status == GhostStatus.ACTIVE:
                    ghost.set_behavior(ghost.behavior_default)
