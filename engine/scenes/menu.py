from engine.scenes.scene import Scene
# from ..components.navbar import Navbar
from ..components.buttons import Button
from ..components.main import Main
from ..components.text import Text
from utils.colors import Basic


class MenuScene(Scene):
    def __init__(self, engine):
        super().__init__()
        self.engine = engine
        self.center_x = self.engine.win_w // 2
        self.center_y = self.engine.win_h // 2

        # ========================= Components ================================
        main_color = Basic.BLUE
        main_txt_color = Basic.YELLOW
        main_w = (self.engine.win_w - 200) - 1
        main_h = (self.engine.win_h - 200) - 1

        self.main = Main(self.center_x - (main_w // 2),
                         self.center_y - main_h // 2,
                         main_w,
                         main_h,
                         main_color)
        self.main.add(Text(200, 400, "MAIN", main_txt_color))

        # navbar_color = Basic.RED
        # navbar_txt_color = Basic.WHITE
        # self.navbar = Navbar(359, 2, 600, 80, navbar_color)
        # self.navbar.add(Text(200, 2, "Pacman", navbar_txt_color))

        btn_start_color = Basic.YELLOW
        self.quit_button = Button(140, 2, on_click=engine.onClose)
        self.quit_button.add(Text(200, 2, "QUIT", btn_start_color))

        btn_quit_color = Basic.GREEN
        self.start_button = Button(140, 2, on_click=engine.onClose)
        self.start_button.add(Text(200, 2, "START", btn_quit_color))

    def draw(self, renderer):
        # self.navbar.draw(renderer)
        self.main.draw(renderer)
        self.start_button.draw(renderer)
        self.quit_button.draw(renderer)

    def handle_click(self, button, x, y):
        self.main.handle_click(button, x, y)

    def start_game(self):
        print("start game")
        from engine.scenes.game import GameScene
        self.engine.set_scene(GameScene(self.engine))
