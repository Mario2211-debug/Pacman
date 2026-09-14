from engine import keys
from engine.scenes.scene import Scene
from ..components.main import Main
from ..components.text_input import TextInput
from src.highscores import NAME_MAX_LENGTH
from utils.colors import Basic, Grays, Pacman, UI

PANEL_W = 500
INPUT_W = 200


class GameOverScene(Scene):

    def __init__(self, engine, score, victory):
        super().__init__()
        self.engine = engine
        self.score = score
        self.victory = victory
        self.center_x = engine.win_w // 2
        self.new_record = engine.highscores.qualifies(score)

        # ========================= Components ================================
        self.main = Main(self.center_x - PANEL_W // 2, 110, PANEL_W, 380,
                         UI.DARK_SURFACE)
        self.name_input = TextInput(self.center_x - INPUT_W // 2, 330,
                                    INPUT_W, max_length=NAME_MAX_LENGTH,
                                    on_submit=self.save)

    def update(self, dt):
        self.name_input.update(dt)

    def draw(self, renderer):
        cx = self.center_x
        self.main.draw(renderer)
        if self.victory:
            renderer.draw_text_centered("CONGRATULATIONS!", cx, 140,
                                        Pacman.YELLOW)
            renderer.draw_text_centered("YOU CLEARED ALL LEVELS", cx, 175,
                                        Basic.WHITE)
        else:
            renderer.draw_text_centered("GAME OVER", cx, 150, Basic.RED)
        renderer.draw_text_centered(f"FINAL SCORE {self.score}", cx, 220,
                                    Basic.WHITE)

        if self.new_record:
            renderer.draw_text_centered("NEW HIGHSCORE!", cx, 255,
                                        Pacman.GOLD)
            renderer.draw_text_centered("ENTER YOUR NAME", cx, 295,
                                        Grays.GRAY_7)
            self.name_input.draw(renderer)
            renderer.draw_text_centered("ENTER SAVE   ESC SKIP", cx, 420,
                                        Grays.GRAY_6)
        else:
            renderer.draw_text_centered("NOT ENOUGH FOR THE TOP 10", cx, 295,
                                        Grays.GRAY_7)
            renderer.draw_text_centered("PRESS ENTER TO CONTINUE", cx, 420,
                                        Grays.GRAY_6)

    def handle_click(self, button, x, y):
        pass

    def handle_key(self, key):
        if key == keys.ESCAPE:
            self.main_menu()
        elif not self.new_record:
            if key in keys.CONFIRM:
                self.main_menu()
        else:
            self.name_input.handle_key(key)

    def save(self, name):
        self.engine.highscores.add(name, self.score)
        self.main_menu()

    def main_menu(self):
        from engine.scenes.menu import MenuScene
        self.engine.set_scene(MenuScene(self.engine))
