"""Pacman position, movement and sprites."""

from .display import ImgData
from .game_types import Direction, PacManStatus, GhostStatus, GhostBehavior
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .game import Game

SPEED_BASE = 3


class PacMan:
    """The player character."""
    def __init__(self, name: str = "pacman", x: int = 0, y: int = 0) -> None:
        """Create pacman at the given cell."""
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
        self.speed = SPEED_BASE
        self.direction: Direction | None = None
        self.direction_next: Direction | None = None
        self.status = PacManStatus.NORMAL
        self.game: Game

    def set_image(self, direction: str) -> None:
        """Pick the sprite for `direction` and advance the animation."""
        image_name = self.name + "_" + str(self.image_sprite) + "_" + direction
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
        """Place pacman at (x, y), moving out of a wall if needed."""
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
        self.y_px = y * self.game.display.cell_width

    def death(self) -> None:
        # Clear old
        """Erase pacman and put it back at its starting cell."""
        pos_x = self.game.display.cell_width + 5 \
            + self.x_px + self.game.display.maze_x
        pos_y = self.game.display.cell_width + 5 \
            + self.y_px + self.game.display.maze_y
        # self.game.display.show(self.mask, pos_x, pos_y)
        self.game.display.add_to_bitmap("maze_screen", self.mask.name,
                                        pos_x, pos_y)

        self.set_start_position(self.start_x, self.start_y)
        self.direction = None
        self.direction_next = None
        self.set_image("right")

    def move(self) -> None:
        """Step to the next cell, eat what is there and pick the next one."""
        if self.direction_next is None:
            return

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
        if self.direction is None:
            return
        dx, dy, code = moves[self.direction.value]
        nx, ny = self.x + dx, self.y + dy
        if (0 <= nx < self.game.maze_width and 0 <= ny < self.game.maze_height
                and (self.game.maze[self.y][self.x] & code) == 0):
            self.next_x, self.next_y = nx, ny
            # print(f"PacMan move {self.direction.name} to {nx}, {ny}")
            return

    def speed_reset(self) -> None:
        """Put the speed back to its base value."""
        self.speed = SPEED_BASE

    def increase_speed(self, num: int = 1) -> None:
        """Speed cheat: go faster, wrapping back to the base speed."""
        self.speed += num
        if self.speed > 10:
            self.speed_reset()

    def invisible(self) -> None:
        """Invincibility cheat: toggle the invisible status."""
        if self.status == PacManStatus.NORMAL:
            # print("INVISIBLE")
            self.status = PacManStatus.INVISIBLE
            for ghost in self.game.ghosts:
                if (ghost.status != GhostStatus.DEATH
                   and ghost.behavior != GhostBehavior.TO_START):
                    ghost.set_behavior(GhostBehavior.RANDOM)
        else:
            # print("VISIBLE")
            self.status = PacManStatus.NORMAL
            for ghost in self.game.ghosts:
                if (ghost.status == GhostStatus.ACTIVE
                   and ghost.behavior != GhostBehavior.TO_START):
                    ghost.set_behavior(ghost.behavior_default)
