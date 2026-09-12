import sys
import random
import time
from mlx import Mlx

from mazegenerator import MazeGenerator
from engine.engine import Engine
from engine.scenes.menu import MenuScene
from src.config import Config, open_config_file
from src.ghost import Ghost
from src.pacman import PacMan, PacManDirection
from src.pacgum import pacgums_generate
from src.display import Display


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


    # ------------------------
    try:
        display = Display()
    except Exception as e:
        print(e)
        exit(1)

    try:
        display.load_image("walls_png", "img/walls_100.png")
        display.create_block_image("corridor_img", display.corridor_width, display.corridor_width, (0xFF000000))
        display.create_block_image("block_42_img", display.corridor_width, display.corridor_width, (0xAA000066))
    except Exception as e:
        print(e)
        exit(1)


    for i in range(10):
        for j in range(10):
            display.show(display.images["walls_png"], display.images["walls_png"].width * i, display.images["walls_png"].height * j)

    mazegen = MazeGenerator((15, 15), False, (0, 0),
                                (1, 1), cfg.seed)
    for x in mazegen.maze:
        print(x)
    pos_y = 0
    for y in range(15):
        pos_y += display.corridor_width
        pos_x = 0
        for x in range(15):
            pos_x += display.corridor_width
            if mazegen.maze[y][x] == 15:
                pos_x += display.wall_width
                display.show(display.images["corridor_img"], pos_x, pos_y + display.wall_width)
                continue

            if not mazegen.maze[y][x] & 8:
                # print(x, y, "don't has left wall")
                display.show(display.images["corridor_img"], pos_x, pos_y + display.wall_width)
            pos_x += display.wall_width
            if not mazegen.maze[y][x] & 1:
                # print(x, y, "don't has top wall")
                display.show(display.images["corridor_img"], pos_x, pos_y)
            display.show(display.images["corridor_img"], pos_x, pos_y + display.wall_width)
        pos_y += display.wall_width



    def gere_close_1(display):
        display.mlx.mlx_loop_exit(display.mlx_ptr)
    # event hooks
    display.mlx.mlx_hook(display.win, 33, 0, gere_close_1, display)  # WM_DELETE_WINDOW

    # Main loop
    display.mlx.mlx_loop(display.mlx_ptr)
    # ------------------------

    #
    # python3 -c "from PIL import Image; Image.open('img/walls_100.png').convert('RGB').save('img/walls_100_new.png')"
    #

    exit()





    # ghost1 = Ghost()
    # ghost2 = Ghost()
    # ghost3 = Ghost()
    # ghost4 = Ghost()

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
        pacman.set_pacgums(pacgums)
        pacman.set_start_position(lvl["width"] // 2, lvl["height"] // 2)

        ghosts[0].set_start_position(0, 0)
        ghosts[1].set_start_position(lvl["width"] - 1, 0)
        ghosts[2].set_start_position(0, lvl["height"] - 1)
        ghosts[3].set_start_position(lvl["width"] - 1, lvl["height"] - 1)

        # ghosts_positions: list = []
        for step in range(25):
            print("\nSPEP", step + 1)
            # pacman.move(PacManDirection.BOTTOM)
            pacman.move(random.choice(list(PacManDirection)))
            for ghost in ghosts:
                ghost.set_maze(mazegen.maze)
                # next_position = ghost.find_movement_to(3, 3, ghosts_positions)
                # ghosts_positions.append(next_position)
                ghost.move(ghosts, pacman)
                # print(f"\nGhost {ghost.image} position: {ghost.x}, {ghost.y}")
                # print("Next position:", next_position)
            # print("------------")

            print()
            print("   ", sep="", end="")
            for x in range(lvl["width"]):
                print(f"{x:<2}", sep="", end="")
            print("\n")
            for y in range(lvl["height"]):
                print(f"{y:<3}", sep="", end="")
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
                            # print("🟩", sep="", end="")
                            print("  ", sep="", end="")
                print()
            time.sleep(1)
            print("\n\n\n")


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
