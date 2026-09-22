"""Persistent highscore file: read, append and reset."""

import json
from typing import Any


def open_highscores_file(filename: str) -> Any:
    """Read the highscores, dropping invalid records.

    Returns None and empties the file when it cannot be parsed.
    """
    try:
        with open(filename, "r") as f:
            highscores_json = json.loads(f.read())
            i = 0
            while i < len(highscores_json):
                if (highscores_json[i].get("name") is None
                        or highscores_json[i].get("name") == ""
                        or highscores_json[i].get("score") is None
                        or highscores_json[i].get("score") == 0):
                    highscores_json.pop(i)
                    continue
                i += 1
            # print(highscores_json)
            return highscores_json
    # except FileNotFoundError as err:
    #     print("\033[91mHighscores file not found.\033[0m")
    #     return
    # except PermissionError as err:
    #     print("\033[91mHighscores file can't be read.\033[0m")
    #     return
    except Exception:
        clear_highscores_file(filename)
        return None


def save_to_highscores_file(filename: str,
                            record: dict[Any, Any]) -> None:
    """Append one record to the highscore file."""
    highscores_json = None
    try:
        highscores_json = open_highscores_file(filename)
    except Exception:
        clear_highscores_file(filename)

    if not highscores_json:
        highscores_json = []
    highscores_json.append(record)
    try:
        with open(filename, "w+") as f:
            f.write(json.dumps(highscores_json,
                               indent=2,
                               ensure_ascii=False))
    except Exception:
        print("\033[91mError occured during saving scores.\033[0m")


def clear_highscores_file(filename: str) -> None:
    """Empty the highscore file."""
    try:
        with open(filename, "w"):
            pass
    # except FileNotFoundError as err:
    #     print("\033[91mHighscores file not found.\033[0m")
    #     return
    # except PermissionError as err:
    #     print("\033[91mHighscores file can't be write.\033[0m")
    #     return
    except Exception:
        # print("\033[91mHighscores file is invalid.\033[0m")
        return
