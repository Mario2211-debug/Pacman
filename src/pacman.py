from enum import Enum

class PacManStatus(Enum):
  NORMAL = 1
  INVISIBLE = 2
  FAST = 3

class PacManDirection(Enum):
  TOP = 0
  RIGHT = 1
  BOTTOM = 2
  LEFT = 3

class PacMan:
    def __init__(self, x: int = 0, y: int = 0, maze: list[list[int]] = []) -> None:
        self.start_x = x
        self.start_y = y
        self.x = x
        self.y = y
        self.next_x = x
        self.next_y = y
        self.x_px = x * 10
        self.y_px = y * 10
        self.status = PacManStatus.NORMAL
        self._maze = maze
        if maze:
            self._maze_width = len(maze[0])
            self._maze_height = len(maze)

    def set_maze(self, maze: list[list[int]]) -> None:
        self._maze = maze
        if maze:
            self._maze_width = len(maze[0])
            self._maze_height = len(maze)

    def set_start_position(self, x: int, y: int) -> None:
        if self._maze[y][x] == 15:
            x += 1
        if self._maze[y][x] == 15:
            y -= 1
        self.start_x = x
        self.start_y = y
        self.x = x
        self.y = y
        self.next_x = x
        self.next_y = y
        self.x_px = x * 10
        self.y_px = y * 10

    def move(self, direction: PacManDirection):
        moves = [(0, -1, 1), (1, 0, 2),
                 (0, 1, 4), (-1, 0, 8)]
        self.x, self.y = self.next_x, self.next_y
        print(f"PacMan position: {self.x}, {self.y}")
        dx, dy, code = moves[direction.value]
        nx, ny = self.x + dx, self.y + dy
        if (0 <= nx < self._maze_width and 0 <= ny < self._maze_height
            and (self._maze[self.y][self.x] & code) == 0):
            self.next_x, self.next_y = nx, ny
            # print(f"PacMan move {direction.name} to {nx}, {ny}")
            return
        # print("PacMan CAN'T move")

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