import sys
# import traceback

from src.game import Game
from src.config import Config, open_config_file
from src.ghost import Ghost
from src.game_types import GhostBehavior
from src.display import Display

if __name__ == "__main__":
    config_filename = ""
    if len(sys.argv) == 2:
        config_filename = sys.argv[1]
    config_json = open_config_file(config_filename)
    cfg = Config.model_validate(config_json)

    game = Game(cfg)

    try:
        display = Display()
    except Exception:
        print("\033[91mAn unexpected error occured.\033[0m")
        # print(e)
        exit(1)

    game.display = display
    display.game = game

    try:
        display.load_all_images()
    except Exception:
        # print(e)
        print("\033[91mAn unexpected error occured.\033[0m")
        exit(1)
        # traceback.print_exc()

    try:
        ghosts = [Ghost("ghost_red"),
                  Ghost("ghost_blue"),
                  Ghost("ghost_orange"),
                  Ghost("ghost_pink")]
        ghosts[1].set_behavior_default(GhostBehavior.CORNERS)
        ghosts[2].set_behavior_default(GhostBehavior.RANDOM)
        game.ghosts = ghosts
        for ghost in ghosts:
            ghost.game = game
            ghost.set_image("right")

        display.mlx.mlx_hook(display.win, 33, 0, game.exit, display)
        display.mlx.mlx_do_key_autorepeatoff(display.mlx_ptr)
        display.mlx.mlx_mouse_hide(display.mlx_ptr)
        game.create_save_score_templates()
        game.menu()

        display.mlx.mlx_loop(display.mlx_ptr)
    except Exception:
        # print(e)
        print("\033[91mAn unexpected error occured.\033[0m")
        exit(1)
