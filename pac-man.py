import sys
# import random
import time
from enum import Enum
import traceback

# from mazegenerator import MazeGenerator
# from src.types import Direction, GameStatus
from src.game import Game
# from engine.engine import Engine
# from engine.scenes.menu import MenuScene
from src.config import Config, open_config_file
from src.ghost import Ghost, Behavior as GhostBehavior
# from src.pacman import PacMan
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
        traceback.print_exc()

    # pacman = PacMan()
    # game.pacman = pacman
    # pacman.game = game

    ghosts = [Ghost("ghost_red"),
              Ghost("ghost_blue"),
              Ghost("ghost_orange"),
              Ghost("ghost_pink")]
    ghosts[1].set_behavior_standart(GhostBehavior.CORNERS)
    ghosts[2].set_behavior_standart(GhostBehavior.RANDOM)
    game.ghosts = ghosts
    for ghost in ghosts:
        ghost.game = game
        ghost.set_image(ghost.name + "_right")



    # def handle_close(display):
    #     display.mlx.mlx_loop_exit(display.mlx_ptr)

    # game.start()



    display.mlx.mlx_hook(display.win, 33, 0, game.exit, display)

    game.menu()

    # display.create_matrix("maze_matrix", 1000, 1000)
    # display.add_to_matrix("maze_matrix", "logo_big", 100, 100)
    # display.add_to_matrix("maze_matrix", "ghost_blue_right", 100, 100)
    # display.add_to_matrix("maze_matrix", "ghost_red_right", 150, 150)
    # display.show(display.images["maze_matrix"], 0, 0)


    # game.game_over()

    # display.mlx.mlx_loop_hook(display.mlx_ptr, game.menu, game)

    # Main loop
    display.mlx.mlx_loop(display.mlx_ptr)
    # ------------------------
    print("EXIT")

    exit()
