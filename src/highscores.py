import json

def open_highscores_file(filename: str) -> None:
    try:
        with open(filename, "r") as f:
            # config_content = f.read()
            return json.loads(f.read())
    except FileNotFoundError as err:
        print("\033[91mHighscores file not found.\033[0m")
        return
    except PermissionError as err:
        print("\033[91mHighscores file can't be read.\033[0m")
        return
    except Exception as err:
        print("\033[91mHighscores file is invalid.\033[0m")
        return

def clear_highscores_file(filename: str) -> None:
    try:
        open(filename, 'w').close()
    except FileNotFoundError as err:
        print("\033[91mHighscores file not found.\033[0m")
        return
    except PermissionError as err:
        print("\033[91mHighscores file can't be write.\033[0m")
        return
    except Exception as err:
        print("\033[91mHighscores file is invalid.\033[0m")
        return
