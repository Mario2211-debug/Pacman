from collections import deque

class Ghost:
    def __init__(self, image: int = None, x: int = 0, y: int = 0):
        self.image = image
        self.x = x
        self.y = y
        self.next_x = x
        self.next_y = y
        self.x_px = x * 10
        self.y_px = y * 10
        self.edible = False
        self.freeze = False

    def find_path(self, maze:list[list[int]], end_x: int, end_y: int) -> None:
        moves = [(0, -1, 1, 'N'), (1, 0, 2, 'E'),
                 (0, 1, 4, 'S'), (-1, 0, 8, 'W')]   # dx, dy, wall code, letter
        start = (self.x, self.y)
        goal = (end_x, end_y)
        prev: dict = {start: None}
        queue = deque([start])
        maze_width = len(maze[0])
        maze_height = len(maze)
        while queue:
            x, y = queue.popleft()
            if (x, y) == goal:
                break
            for dx, dy, code, letter in moves:
                nx, ny = x + dx, y + dy
                if (0 <= nx < maze_width and 0 <= ny < maze_height
                        and (maze[y][x] & code) == 0
                        and (nx, ny) not in prev):
                    prev[(nx, ny)] = ((x, y), letter)
                    queue.append((nx, ny))
        if goal not in prev:
            print("MazeGenerator Class error: no shortest path found.")
            return
        letters = []
        cur = goal
        while prev[cur] is not None:
            parent, letter = prev[cur]
            letters.append(letter)
            cur = parent
        print(''.join(reversed(letters)))
        return