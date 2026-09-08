import sys
import json

from mazegenerator import MazeGenerator
# from src.parser import read_json_file

mazegen = MazeGenerator((15, 15), False, (0, 0), (10, 10), 42)

if __name__ == "__main__":
    # mazegen.generate()
    maze = mazegen.maze
    for x in maze:
        print(x)
    print()
    print(mazegen._shortest_path)

    mazegen._entryx, mazegen._entryy = 1, 1
    mazegen._exitx, mazegen._exity = 2, 2
    mazegen._find_short_path()
    print(mazegen._shortest_path)

    if len(sys.argv) == 2:
        try:
            with open(sys.argv[1], "r") as f:
                print(json.loads(f.read()))
        except Exception as err:
            print(err)