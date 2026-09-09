import sys

from mazegenerator import MazeGenerator
from src.config import Config, open_config_file

mazegen = MazeGenerator((15, 15), False, (0, 0), (10, 10), 42)

if __name__ == "__main__":
    # mazegen.generate()
    maze = mazegen.maze
    # for x in maze:
        # print(x)
    # print()
    # print(mazegen._shortest_path)

    mazegen._entryx, mazegen._entryy = 1, 1
    mazegen._exitx, mazegen._exity = 2, 2
    mazegen._find_short_path()
    # print(mazegen._shortest_path)

    config_filename = ""
    if len(sys.argv) == 2:
        config_filename = sys.argv[1]
    config_json = open_config_file(config_filename)
    cfg = Config.model_validate(config_json)
    print()
    print()
    print(cfg)
