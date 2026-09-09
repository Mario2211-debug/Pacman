import sys
import json

from mazegenerator import MazeGenerator
from src.config import Config

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

    if len(sys.argv) == 2:
        try:
            with open(sys.argv[1], "r") as f:
                config_content = f.readlines()
                lines = "".join(line for line in config_content if not line.lstrip().startswith('#'))
                json_lines = json.loads(lines)
                # print(json_lines)
                cfg = Config.model_validate(json_lines)
                print()
                print()
                print(cfg)

        except Exception as err:
            print("ERROR")
            print(f"\033[91m{err}\033[0m")