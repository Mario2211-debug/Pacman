import json
from pathlib import Path

def open_json_file(filename: Path) -> Any:
    """ Read information from JSON file

    Args:
        filename (Path): address of the file

    Returns:
        Any: result of json.load()
    """
    try:
        with open(filename, "r") as f:
            try:
                return json.load(f)
            except Exception:
                print("\033[1;41mJSON parsing error\033[0m")
                print(f"\033[91m File \"{filename}\" "
                      "has wrong format.\033[0m")
                exit()
    except Exception as err:
        print(f"\033[91m{err}\033[0m")
        exit()