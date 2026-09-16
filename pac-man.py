import sys
# import random
# import time
from enum import Enum

from mazegenerator import MazeGenerator
from src.types import Direction, GameStatus
from src.game import Game
from engine.engine import Engine
from engine.scenes.menu import MenuScene
from src.config import Config, open_config_file
from src.ghost import Ghost, Behavior as GhostBehavior
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
    display.game = game
    try:
        display.load_all_images()
        display.create_rectangle("block_42_img", display.corridor_width, display.corridor_width, 0xAA000066)
        # display.create_rectangle("pacman_mask", display.images["pacman"].width, display.images["pacman"].height, 0xFF000000)
    except Exception as e:
        print(e)
        exit(1)

    maze_width = 25
    maze_height = 20

    mazegen = MazeGenerator((maze_width, maze_height), False, (0, 0), (1, 1), cfg.seed)
    game.set_maze(mazegen.maze)

    pacman = PacMan()
    game.pacman = pacman
    pacman.game = game
    pacman.set_image("pacman_right")
    pacman.set_start_position(maze_width // 2, maze_height // 2)

    pacgums = pacgums_generate(mazegen.maze, cfg.pacgum)
    game.pacgums = pacgums

    ghosts = [Ghost("ghost_red"),
              Ghost("ghost_blue"),
              Ghost("ghost_orange"),
              Ghost("ghost_pink")]
    for ghost in ghosts:
        ghost.game = game
        ghost.set_image(ghost.name + "_right")
    game.ghosts = ghosts

    ghosts[0].set_start_position(0, 0)
    ghosts[1].set_start_position(maze_width - 1, 0)
    ghosts[1].set_behavior(GhostBehavior.CORNERS)
    ghosts[2].set_start_position(0, maze_height - 1)
    ghosts[2].set_behavior(GhostBehavior.RANDOM)
    ghosts[3].set_start_position(maze_width - 1, maze_height - 1)


    # display.clear_window()
    display.show_filled_block(display.images["background1"], 0, 0, display.screen_width // display.images["background1"].width + 1, display.screen_height // display.images["background1"].height + 1)

    # display.show_filled_block(display.images["emptiness"], 1300, 670, 15, 5, 4, 4)

    display.show(display.images["logo_small"], 1350, 50)

    # display.show_text("Test text.\n0123456789\n!?+-=.:,", 1200, 350)

    game.display.show_maze()

    # def handle_close(display):
    #     display.mlx.mlx_loop_exit(display.mlx_ptr)

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
            obj.set_image(obj.name + "_right")
            if obj.x_px < obj.next_x * (display.corridor_width + display.wall_width):
                obj.x_px += obj.speed
            if obj.x_px >= obj.next_x * (display.corridor_width + display.wall_width):
                obj.move()
        elif obj.direction == Direction.LEFT:
            obj.set_image(obj.name + "_left")
            if obj.x_px > obj.next_x * (display.corridor_width + display.wall_width):
                obj.x_px -= obj.speed
            if obj.x_px <= obj.next_x * (display.corridor_width + display.wall_width):
                obj.move()
        elif obj.direction == Direction.TOP:
            if type(obj) == PacMan:
                obj.set_image("pacman_top")
            if obj.y_px > obj.next_y * (display.corridor_width + display.wall_width):
                obj.y_px -= obj.speed
            if obj.y_px <= obj.next_y * (display.corridor_width + display.wall_width):
                obj.move()
        elif obj.direction == Direction.BOTTOM:
            if type(obj) == PacMan:
                obj.set_image("pacman_bottom")
            if obj.y_px < obj.next_y * (display.corridor_width + display.wall_width):
                obj.y_px += obj.speed
            if obj.y_px >= obj.next_y * (display.corridor_width + display.wall_width):
                obj.move()

        #Show pacgum
        if type(obj) == Ghost:
            if pacgums[obj.y][obj.x] == 1:
                game.display.show_pacgum(obj.x, obj.y, "small")
            elif pacgums[obj.y][obj.x] == 2:
                game.display.show_pacgum(obj.x, obj.y, "big")

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
                print(f"!!!! CATCHED BY {ghost.name} at {ghost.x}, {ghost.y}")
                game.status = GameStatus.DEAD
                # exit()
        # time.sleep(0.5)



    display.mlx.mlx_hook(display.win, 33, 0, game.exit, display)
    display.mlx.mlx_hook(display.win, 2, 1, handle_key_press, pacman)

    display.mlx.mlx_loop_hook(display.mlx_ptr, make_turn, None)

    game.menu()
    # game.pause()
    # display.mlx.mlx_loop_hook(display.mlx_ptr, game.menu, game)

    # Main loop
    display.mlx.mlx_loop(display.mlx_ptr)
    # ------------------------
    print("EXIT")

    exit()
