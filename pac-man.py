import sys
import random
import time
from enum import Enum

from mazegenerator import MazeGenerator
from src.types import Direction, GameStatus
from src.game import Game
from engine.engine import Engine
from engine.scenes.menu import MenuScene
from src.config import Config, open_config_file
from src.ghost import Ghost
from src.pacman import PacMan
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

    game = Game()
    game.config = cfg

    try:
        display = Display()
    except Exception as e:
        print(e)
        exit(1)

    game.display = display

    try:
        display.load_all_images()
        display.create_rectangle("block_42_img", display.corridor_width, display.corridor_width, 0xAA000066)
        display.create_mask("pacman")
        display.create_mask("ghost_red")
        display.create_mask("ghost_blue")
        display.create_mask("ghost_orange")
        display.create_mask("ghost_pink")
        display.create_mask("ghost_dead")
        # display.create_rectangle("pacman_mask", display.images["pacman"].width, display.images["pacman"].height, 0xFF000000)
    except Exception as e:
        print(e)
        exit(1)

    # print(display.images["ghost_blue"].sl)
    # print(display.images["ghost_blue"].iformat)
    # exit()

    # for i in range(0, display.images["ghost_blue"].sl * display.images["ghost_blue"].width, 4):
    #     for j in (display.images["ghost_blue"].data[i: i + 4]):
    #         print("  ", j, end="")
    #     print()
    #     if i == display.images["ghost_blue"].sl * 4:
    #         print()

    # for i in range(3, display.images["ghost_blue"].sl * display.images["ghost_blue"].width, 4):
    #     print(display.images["ghost_blue"].data[i])

    # exit()


    maze_width = 25
    maze_height = 20

    mazegen = MazeGenerator((maze_width, maze_height), False, (0, 0), (1, 1), cfg.seed)
    game.set_maze(mazegen.maze)

    pacman = PacMan(display.images["pacman"], display.images["pacman_mask"])
    game.pacman = pacman
    pacman.game = game

    pacgums = pacgums_generate(mazegen.maze, cfg.pacgum)
    game.pacgums = pacgums
    pacman.set_start_position(maze_width // 2, maze_height // 2)

    ghosts = [Ghost(display.images["ghost_red"], display.images["ghost_red_mask"]),
              Ghost(display.images["ghost_blue"], display.images["ghost_blue_mask"]),
              Ghost(display.images["ghost_orange"], display.images["ghost_orange_mask"]),
              Ghost(display.images["ghost_pink"], display.images["ghost_pink_mask"])]
    for ghost in ghosts:
        ghost.game = game
    ghosts[0].set_start_position(0, 0)
    ghosts[1].set_start_position(maze_width - 1, 0)
    ghosts[2].set_start_position(0, maze_height - 1)
    ghosts[3].set_start_position(maze_width - 1, maze_height - 1)
    game.ghosts = ghosts


    display.clear_all()
    display.show_filled_block(display.images["background1"], 0, 0, int(display.screen_width / display.images["background1"].width) + 1, int(display.screen_height / display.images["background1"].height) + 1)

    display.show_filled_block(display.images["emptiness"], 1300, 670, 15, 5, 4, 4)

    display.show(display.images["logo"], 1350, 50)

    display.create_text("Test text.\n0123456789\n!?+-=.:,", 1200, 350)


    # display.show(display.images["pacman_mask"], 10, 10)
    # display.show(display.images["ghost_orange_mask"], 30, 10)

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
            if pacgums[y][x] == 1:
                display.show(display.images["."], pos_x + 5, pos_y + display.wall_width + 5)
            elif pacgums[y][x] == 2:
                display.show(display.images["+"], pos_x, pos_y + display.wall_width)

        pos_y += display.wall_width


    def handle_close(display):
        display.mlx.mlx_loop_exit(display.mlx_ptr)

    def handle_key_press(key, pacman):
        # print(f"Pressed key {key}")
        if key == 119 or key == 65362:
            pacman.direction_next = Direction.TOP
        elif key == 100 or key == 65363:
            pacman.direction_next = Direction.RIGHT
        elif key == 115 or key == 65364:
            pacman.direction_next = Direction.BOTTOM
        elif key == 97 or key == 65361:
            pacman.direction_next = Direction.LEFT

    def move_object(obj: PacMan | Ghost):
        shift_x = display.corridor_width + display.wall_width + 5
        shift_y = display.corridor_width + display.wall_width + 5
        # Clear old
        pos_x = shift_x + obj.x_px
        pos_y = shift_y + obj.y_px
        display.show(obj.mask, pos_x, pos_y)

        if obj.direction == Direction.RIGHT:
            # print(obj)
            if obj.x_px < obj.next_x * (display.corridor_width + display.wall_width):
                obj.x_px += obj.speed
            if obj.x_px >= obj.next_x * (display.corridor_width + display.wall_width):
                obj.move()
        elif obj.direction == Direction.LEFT:
            if obj.x_px > obj.next_x * (display.corridor_width + display.wall_width):
                obj.x_px -= obj.speed
            if obj.x_px <= obj.next_x * (display.corridor_width + display.wall_width):
                obj.move()
        elif obj.direction == Direction.TOP:
            if obj.y_px > obj.next_y * (display.corridor_width + display.wall_width):
                obj.y_px -= obj.speed
            if obj.y_px <= obj.next_y * (display.corridor_width + display.wall_width):
                obj.move()
        elif obj.direction == Direction.BOTTOM:
            if obj.y_px < obj.next_y * (display.corridor_width + display.wall_width):
                obj.y_px += obj.speed
            if obj.y_px >= obj.next_y * (display.corridor_width + display.wall_width):
                obj.move()

        #Show pacgum
        if type(obj) == Ghost:
            if pacgums[obj.y][obj.x] == 1:
                display.show(display.images["."], (obj.x + 1) * (display.corridor_width + display.wall_width) + 5, (obj.y + 1) * (display.corridor_width + display.wall_width) + 5)
            elif pacgums[obj.y][obj.x] == 2:
                display.show(display.images["+"], (obj.x + 1) * (display.corridor_width + display.wall_width) + 5, (obj.y + 1) * (display.corridor_width + display.wall_width) + 5)

        # Show new
        pos_x = shift_x + obj.x_px
        pos_y = shift_y + obj.y_px
        display.show(obj.image, pos_x, pos_y)


    def make_turn(nothing):
        if game.status != GameStatus.RUN:
            return
        move_object(pacman)
        for ghost in ghosts:
            move_object(ghost)
            if (pacman.x_px - pacman.image.width // 1.5 <= ghost.x_px <= pacman.x_px + pacman.image.width // 1.5
                and pacman.y_px - pacman.image.height // 1.5 <= ghost.y_px <= pacman.y_px + pacman.image.height // 1.5):
                print(f"!!!! CATCHED BY {ghost.image} at {ghost.x}, {ghost.y}")
                game.status = GameStatus.DEAD
                # exit()
        # time.sleep(0.5)



    display.mlx.mlx_hook(display.win, 33, 0, handle_close, display)  # WM_DELETE_WINDOW
    # display.mlx.mlx_key_hook(display.win, gere_key_press, pacman)
    display.mlx.mlx_hook(display.win, 2, 1, handle_key_press, pacman)

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

    # ghosts = [Ghost(1), Ghost(2), Ghost(3), Ghost(4)]
    # pacman = PacMan()

    # for lvl in cfg.level:
    #     mazegen = MazeGenerator((lvl["width"], lvl["height"]), False, (0, 0),
    #                             (1, 1), cfg.seed)
    #     for x in mazegen.maze:
    #         print(x)

    #     pacgums = pacgums_generate(mazegen.maze, cfg.pacgum)
    #     print()
    #     for x in pacgums:
    #         print(x)

    #     pacman.set_maze(mazegen.maze)
    #     pacman.set_pacgums(pacgums)
    #     pacman.set_start_position(lvl["width"] // 2, lvl["height"] // 2)

    #     ghosts[0].set_start_position(0, 0)
    #     ghosts[1].set_start_position(lvl["width"] - 1, 0)
    #     ghosts[2].set_start_position(0, lvl["height"] - 1)
    #     ghosts[3].set_start_position(lvl["width"] - 1, lvl["height"] - 1)

    #     # ghosts_positions: list = []
    #     for step in range(25):
    #         print("\nSPEP", step + 1)
    #         # pacman.move(PacManDirection.BOTTOM)
    #         pacman.move(random.choice(list(PacManDirection)))
    #         for ghost in ghosts:
    #             ghost.set_maze(mazegen.maze)
    #             # next_position = ghost.find_movement_to(3, 3, ghosts_positions)
    #             # ghosts_positions.append(next_position)
    #             ghost.move(ghosts, pacman)
    #             # print(f"\nGhost {ghost.image} position: {ghost.x}, {ghost.y}")
    #             # print("Next position:", next_position)
    #         # print("------------")

    #         print()
    #         print("   ", sep="", end="")
    #         for x in range(lvl["width"]):
    #             print(f"{x:<2}", sep="", end="")
    #         print("\n")
    #         for y in range(lvl["height"]):
    #             print(f"{y:<3}", sep="", end="")
    #             for x in range(lvl["width"]):
    #                 if pacman.x == x and pacman.y == y:
    #                     print("🟡", sep="", end="")
    #                     continue
    #                 for ghost in ghosts:
    #                     if ghost.x == x and ghost.y == y:
    #                         print("👻", sep="", end="")
    #                         break
    #                 else:
    #                     if mazegen.maze[y][x] == 15:
    #                         print("🟦", sep="", end="")
    #                     elif pacgums[y][x] == 1:
    #                         print("ㆍ", sep="", end="")
    #                     elif pacgums[y][x] == 2:
    #                         print("🔴", sep="", end="")
    #                     else:
    #                         # print("🟩", sep="", end="")
    #                         print("  ", sep="", end="")
    #             print()
    #         time.sleep(1)
    #         print("\n\n\n")


    #     print()
    #     break
