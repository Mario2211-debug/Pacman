from engine.scenes.scene import Scene
from ..components.navbar import Navbar
from ..components.buttons import Button
from ..components.text import Text
from utils.colors import Basic


class GameScene(Scene):
    def __init__(self, engine):
        super().__init__()
        self.engine = engine
        self.navbar = Navbar(2, 2, 800, 10, 0x1A1A1AFF)

        # ========================= Components ================================
        text_color = Basic.RED
        self.navbar.add(Text(200, 2, "Pacman", text_color))
        self.navbar.add(Button(140, 2, on_click=engine.onClose).add(Text(200, 2, "PAUSE", text_color)))

    def draw(self, renderer):
        print("Menu draw")
        self.navbar.draw(renderer)

    def handle_click(self, button, x, y):
        self.navbar.handle_click(button, x, y)

    def start_game(self):
        print("start game")
        #from game_scene import GameScene
        #self.engine.set_scene(GameScene(self.engine))