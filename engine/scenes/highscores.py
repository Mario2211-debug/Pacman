from engine import keys
from engine.render import CHAR_W
from engine.scenes.scene import Scene
from ..components.main import Main
from ..components.menu_list import MenuList
from utils.colors import Basic, Grays, Pacman, UI

PANEL_W = 440
ROW_H = 34


class HighscoresScene(Scene):
    def __init__(self, engine):
        super().__init__()
        self.engine = engine
        self.center_x = engine.win_w // 2

        # ========================= Components ================================
        self.main = Main(self.center_x - PANEL_W // 2, 50, PANEL_W, 500,
                         UI.DARK_SURFACE)
        self.menu = MenuList(self.center_x - 100, 480, 200,
                             [("BACK", self.back)], bg_color=Basic.NAVY)

    def draw(self, renderer):
        self.main.draw(renderer)
        renderer.draw_text_centered("HIGHSCORES", self.center_x, 70,
                                    Pacman.YELLOW)

        entries = self.engine.highscores.entries
        if not entries:
            renderer.draw_text_centered("NO SCORES YET", self.center_x, 250,
                                        Grays.GRAY_6)

        left = self.center_x - PANEL_W // 2 + 30
        right = self.center_x + PANEL_W // 2 - 30
        for i, entry in enumerate(entries):
            y = 120 + i * ROW_H
            color = Pacman.YELLOW if i == 0 else Basic.WHITE
            score = str(entry["score"])
            renderer.draw_text(f"{i + 1:2d}.", left, y, color)
            renderer.draw_text(entry["name"], left + 60, y, color)
            renderer.draw_text(score, right - len(score) * CHAR_W, y, color)

        self.menu.draw(renderer)

    def handle_click(self, button, x, y):
        self.menu.handle_click(button, x, y)

    def handle_key(self, key):
        if key == keys.ESCAPE:
            self.back()
        else:
            self.menu.handle_key(key)

    def back(self):
        from engine.scenes.menu import MenuScene
        self.engine.set_scene(MenuScene(self.engine))
