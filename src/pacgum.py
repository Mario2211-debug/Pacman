import random

def pacgums_generate(maze: list[list[int]], number: int) -> list[list[int]]:
    maze_width = len(maze[0])
    maze_height = len(maze)
    pacgums = [[0] * maze_width for _ in range(maze_height)]

    pacgums_max = min(number, sum(1 for row in maze for x in row if x != 15) - 4)

    pacgums[0][0] = 2
    pacgums[maze_width - 1][0] = 2
    pacgums[0][maze_height - 1] = 2
    pacgums[maze_width - 1][maze_height - 1] = 2

    while pacgums_max:
        x = random.randint(0, maze_width - 1)
        y = random.randint(0, maze_height - 1)
        if maze[x][y] != 15 and not pacgums[x][y]:
            # if random.getrandbits(1):
            pacgums[x][y] = 1
            pacgums_max -= 1

    # for y in range(maze_height):
    #     for x in range(maze_width):
    #         if maze[x][y] != 15 and not pacgums[x][y]:
    #             if random.getrandbits(1):
    #                 pacgums[x][y] = 1
    #                 pacgums_max -= 1
    #         if pacgums_max == 0:
    #             break
    #     if pacgums_max == 0:
    #         break

    return pacgums
