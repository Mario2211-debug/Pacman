from engine import keys
from engine.scenes.scene import Scene
from ..components.main import Main
from ..components.menu_list import MenuList
from utils.colors import Basic, Grays, Pacman, UI

PANEL_W = 640
LINE_H = 28


class InstructionsScene(Scene):
    def __init__(self, engine):
        super().__init__()
        self.engine = engine
        self.center_x = engine.win_w // 2
        cfg = engine.config

        # ========================= Components ================================
        self.main = Main(self.center_x - PANEL_W // 2, 40, PANEL_W, 520,
                         UI.DARK_SURFACE)
        self.menu = MenuList(self.center_x - 100, 500, 200,
                             [("BACK", self.back)], bg_color=Basic.NAVY)

        title, text = Pacman.YELLOW, Basic.WHITE
        self.lines = [
            ("CONTROLS", title),
            ("ARROWS / WASD   MOVE", text),
            ("ESC / P         PAUSE", text),
            ("", text),
            ("RULES", title),
            ("EAT ALL PACGUMS TO CLEAR THE LEVEL", text),
            (f"PACGUM          +{cfg.points_per_pacgum}", text),
            (f"SUPER PACGUM    +{cfg.points_per_super_pacgum}"
             ", GHOSTS BECOME EDIBLE", text),
            (f"EDIBLE GHOST    +{cfg.points_per_ghost}", text),
            ("GHOST TOUCH     -1 LIFE", text),
            (f"TIME OUT        -1 LIFE ({cfg.level_max_time}s PER LEVEL)",
             text),
            (f"{len(cfg.level)} LEVELS, {cfg.lives} LIVES", Grays.GRAY_7),
        ]

    def draw(self, renderer):
        self.main.draw(renderer)
        left = self.center_x - PANEL_W // 2 + 40
        for i, (line, color) in enumerate(self.lines):
            renderer.draw_text(line, left, 70 + i * LINE_H, color)
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
