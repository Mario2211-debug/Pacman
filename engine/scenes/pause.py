from engine import keys
from engine.scenes.scene import Scene
from ..components.main import Main
from ..components.menu_list import MenuList
from utils.colors import Basic, Pacman, UI

PANEL_W = 340
PANEL_H = 240
MENU_W = 260


class PauseScene(Scene):
    def __init__(self, engine, game_scene):
        super().__init__()
        self.engine = engine
        self.game_scene = game_scene
        self.center_x = engine.win_w // 2
        panel_y = (engine.win_h - PANEL_H) // 2

        # ========================= Components ================================
        self.main = Main(self.center_x - PANEL_W // 2, panel_y,
                         PANEL_W, PANEL_H, UI.DARK_SURFACE)
        self.menu = MenuList(self.center_x - MENU_W // 2, panel_y + 80,
                             MENU_W, [
                                 ("RESUME", self.resume),
                                 ("MAIN MENU", self.main_menu),
                             ], bg_color=Basic.NAVY)

    def draw(self, renderer):
        self.game_scene.draw(renderer)
        self.main.draw(renderer)
        renderer.draw_rect(self.main.x, self.main.y, self.main.width,
                           self.main.height, Pacman.YELLOW, 2)
        renderer.draw_text_centered("PAUSED", self.center_x,
                                    self.main.y + 30, Pacman.YELLOW)
        self.menu.draw(renderer)

    def handle_click(self, button, x, y):
        self.menu.handle_click(button, x, y)

    def handle_key(self, key):
        if key in keys.PAUSE:
            self.resume()
        else:
            self.menu.handle_key(key)

    def resume(self):
        self.engine.set_scene(self.game_scene)

    def main_menu(self):
        from engine.scenes.menu import MenuScene
        self.engine.set_scene(MenuScene(self.engine))
