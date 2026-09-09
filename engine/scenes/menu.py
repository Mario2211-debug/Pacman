from engine.scenes.scene import Scene
from ..components.navbar import Navbar
from ..components.buttons import Button


class MenuScene(Scene):
    def __init__(self, engine):
        super().__init__()
        self.engine = engine
        self.navbar = Navbar(100, 100, 600, 100, 0x1A1A1AFF)
        print("Menu")
        self.navbar.add(Button(140, 2, "QUIT", on_click=engine.onClose))

    def draw(self, renderer):
        print("Menu draw")
        self.navbar.draw(renderer)

    def handle_click(self, button, x, y):
        self.navbar.handle_click(button, x, y)

    def start_game(self):
        print("start game")
        #from game_scene import GameScene
        #self.engine.set_scene(GameScene(self.engine))