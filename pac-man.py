from mazegenerator import MazeGenerator
from engine.engine import Engine


engine = Engine(700, 600)
engine.run()

mazegen = MazeGenerator((15, 15), False, (0, 0), (10, 10), 42)

if __name__ == "__main__":
    # mazegen.generate()
    maze = mazegen.maze
    for x in maze:
        print(x)
    print()
    print(mazegen._shortest_path)

    mazegen._entryx, mazegen._entryy = 1, 1
    mazegen._exitx, mazegen._exity = 2, 2
    mazegen._find_short_path()
    print(mazegen._shortest_path)
