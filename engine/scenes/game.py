import math

from engine import keys
from engine.scenes.scene import Scene
from ..components.navbar import Navbar
from ..components.buttons import Button
from src.game_state import GameState
from utils.colors import Basic, Grays, Pacman

HUD_H = 40
MZ_W = 20
MZ_H = 25


class GameScene(Scene):
    def __init__(self, engine):
        super().__init__()
        self.engine = engine
        self.state = GameState(engine.config)
        self.engine.render.load_all_images()
        self.engine.render.create_rectangle("block_42_img",
                                            self.engine.render.corridor_width,
                                            self.engine.render.corridor_width,
                                            0xAA000066)
        self.engine.render.create_rectangle("pacman_mask",
                                            self.engine.render.images["pacman"].width,
                                            self.engine.render.images["pacman"].height,
                                            0xFF000000)
        self.engine.render.create_rectangle("ghost_mask",
                                            self.engine.render.images["ghost_red"].width,
                                            self.engine.render.images["ghost_orange"].height + 5,
                                            0xFF000000)
        self.engine.render.clear_all()
        self.engine.render.show_filled_block(self.engine.render.images["background1"], 0, 0,
                                      int(self.engine.win_w / self.engine.render.images["background1"].width) + 1,
                                      int(self.engine.win_h / self.engine.render.images["background1"].height) + 1)
        self.engine.render.show_filled_block(self.engine.render.images["emptiness"],
                                             1300, 670, 15, 5, 4, 4)
        self.engine.render.show(self.engine.render.images["logo"], 1350, 50)
        self.engine.render.create_text("Test text.\n0123456789\n!?+-=.:,", 1200, 350)

        # ========================= Components ================================
        self.navbar = Navbar(0, 0, engine.win_w, HUD_H, Grays.DARK_3)
        self.pause_button = Button(engine.win_w - 90, 8,
                                   on_click=self.pause,
                                   bg_color=Basic.NAVY,
                                   width=80, height=24, label="PAUSE")
        self.navbar.add(self.pause_button)

    def update(self, dt):
        self.state.tick(dt)
        if self.state.finished:
            self.end_game()

    def draw(self, renderer):
        self.draw_hud(renderer)
        self.draw_world(renderer)

    def draw_hud(self, renderer):
        state = self.state
        self.navbar.draw(renderer)
        renderer.draw_text(f"SCORE {state.score}", 12, 10, Basic.WHITE)
        renderer.draw_text(f"LIVES {state.lives}", 200, 10, Pacman.YELLOW)
        renderer.draw_text(f"LEVEL {state.level_number}/"
                           f"{state.total_levels}", 340, 10, Basic.WHITE)
        renderer.draw_text(f"TIME {max(0, math.ceil(state.time_left))}",
                           540, 10, Basic.WHITE)

    def draw_world(self, renderer):
        center_x = self.engine.win_w // 2
        renderer.draw_text_centered("GAMEPLAY GOES HERE", center_x, 250,
                                    Grays.GRAY_6)
        renderer.draw_text_centered("TEST KEYS: 1 PACGUM  2 SUPER  3 GHOST",
                                    center_x, 300, Grays.GRAY_5)
        renderer.draw_text_centered("K LOSE LIFE  N NEXT LEVEL  ESC/P PAUSE",
                                    center_x, 330, Grays.GRAY_5)
        renderer.gen_maze(MZ_W, MZ_W, False, (0, 0), (1, 1), 0)

    def handle_click(self, button, x, y):
        if button == 1 and self.pause_button.contains(x, y):
            self.pause_button.click()

    def handle_key(self, key):
        if key in keys.PAUSE:
            self.pause()
        # Temporary test keys until the gameplay is plugged in
        elif key == keys.ONE:
            self.state.eat_pacgum()
        elif key == keys.TWO:
            self.state.eat_super_pacgum()
        elif key == keys.THREE:
            self.state.eat_ghost()
        elif key == keys.K:
            self.state.lose_life()
        elif key == keys.N:
            self.state.complete_level()

    def pause(self):
        from engine.scenes.pause import PauseScene
        self.engine.set_scene(PauseScene(self.engine, self))

    def end_game(self):
        from engine.scenes.game_over import GameOverScene
        self.engine.set_scene(GameOverScene(self.engine, self.state.score,
                                            self.state.victory))
