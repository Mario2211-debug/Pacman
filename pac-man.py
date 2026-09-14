import sys
import random
import time

from mazegenerator import MazeGenerator
from engine.engine import Engine
from engine.scenes.menu import MenuScene
from src.config import Config, open_config_file
from src.ghost import Ghost
from src.highscores import Highscores
from src.pacman import PacMan, PacManDirection
from src.pacgum import pacgums_generate

WIN_W = 800
WIN_H = 600


def terminal_simulation(cfg: Config) -> None:
    """Debug view of the maze, pacman and ghosts in the terminal."""
    ghosts = [Ghost(1), Ghost(2), Ghost(3), Ghost(4)]
    pacman = PacMan()

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
        pacman.set_start_position(5, 5)

        ghosts[0].set_start_position(0, 0)
        ghosts[1].set_start_position(lvl["width"] - 1, 0)
        ghosts[2].set_start_position(0, lvl["height"] - 1)
        ghosts[3].set_start_position(lvl["width"] - 1, lvl["height"] - 1)

        # ghosts_positions: list = []
        for step in range(25):
            # print("\nSPEP", step)
            # pacman.move(PacManDirection.BOTTOM)
            pacman.move(random.choice(list(PacManDirection)))
            for ghost in ghosts:
                ghost.set_maze(mazegen.maze)
                # next_position = ghost.find_movement_to(3, 3,
                #                                        ghosts_positions)
                # ghosts_positions.append(next_position)
                ghost.move(ghosts, pacman)
                # print(f"\nGhost {ghost.image} position: {ghost.x}, "
                #       f"{ghost.y}")
                # print("Next position:", next_position)
            # print("------------")

            for y in range(lvl["height"]):
                for x in range(lvl["width"]):
                    if pacman.x == x and pacman.y == y:
                        print("🟡", sep="", end="")
                        continue
                    for ghost in ghosts:
                        if ghost.x == x and ghost.y == y:
                            print("👻", sep="", end="")
                            break
                    else:
                        if mazegen.maze[y][x] == 15:
                            print("🟦", sep="", end="")
                        elif pacgums[y][x] == 1:
                            print("ㆍ", sep="", end="")
                        elif pacgums[y][x] == 2:
                            print("🔴", sep="", end="")
                        else:
                            print("🟩", sep="", end="")
                print()
            time.sleep(1)
            print("\n\n\n")

        print()
        break


def main() -> None:
    args = [arg for arg in sys.argv[1:] if not arg.startswith("--")]
    config_filename = args[0] if args else ""
    cfg = Config.model_validate(open_config_file(config_filename))

    if "--terminal" in sys.argv:
        terminal_simulation(cfg)
        return

    try:
        engine = Engine(WIN_W, WIN_H, cfg, Highscores(cfg.highscore_filename))
    except RuntimeError as err:
        print(f"\033[91m{err}\033[0m")
        sys.exit(1)
    engine.set_scene(MenuScene(engine))
    engine.run()


if __name__ == "__main__":
    main()
