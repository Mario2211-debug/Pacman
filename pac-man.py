import sys

from mazegenerator import MazeGenerator
from src.config import Config, open_config_file


if __name__ == "__main__":
    config_filename = ""
    if len(sys.argv) == 2:
        config_filename = sys.argv[1]
    config_json = open_config_file(config_filename)
    cfg = Config.model_validate(config_json)
    # print(cfg)

    for lvl in cfg.level:
        mazegen = MazeGenerator((lvl["width"], lvl["height"]), False, (0, 0), (1, 1), cfg.seed)
        for x in mazegen.maze:
            print(x)
        print()
