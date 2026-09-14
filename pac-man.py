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
from src.display import Display

WIN_W = 800
WIN_H = 600


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
        display.load_all_images()
        display.create_rectangle("block_42_img", display.corridor_width, display.corridor_width, 0xAA000066)
        display.create_rectangle("pacman_mask", display.images["pacman"].width, display.images["pacman"].height, 0xFF000000)
        display.create_rectangle("ghost_mask", display.images["ghost_red"].width, display.images["ghost_orange"].height + 5, 0xFF000000)
    except Exception as e:
        print(e)
        exit(1)

    display.clear_all()
    display.show_filled_block(display.images["background1"], 0, 0, int(display.screen_width / display.images["background1"].width) + 1, int(display.screen_height / display.images["background1"].height) + 1)

    display.show_filled_block(display.images["emptiness"], 1300, 670, 15, 5, 4, 4)

    display.show(display.images["logo"], 1350, 50)

    display.create_text("Test text.\n0123456789\n!?+-=.:,", 1200, 350)


    maze_width = 25
    maze_height = 20

    mazegen = MazeGenerator((maze_width, maze_height), False, (0, 0), (1, 1), cfg.seed)
    # for x in mazegen.maze:
    #     print(x)
    pos_y = 0
    for y in range(maze_height):
        pos_y += display.corridor_width
        pos_x = 0
        for x in range(maze_width):
            pos_x += display.corridor_width
            if mazegen.maze[y][x] == 15:
                pos_x += display.wall_width
                display.show(display.images["block_42_img"], pos_x, pos_y + display.wall_width)
                continue

            if not mazegen.maze[y][x] & 8:
                # print(x, y, "don't has left wall")
                display.show(display.images["emptiness"], pos_x, pos_y + display.wall_width)
            pos_x += display.wall_width
            if not mazegen.maze[y][x] & 1:
                # print(x, y, "don't has top wall")
                display.show(display.images["emptiness"], pos_x, pos_y)
            display.show(display.images["emptiness"], pos_x, pos_y + display.wall_width)
        pos_y += display.wall_width

    pacman = PacMan()

    ghosts = [Ghost(display.images["ghost_red"]),
              Ghost(display.images["ghost_blue"]),
              Ghost(display.images["ghost_orange"]),
              Ghost(display.images["ghost_pink"])]
    ghosts[0].set_start_position(0, 0)
    ghosts[1].set_start_position(maze_width - 1, 0)
    ghosts[2].set_start_position(0, maze_height - 1)
    ghosts[3].set_start_position(maze_width - 1, maze_height - 1)
    for ghost in ghosts:
        ghost.set_maze(mazegen.maze)

    pacgums = pacgums_generate(mazegen.maze, cfg.pacgum)
    pacman.set_maze(mazegen.maze)
    pacman.set_pacgums(pacgums)
    pacman.set_start_position(10, 10)

    def gere_close_1(display):
        display.mlx.mlx_loop_exit(display.mlx_ptr)

    def gere_key_press(key, pacman):
        print(f"Pressed key {key}")
        if key == 119:
            pacman.direction = PacManDirection.TOP
        elif key == 100:
            pacman.direction = PacManDirection.RIGHT
        elif key == 115:
            pacman.direction = PacManDirection.BOTTOM
        elif key == 97:
            pacman.direction = PacManDirection.LEFT

    def make_turn(nothing):
        shift_x = display.corridor_width + display.wall_width + 1
        shift_y = display.corridor_width + display.wall_width + 1
        # Clear old
        pos_x = shift_x + pacman.x * (display.corridor_width + display.wall_width) + int(display.corridor_width / 2) - int(display.images["pacman"].width / 2)
        pos_y = shift_y + pacman.y * (display.corridor_width + display.wall_width) + int(display.corridor_width / 2) - int(display.images["pacman"].height / 2)
        display.show(display.images["pacman_mask"], pos_x, pos_y)
        # Show new
        # pacman.move(random.choice(list(PacManDirection)))
        # print(pacman.direction)
        pacman.move(pacman.direction)
        pos_x = shift_x + pacman.x * (display.corridor_width + display.wall_width) + int(display.corridor_width / 2) - int(display.images["pacman"].width / 2)
        pos_y = shift_y + pacman.y * (display.corridor_width + display.wall_width) + int(display.corridor_width / 2) - int(display.images["pacman"].height / 2)
        display.show(display.images["pacman"], pos_x, pos_y)

        for ghost in ghosts:
        # Clear old
            pos_x = shift_x + ghost.x * (display.corridor_width + display.wall_width) + int(display.corridor_width / 2) - int(ghost.image.width / 2)
            pos_y = shift_y + ghost.y * (display.corridor_width + display.wall_width) + int(display.corridor_width / 2) - int(ghost.image.height / 2)
            display.show(display.images["ghost_mask"], pos_x, pos_y)
            # Show new
            ghost.move(ghosts, pacman)
            pos_x = shift_x + ghost.x * (display.corridor_width + display.wall_width) + int(display.corridor_width / 2) - int(ghost.image.width / 2)
            pos_y = shift_y + ghost.y * (display.corridor_width + display.wall_width) + int(display.corridor_width / 2) - int(ghost.image.height / 2)
            display.show(ghost.image, pos_x, pos_y)


            display.mlx.mlx_hook(display.win, 33, 0, gere_close_1, display)  # WM_DELETE_WINDOW
            display.mlx.mlx_key_hook(display.win, gere_key_press, pacman)
        time.sleep(0.5)

    display.mlx.mlx_loop_hook(display.mlx_ptr, make_turn, None)

    # Main loop
    display.mlx.mlx_loop(display.mlx_ptr)
    # ------------------------

    #
    # python3 -c "from PIL import Image; Image.open('img/walls_100.png').convert('RGB').save('img/walls_100_new.png')"
    #

    # !!!!!!!!!!!!!
    # mlx.mlx_destroy_image(mlx_ptr, img_ptr)
    # !!!!!!!!!!!!!

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
