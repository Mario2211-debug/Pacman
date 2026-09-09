from collections import deque

class Ghost:
    def __init__(self, image: int = 0, x: int = 0, y: int = 0, maze: list[list[int]] = []) -> None:
        self.image = image
        self.start_x = x
        self.start_y = y
        self.x = x
        self.y = y
        self.next_x = x
        self.next_y = y
        self.x_px = x * 10
        self.y_px = y * 10
        self.edible = False
        self.freeze = False
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
        self.start_x = x
        self.start_y = y
        self.x = x
        self.y = y
        self.x_px = x * 10
        self.y_px = y * 10

    def find_movement_to(self, end_x: int, end_y: int, ghosts_positions: list[tuple[int]] = []) -> tuple[int]:
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
                if (0 <= nx < self._maze_width and 0 <= ny < self._maze_height
                        and (self._maze[y][x] & code) == 0
                        and (nx, ny) not in prev):
                    prev[(nx, ny)] = ((x, y))
                    queue.append((nx, ny))
        if goal not in prev:
            # print("MazeGenerator Class error: no shortest path found.")
            # return
            return (self.x, self.y)
        parents = []
        cur = goal
        while prev[cur] is not None:
            parent = prev[cur]
            parents.append(parent)
            cur = parent
        if parents:
            self.next_x = parents[-2][0]
            self.next_y = parents[-2][1]
            return parents[-2]
        else:
            self.next_x = goal[0]
            self.next_y = goal[1]
            return goal
