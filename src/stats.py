from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .game import Game

class Stats:
    def __init__(self, game: Game) -> None:
        self.stats = {"level": 1,
                      "score": 0,
                      "lives": 0,
                      "time": 0}
        # self.level = 1
        # self.lives = 0
        # self.score = 0
        # self.time = 0
        self.game: Game = game
        self.windows = {"level": self.Window("Level", 1300, 200, "level", game),
                        "score": self.Window("Score", 1300, 400, "score", game),
                        "lives": self.Window("Lives", 1300, 600, "lives", game),
                        "time": self.Window("Time", 1300, 800, "time", game)}

    class Window:
        def __init__(self, text: str, x: int, y: int, stat: str, game: Game) -> None:
            self.text = text
            self.x = x
            self.y = y
            self.stat = stat
            self.game: Game = game

        def show_window(self) -> None:
            self.game.display.show_text(self.text, self.x, self.y)
            self.game.display.show_filled_block(self.game.display.images["emptiness"], self.x, self.y + 70, 10, 2, 4, 4)
            self.game.display.show_text(str(self.game.stats.stats[self.stat]), self.x, self.y + 75)

        def update_window(self) -> None:
            self.game.display.show_filled_block(self.game.display.images["emptiness"], self.x, self.y + 70, 10, 2, 4, 4)
            self.game.display.show_text(str(self.game.stats.stats[self.stat]), self.x, self.y + 75)

    def show_stats(self):
        if not self.game.display:
            return
        for window in self.windows.values():
            window.show_window()

    def reset_stats(self):
        for stat in self.stats.keys():
            self.stats[stat] = 0

    def increase_score(self, num):
        self.stats["score"] += num
        self.windows["score"].update_window()