import sys

from mazegenerator import MazeGenerator
from engine.engine import Engine
from engine.scenes.menu import MenuScene
from src.config import Config, open_config_file
from src.ghost import Ghost
from src.pacman import PacMan
from src.pacgum import pacgums_generate


# engine = Engine(800, 600)
# engine.set_scene(MenuScene(engine))
# engine.run()

if __name__ == "__main__":
    config_filename = ""
    if len(sys.argv) == 2:
        config_filename = sys.argv[1]
    config_json = open_config_file(config_filename)
    cfg = Config.model_validate(config_json)
    # print(cfg)

    # ghost1 = Ghost()
    # ghost2 = Ghost()
    # ghost3 = Ghost()
    # ghost4 = Ghost()

    ghosts = [Ghost(1), Ghost(2), Ghost(3), Ghost(4)]
    pacman = PacMan(10, 10)

    for lvl in cfg.level:
        mazegen = MazeGenerator((lvl["width"], lvl["height"]), False, (0, 0),
                                (1, 1), cfg.seed)
        for x in mazegen.maze:
            print(x)

        pacgums = pacgums_generate(mazegen.maze, cfg.pacgum)
        print()
        for x in pacgums:
            print(x)

        pacman.set_maze(mazegen.maze)

        ghosts[0].set_start_position(0, 0)
        ghosts[1].set_start_position(lvl["width"] - 1, 0)
        ghosts[2].set_start_position(0, lvl["height"] - 1)
        ghosts[3].set_start_position(lvl["width"] - 1, lvl["height"] - 1)

        # ghosts_positions: list = []
        for step in range(15):
            for ghost in ghosts:
                ghost.set_maze(mazegen.maze)
                # next_position = ghost.find_movement_to(3, 3, ghosts_positions)
                # ghosts_positions.append(next_position)
                ghost.move(ghosts, pacman)
                print(f"\nGhost {ghost.image} position: {ghost.x}, {ghost.y}")
                # print("Next position:", next_position)
            print("------------")

        # ghosts_positions: list = []
        # ghost1.set_maze(mazegen.maze)
        # ghost1.set_start_position(0, 0)
        # print("\nGhost 1 position:", ghost1.x, ghost1.y)
        # next_position = ghost1.find_movement_to(3, 3)
        # ghosts_positions.append(next_position)
        # print("Next position:", next_position)

        # ghost2.set_maze(mazegen.maze)
        # ghost2.set_start_position(lvl["width"] - 1, 0)
        # print("\nGhost 2 position:", ghost2.x, ghost2.y)
        # next_position = ghost2.find_movement_to(3, 3, ghosts_positions)
        # ghosts_positions.append(next_position)
        # print("Next position:", next_position)

        # ghost3.set_maze(mazegen.maze)
        # ghost3.set_start_position(0, lvl["height"] - 1)
        # print("\nGhost 3 position:", ghost3.x, ghost3.y)
        # next_position = ghost3.find_movement_to(3, 3, ghosts_positions)
        # ghosts_positions.append(next_position)
        # print("Next position:", next_position)

        # ghost4.set_maze(mazegen.maze)
        # ghost4.set_start_position(lvl["width"] - 1, lvl["height"] - 1)
        # print("\nGhost 4 position:", ghost4.x, ghost4.y)
        # next_position = ghost4.find_movement_to(3, 3, ghosts_positions)
        # print("Next position:", next_position)

        print()
        break
