from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .game import Game

class Stats:
    def __init__(self, game: Game) -> None:
        self.stats = {"level": 1,
                      "score": 0,
                      "lives": 0,
                      "time": 90}
        # self.level = 1
        # self.lives = 0
        # self.score = 0
        # self.time = 0
        self.game: Game = game
        self.windows = {"level": self.Window("Level", 1400, 200, "level", game),
                        "score": self.Window("Score", 1400, 400, "score", game),
                        "lives": self.Window("Lives", 1400, 600, "lives", game),
                        "time": self.Window("Time", 1400, 800, "time", game)}

    class Window:
        def __init__(self, text: str, x: int, y: int, stat: str, game: Game) -> None:
            self.text = text
            self.x = x
            self.y = y
            self.stat = stat
            self.game: Game = game

        def show_window(self) -> None:
            self.game.display.show_text(self.text, self.x, self.y, "left", "maze_screen")
            self.update_window()

        def update_window(self) -> None:
            self.game.display.show_filled_block(self.game.display.images["emptiness"], self.x, self.y + 50, 13, 2, 4, 4, "maze_screen")
            # self.game.display.show(self.game.display.images["stat_window"], self.x, self.y + 70)
            if self.stat != "lives":
                if self.stat == "score" and self.game.stats.stats["score"] > 999999999999999:
                    self.game.display.show_text("999999999999999", self.x + 15, self.y + 67, "left", "maze_screen")
                else:
                    self.game.display.show_text(str(self.game.stats.stats[self.stat]), self.x + 15, self.y + 67, "left", "maze_screen")
            else:
                for i in range(self.game.stats.stats["lives"]):
                    # self.game.display.show(self.game.display.images["pacman_right"], self.x + (self.game.display.images["pacman_right"].width + 10) * i, self.y + 75)
                    self.game.display.add_to_bitmap("maze_screen", "pacman_3_right", self.x + (self.game.display.images["pacman_3_right"].width + 13) * i + 15, self.y + 70)

    def show_stats(self) -> None:
        if not self.game.display:
            return
        for window in self.windows.values():
            window.show_window()

    def reset_stats(self) -> None:
        self.stats["level"] = 1
        self.stats["score"] = 0
        self.reset_time()
        self.stats["lives"] = self.game.config.lives
        self.stats["time"] = self.game.config.level_max_time

    def increase_score(self, num: int = 1) -> None:
        self.stats["score"] += num
        self.windows["score"].update_window()

    def increase_time(self, num: int = 1) -> None:
        self.stats["time"] += num
        self.windows["time"].update_window()

    def reset_time(self, num: int = 1) -> None:
        self.stats["time"] = self.game.config.level_max_time

    def increase_lives(self, num: int = 1) -> None:
        self.stats["lives"] += num
        if self.stats["lives"] > 10:
            self.stats["lives"] = 10
        else:
            self.windows["lives"].update_window()

    def increase_level(self, num: int = 1) -> None:
        self.stats["level"] += num
        if self.stats["level"] > 999999999999999:
            self.stats["level"] = 999999999999999
        # self.windows["level"].update_window()