import random
from collections import deque

from .types import Direction, GhostStatus, GhostBehavior, PacManStatus
from .display import ImgData

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .game import Game

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
        self.behavior_default = GhostBehavior.PLAYER
        self.behavior = GhostBehavior.PLAYER
        self.target: tuple
        self.direction = Direction.RIGHT
        self.status = GhostStatus.ACTIVE
        self.freeze = False
        self.game: Game

    def set_image(self, image_direction: str) -> None:
        if self.status == GhostStatus.DEATH:
            image_name = "ghost_dead_right"
        elif self.status == GhostStatus.EDIBLE:
            image_name = "scared_" + self.name + "_" + image_direction
        else:
            image_name = self.name + "_" + image_direction
        if self.game.display.images.get(image_name):
            self.image = self.game.display.images[image_name]
            self.mask = self.game.display.images[image_name + "_mask"]

    def set_behavior_default(self, behavior: GhostBehavior):
        self.behavior_default = behavior

    def set_behavior(self, behavior: GhostBehavior):
        self.behavior = behavior

    def set_start_position(self, x: int, y: int) -> None:
        self.start_x = x
        self.start_y = y
        self.x = x
        self.y = y
        self.next_x = x
        self.next_y = y
        self.x_px = x * self.game.display.cell_width
        self.y_px = y  * self.game.display.cell_width
        self.target = (x, y)

    def find_next_position(self, target: tuple) -> tuple[int]:
        moves = [(0, -1, 1), (1, 0, 2),
                 (0, 1, 4), (-1, 0, 8)]
        start = (self.x, self.y)
        goal = target
        prev: dict = {start: None}
        queue = deque([start])
        ghosts_next_positions = [(ghost.next_x, ghost.next_y) for ghost in self.game.ghosts if ghost is not self and ghost.status != GhostStatus.DEATH]
        while queue:
            x, y = queue.popleft()
            if (x, y) == goal:
                break
            for dx, dy, code in moves:
                nx, ny = x + dx, y + dy
                if (nx, ny) in ghosts_next_positions and self.status != GhostStatus.DEATH:
                    continue
                if self.behavior == GhostBehavior.SCARED and nx == self.game.pacman.x and ny == self.game.pacman.y:
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
        if (self.x, self.y) in corners:
            corners.remove((self.x, self.y))
        return random.choice(corners)

    def get_random_cell(self) -> tuple:
        rand_x = random.randint(0, self.game.maze_width - 1)
        rand_y = random.randint(0, self.game.maze_height - 1)
        if self.game.maze[rand_y][rand_x] !=  15:
            return (rand_x, rand_y)
        return self.get_random_cell()

    def get_random_corner_far_from_pacman(self) -> tuple:
        corners = [(0, 0), (self.game.maze_width - 1, 0), (0, self.game.maze_height - 1), (self.game.maze_width - 1, self.game.maze_height - 1)]
        pacman_quarter_x = min(1, (self.game.pacman.x // (self.game.maze_width // 2)))
        pacman_quarter_y = min(1, (self.game.pacman.y // (self.game.maze_height // 2)))
        corner_x = pacman_quarter_x * (self.game.maze_width- 1)
        corner_y = pacman_quarter_y * (self.game.maze_height- 1)
        # print("pacman near corner:", (pacman_quarter_x * (self.game.maze_width- 1), pacman_quarter_y * (self.game.maze_height - 1)))
        if (corner_x, corner_y) in corners:
            corners.remove((corner_x, corner_y))
        return random.choice(corners)

    def get_random_cell_far_from_pacman(self) -> tuple:
        ghosts_targets = [ghost.target for ghost in self.game.ghosts if ghost is not self]
        # print("ghosts_targets:", ghosts_targets)
        rand_x = random.randint(0, self.game.maze_width - 1)
        rand_y = random.randint(0, self.game.maze_height - 1)
        if (self.game.maze[rand_y][rand_x] ==  15 or
            (rand_x, rand_y) in ghosts_targets or
            (self.game.pacman.x - self.game.maze_width // 4 < rand_x < self.game.pacman.x + self.game.maze_width // 4 and
            self.game.pacman.y - self.game.maze_height // 4 < rand_x < self.game.pacman.y + self.game.maze_height // 4)):
            return self.get_random_cell_far_from_pacman()
        return (rand_x, rand_y)

    def move(self):
        if self.freeze is False:
            self.x, self.y = self.next_x, self.next_y
            self.x_px = self.x * self.game.display.cell_width
            self.y_px = self.y * self.game.display.cell_width
            # print(f"Ghost {self.image} position: {self.x}, {self.y}")

            if self.behavior == GhostBehavior.PLAYER:
                self.target = (self.game.pacman.next_x, self.game.pacman.next_y)
            elif self.behavior == GhostBehavior.CORNERS:
                if self.target == (self.x, self.y):
                    self.target = self.get_random_corner()
            elif self.behavior == GhostBehavior.RANDOM:
                if self.target == (self.x, self.y):
                    self.target = self.get_random_cell()
            elif self.behavior == GhostBehavior.SCARED:
                if self.target == (self.x, self.y):
                    self.target = self.get_random_cell_far_from_pacman()
                    # self.target = self.get_random_corner_far_from_pacman()
                # if self.target == (self.x, self.y):
                # self.target = self.get_random_cell_far_from_pacman()
                # print(self.name, self.x, self.y, "Scared and run to:", self.target)
            elif self.behavior == GhostBehavior.DEATH:
                if self.target == (self.x, self.y):
                    print("Death found target")
                    self.reborn()
            elif self.behavior == GhostBehavior.TO_START:
                if (self.x, self.y) != (self.start_x, self.start_y):
                    self.target = (self.start_x, self.start_y)
                else:
                    self.reborn()
                    # print("self.target", self.target)

            move_to_x, move_to_y = self.find_next_position(self.target)
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

    def make_freeze(self):
        if self.freeze == True:
            self.freeze = False
        else:
            self.freeze = True
        # if self.status == GhostStatus.FREEZE:
        #     self.status = GhostStatus.ACTIVE
        # else:
        #     self.status = GhostStatus.FREEZE

    def death(self):
        self.speed = 20
        self.status = GhostStatus.DEATH
        self.set_behavior(GhostBehavior.DEATH)
        self.target = self.get_random_corner_far_from_pacman()
        self.set_image("right")
        print(self.name, "Death in position", self.x, self.y)

    def reborn(self):
        print(self.name, "Reborn in position", self.x, self.y)
        self.speed = 2
        self.status = GhostStatus.ACTIVE
        if self.game.pacman.status != PacManStatus.INVISIBLE:
            self.set_behavior(self.behavior_default)
        else:
            self.set_behavior(GhostBehavior.RANDOM)
        self.set_image("right")
