from engine.scenes.scene import Scene
from ..components.main import Main
from ..components.menu_list import MenuList
from utils.colors import Basic, Grays, Pacman, UI

MENU_W = 300


class MenuScene(Scene):
    def __init__(self, engine):
        super().__init__()
        self.engine = engine
        self.center_x = self.engine.win_w // 2

        # ========================= Components ================================
        self.main = Main(self.center_x - 200, 100, 400, 400, UI.DARK_SURFACE)
        self.menu = MenuList(self.center_x - MENU_W // 2, 200, MENU_W, [
            ("START GAME", self.start_game),
            ("HIGHSCORES", self.show_highscores),
            ("INSTRUCTIONS", self.show_instructions),
            ("EXIT", engine.onClose),
        ], bg_color=Basic.NAVY)

    def draw(self, renderer):
        self.main.draw(renderer)
        renderer.draw_text_centered("PAC-MAN", self.center_x, 135,
                                    Pacman.YELLOW)
        self.menu.draw(renderer)
        renderer.draw_text_centered("ARROWS + ENTER OR MOUSE",
                                    self.center_x, 450, Grays.GRAY_6)

    def handle_click(self, button, x, y):
        self.menu.handle_click(button, x, y)

    def handle_key(self, key):
        self.menu.handle_key(key)
        print("menu scene clisk")
        self.navbar.handle_click(button, x, y)

    def start_game(self):
        from engine.scenes.game import GameScene
        self.engine.set_scene(GameScene(self.engine))

    def show_highscores(self):
        from engine.scenes.highscores import HighscoresScene
        self.engine.set_scene(HighscoresScene(self.engine))

    def show_instructions(self):
        from engine.scenes.instructions import InstructionsScene
        self.engine.set_scene(InstructionsScene(self.engine))
