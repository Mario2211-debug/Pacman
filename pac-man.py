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

class ImgData:
    """Structure for image data"""
    def __init__(self):
        self.img = None
        self.width = 0
        self.height = 0
        self.data = None
        self.sl = 0  # size line
        self.bpp = 0  # bits per pixel
        self.iformat = 0

class Display:
    """Structure for main vars"""
    def __init__(self):
        self.mlx = None
        self.mlx_ptr = None
        self.win = None
        self.walls_png = ImgData()
        self.corridor_img = ImgData()


engine = Engine(800, 600)
engine.set_scene(MenuScene(engine))
engine.run()

if __name__ == "__main__":
    config_filename = ""
    if len(sys.argv) == 2:
        config_filename = sys.argv[1]
    config_json = open_config_file(config_filename)
    cfg = Config.model_validate(config_json)
    # print(cfg)

    # ------------------------
    display = Display()
    try:
        display.mlx = Mlx()
    except Exception as e:
        print(f"Error: Can't initialize MLX: {e}", file=sys.stderr)
        sys.exit(1)
    display.mlx_ptr = display.mlx.mlx_init()

    screen_size = display.mlx.mlx_get_screen_size(display.mlx_ptr)
    win_w = screen_size[1]
    win_h = screen_size[2]
    # win_w = 500
    # win_h = 500
    try:
        display.win = display.mlx.mlx_new_window(display.mlx_ptr, win_w, win_h, "MLX main win")
        if not display.win:
            raise Exception("Can't create main window")
    except Exception as e:
        print(f"Error Win create: {e}", file=sys.stderr)
        sys.exit(1)

    # Load PNG & XPM
    display.walls_png = ImgData()
    result = display.mlx.mlx_png_file_to_image(display.mlx_ptr, "img/walls_200.png")
    if not result:
        raise Exception("Can't load PNG")
    display.walls_png.img, display.walls_png.width, display.walls_png.height = result
    if not display.walls_png.img:
        raise Exception("Can't create png")
    display.walls_png.data, display.walls_png.bpp, display.walls_png.sl, display.walls_png.iformat = \
        display.mlx.mlx_get_data_addr(display.walls_png.img)

    # Empty image for corridor
    display.corridor_img.img = display.mlx.mlx_new_image(display.mlx_ptr, 30, 30)
    if not display.corridor_img.img:
        raise Exception("Can't create image 1")

    # display.corridor_img.width = 50
    # display.corridor_img.height = 50
    display.corridor_img.data, display.corridor_img.bpp, display.corridor_img.sl, display.corridor_img.iformat = \
        display.mlx.mlx_get_data_addr(display.corridor_img.img)
    # Fill image for corridor
    for i in range(0, display.corridor_img.sl * 30, 4):
        display.corridor_img.data[i:i + 4] = (0xFF000000).to_bytes(4, 'little')


    for i in range(10):
        for j in range(10):
            display.mlx.mlx_put_image_to_window(display.mlx_ptr, display.win, display.walls_png.img, display.walls_png.width * i, display.walls_png.height * j)


    mazegen = MazeGenerator((20, 20), False, (0, 0),
                                (1, 1), 1)
    for x in mazegen.maze:
        print(x)
    pos_y = 0
    for y in range(20):
        pos_y += 30
        pos_x = 0
        for x in range(20):
            pos_x += 30
            if mazegen.maze[y][x] == 15:
                pos_x += 15
                continue
            if not mazegen.maze[y][x] & 8:
                # print(x, y, "don't has left wall")
                display.mlx.mlx_put_image_to_window(display.mlx_ptr, display.win, display.corridor_img.img, pos_x, pos_y + 15)
            else:
                print(x, y, "has left wall")
            pos_x += 15
            if not mazegen.maze[y][x] & 1:
                # print(x, y, "don't has top wall")
                display.mlx.mlx_put_image_to_window(display.mlx_ptr, display.win, display.corridor_img.img, pos_x, pos_y)
            else:
                print(x, y, "has top wall")
            display.mlx.mlx_put_image_to_window(display.mlx_ptr, display.win, display.corridor_img.img, pos_x, pos_y + 15)
        pos_y += 15



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


        print()
        break
