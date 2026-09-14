import sys
from src.ghost import Ghost
from src.display import Display
from engine.engine import Engine
from src.highscores import Highscores
from mazegenerator import MazeGenerator
from src.pacgum import pacgums_generate
from engine.scenes.menu import MenuScene
from src.pacman import PacMan, PacManDirection
from src.config import Config, open_config_file


# if __name__ == "__main__":
#     config_filename = ""
#     if len(sys.argv) == 2:
#         config_filename = sys.argv[1]
#     config_json = open_config_file(config_filename)
#     cfg = Config.model_validate(config_json)
#     engine = Engine(WIN_W, WIN_H, cfg, Highscores)
#     engine.set_scene(MenuScene(engine))
#     engine.run()

#     try:
#         display = Display()
#     except Exception as e:
#         print(e)
#         exit(1)

#     try:
#         display.load_all_images()
#         display.create_rectangle("block_42_img", display.corridor_width,
#                                  display.corridor_width, 0xAA000066)
#         display.create_rectangle("pacman_mask", display.images["pacman"].width,
#                                  display.images["pacman"].height, 0xFF000000)
#         display.create_rectangle("ghost_mask",
#                                  display.images["ghost_red"].width,
#                                  display.images["ghost_orange"].height + 5, 0xFF000000)
#     except Exception as e:
#         print(e)
#         exit(1)

#     display.clear_all()
#     display.show_filled_block(display.images["background1"], 0, 0,
#                               int(display.screen_width / display.images["background1"].width) + 1, int(display.screen_height / display.images["background1"].height) + 1)

#     display.show_filled_block(display.images["emptiness"],
#                               1300, 670, 15, 5, 4, 4)

#     display.show(display.images["logo"], 1350, 50)

#     display.create_text("Test text.\n0123456789\n!?+-=.:,", 1200, 350)

#     maze_width = 25
#     maze_height = 20

#     mazegen = MazeGenerator((maze_width, maze_height), False,
#                             (0, 0), (1, 1), cfg.seed)
#     # for x in mazegen.maze:
#     #     print(x)
#     pos_y = 0
#     for y in range(maze_height):
#         pos_y += display.corridor_width
#         pos_x = 0
#         for x in range(maze_width):
#             pos_x += display.corridor_width
#             if mazegen.maze[y][x] == 15:
#                 pos_x += display.wall_width
#                 display.show(display.images["block_42_img"], pos_x, pos_y + display.wall_width)
#                 continue

#             if not mazegen.maze[y][x] & 8:
#                 # print(x, y, "don't has left wall")
#                 display.show(display.images["emptiness"], pos_x, pos_y + display.wall_width)
#             pos_x += display.wall_width
#             if not mazegen.maze[y][x] & 1:
#                 # print(x, y, "don't has top wall")
#                 display.show(display.images["emptiness"], pos_x, pos_y)
#             display.show(display.images["emptiness"], pos_x, pos_y + display.wall_width)
#         pos_y += display.wall_width

#     pacman = PacMan()
#     pacman.display = display

#     ghosts = [Ghost(display.images["ghost_red"]),
#               Ghost(display.images["ghost_blue"]),
#               Ghost(display.images["ghost_orange"]),
#               Ghost(display.images["ghost_pink"])]
#     ghosts[0].set_start_position(0, 0)
#     ghosts[1].set_start_position(maze_width - 1, 0)
#     ghosts[2].set_start_position(0, maze_height - 1)
#     ghosts[3].set_start_position(maze_width - 1, maze_height - 1)
#     for ghost in ghosts:
#         ghost.set_maze(mazegen.maze)

#     pacgums = pacgums_generate(mazegen.maze, cfg.pacgum)
#     pacman.set_maze(mazegen.maze)
#     pacman.set_pacgums(pacgums)
#     pacman.set_start_position(0, 0, display.corridor_width + display.wall_width)

#     def gere_close_1(display):
#         display.mlx.mlx_loop_exit(display.mlx_ptr)

#     def gere_key_press(key, pacman):
#         print(f"Pressed key {key}")
#         if key == 119 or key == 65362:
#             pacman.direction_next = PacManDirection.TOP
#         elif key == 100 or key == 65363:
#             pacman.direction_next = PacManDirection.RIGHT
#         elif key == 115 or key == 65364:
#             pacman.direction_next = PacManDirection.BOTTOM
#         elif key == 97 or key == 65361:
#             pacman.direction_next = PacManDirection.LEFT

#     def make_turn(nothing):
#         shift_x = display.corridor_width + display.wall_width + 1
#         shift_y = display.corridor_width + display.wall_width + 1
#         # Clear old
#         pos_x = shift_x + pacman.x_px
#         pos_y = shift_y + pacman.y_px
#         display.show(display.images["pacman_mask"], pos_x, pos_y)

#         if pacman.direction == PacManDirection.RIGHT:
#             if pacman.x_px < pacman.next_x * (display.corridor_width + display.wall_width):
#                 pacman.x_px += pacman.speed
#             if pacman.x_px >= pacman.next_x * (display.corridor_width + display.wall_width):
#                 pacman.move()
#         elif pacman.direction == PacManDirection.LEFT:
#             if pacman.x_px > pacman.next_x * (display.corridor_width + display.wall_width):
#                 pacman.x_px -= pacman.speed
#             if pacman.x_px <= pacman.next_x * (display.corridor_width + display.wall_width):
#                 pacman.move()
#         elif pacman.direction == PacManDirection.TOP:
#             if pacman.y_px > pacman.next_y * (display.corridor_width + display.wall_width):
#                 pacman.y_px -= pacman.speed
#             if pacman.y_px <= pacman.next_y * (display.corridor_width + display.wall_width):
#                 pacman.move()
#         elif pacman.direction == PacManDirection.BOTTOM:
#             if pacman.y_px < pacman.next_y * (display.corridor_width + display.wall_width):
#                 pacman.y_px += pacman.speed
#             if pacman.y_px >= pacman.next_y * (display.corridor_width + display.wall_width):
#                 pacman.move()
#         pos_x = shift_x + pacman.x_px
#         pos_y = shift_y + pacman.y_px
#         display.show(display.images["pacman"], pos_x, pos_y)

#     display.mlx.mlx_hook(display.win, 33, 0, gere_close_1, display)
#     display.mlx.mlx_loop(display.mlx_ptr)

#     exit()
#     ghosts = [Ghost(1), Ghost(2), Ghost(3), Ghost(4)]
#     pacman = PacMan()

#     for lvl in cfg.level:
#         mazegen = MazeGenerator((lvl["width"], lvl["height"]), False, (0, 0),
#                                 (1, 1), cfg.seed)
#         for x in mazegen.maze:
#             print(x)

#         pacgums = pacgums_generate(mazegen.maze, cfg.pacgum)
#         print()
#         for x in pacgums:
#             print(x)

#         pacman.set_maze(mazegen.maze)
#         pacman.set_start_position(5, 5)

#         ghosts[0].set_start_position(0, 0)
#         ghosts[1].set_start_position(lvl["width"] - 1, 0)
#         ghosts[2].set_start_position(0, lvl["height"] - 1)
#         ghosts[3].set_start_position(lvl["width"] - 1, lvl["height"] - 1)


WIN_W = 700
WIN_H = 800

def main() -> None:
    args = [arg for arg in sys.argv[1:] if not arg.startswith("--")]
    config_filename = args[0] if args else ""
    cfg = Config.model_validate(open_config_file(config_filename))
    try:
        engine = Engine(WIN_W, WIN_H, cfg, Highscores(cfg.highscore_filename))
    except RuntimeError as err:
        print(f"\033[91m{err}\033[0m")
        sys.exit(1)
    engine.set_scene(MenuScene(engine))
    engine.run()


if __name__ == "__main__":
    main()
