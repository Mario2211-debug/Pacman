import json

def open_highscores_file(filename: str) -> None:
    try:
        with open(filename, "r") as f:
            return json.loads(f.read())
    # except FileNotFoundError as err:
    #     print("\033[91mHighscores file not found.\033[0m")
    #     return
    # except PermissionError as err:
    #     print("\033[91mHighscores file can't be read.\033[0m")
    #     return
    except Exception as err:
        open(filename, 'w').close()
        # print("\033[91mHighscores file is invalid.\033[0m")
        return

def save_to_highscores_file(filename: str, record: dict) -> None:
    try:
        highscores_json = open_highscores_file(filename)
    except Exception as err:
        open(filename, 'w').close()
        # print("\033[91mHighscores file is invalid.\033[0m")
    finally:
        if not highscores_json:
            highscores_json = []
        highscores_json.append(record)
        try:
            with open(filename, "w+") as f:
                f.write(json.dumps(highscores_json, indent=2, ensure_ascii=False))
                # print(f"\033[93mResult saved in \"{filename}\"\033[0m")
        except Exception as err:
            print(f"\033[91m{err}\033[0m")
            exit()


def clear_highscores_file(filename: str) -> None:
    try:
        open(filename, 'w').close()
    # except FileNotFoundError as err:
    #     print("\033[91mHighscores file not found.\033[0m")
    #     return
    # except PermissionError as err:
    #     print("\033[91mHighscores file can't be write.\033[0m")
    #     return
    except Exception as err:
        # print("\033[91mHighscores file is invalid.\033[0m")
        return
