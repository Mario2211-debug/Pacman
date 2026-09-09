from mazegenerator import MazeGenerator
from engine.engine import Engine
from engine.scenes.menu import MenuScene


engine = Engine(800, 600)
engine.set_scene(MenuScene(engine))
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
    print(0xFF0000FF)
