import sys

from mazegenerator import MazeGenerator
from src.config import Config, open_config_file
from src.ghost import Ghost


if __name__ == "__main__":
    config_filename = ""
    if len(sys.argv) == 2:
        config_filename = sys.argv[1]
    config_json = open_config_file(config_filename)
    cfg = Config.model_validate(config_json)
    # print(cfg)

    for lvl in cfg.level:
        mazegen = MazeGenerator((lvl["width"], lvl["height"]), False, (0, 0), (1, 1), cfg.seed)
        ghost1 = Ghost(None, 0, 0)
        ghost2 = Ghost(None, lvl["width"] - 1, 0)
        ghost3 = Ghost(None, 0, lvl["height"] - 1)
        ghost4 = Ghost(None, lvl["width"] - 1, lvl["height"] - 1)
        print("Ghost 1:", ghost1.x, ghost1.y)
        print("Ghost 2:", ghost2.x, ghost2.y)
        print("Ghost 3:", ghost3.x, ghost3.y)
        print("Ghost 4:", ghost4.x, ghost4.y)
        for x in mazegen.maze:
            print(x)
        print()
