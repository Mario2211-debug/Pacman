import json
import os
from typing import Any

MAX_ENTRIES = 10
NAME_MAX_LENGTH = 10


class Highscores:
    """Top scores saved in a JSON file. Bad or missing files never crash."""

    def __init__(self, filename: str, max_entries: int = MAX_ENTRIES) -> None:
        self.filename = filename
        self.max_entries = max_entries
        self.entries: list[dict[str, Any]] = []
        self.load()

    @staticmethod
    def clean_name(name: str) -> str:
        # The MLX font only has ASCII glyphs
        chars = (c for c in name.upper() if c.isascii() and c.isalnum())
        return "".join(chars)[:NAME_MAX_LENGTH]

    def load(self) -> None:
        self.entries = []
        try:
            with open(self.filename, "r") as f:
                data = json.load(f)
        except FileNotFoundError:
            return
        except (OSError, ValueError) as err:
            print(f"\033[91mHighscores file can't be read: {err}")
            print("Starting with an empty list.\033[0m")
            return

        if not isinstance(data, list):
            print("\033[91mHighscores file has an invalid format.")
            print("Starting with an empty list.\033[0m")
            return

        for item in data:
            if not isinstance(item, dict):
                continue
            name = item.get("name")
            score = item.get("score")
            if (not isinstance(name, str) or not isinstance(score, int)
                    or isinstance(score, bool) or score < 0):
                continue
            name = self.clean_name(name)
            if name:
                self.entries.append({"name": name, "score": score})
        self._sort()

    def _sort(self) -> None:
        # Stable sort: on a tie the older score keeps the better rank
        self.entries.sort(key=lambda entry: entry["score"], reverse=True)
        del self.entries[self.max_entries:]

    def qualifies(self, score: int) -> bool:
        return (len(self.entries) < self.max_entries
                or score > self.entries[-1]["score"])

    def add(self, name: str, score: int) -> bool:
        """Adds the score if it enters the top and saves the file.
        Returns True if the score entered the top."""
        name = self.clean_name(name)
        if not name or score < 0 or not self.qualifies(score):
            return False
        self.entries.append({"name": name, "score": score})
        self._sort()
        self.save()
        return True

    def save(self) -> bool:
        tmp_filename = self.filename + ".tmp"
        try:
            with open(tmp_filename, "w") as f:
                json.dump(self.entries, f, indent=4)
            os.replace(tmp_filename, self.filename)
        except OSError as err:
            print(f"\033[91mHighscores can't be saved: {err}\033[0m")
            return False
        return True
