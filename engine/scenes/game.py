import math

from engine import keys
from src.game_state import GameState
from engine.scenes.scene import Scene
from ..components.navbar import Navbar
from mazegenerator import MazeGenerator
from ..components.buttons import Button
from utils.colors import Basic, Grays, Pacman

HUD_H = 40
MZ_W = 20
MZ_H = 25


class GameScene(Scene):
    def __init__(self, engine):
        super().__init__()
        self.engine = engine
        self.state = GameState(engine.config)
        self.maze = MazeGenerator((MZ_W, MZ_H), False, (0, 0),
                                  (MZ_W - 1, MZ_H - 1),
                                  engine.config.seed).maze
        render = engine.render
        area_h = engine.win_h - HUD_H
        wall = max(2, min(engine.win_w // MZ_W, area_h // MZ_H) // 5)
        cell = min((engine.win_w - wall) // MZ_W, (area_h - wall) // MZ_H)
        self.cell, self.wall = cell, wall
        self.maze_x = (engine.win_w - (MZ_W * cell + wall)) // 2
        self.maze_y = HUD_H + (area_h - (MZ_H * cell + wall)) // 2
        render.clear(0x000000FF)
        render.draw_maze(self.maze, self.maze_x, self.maze_y, cell, wall,
                         render.images["background1"],
                         0x000000FF, 0x2121DEFF)
        self.background = bytes(render.data)

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
        renderer.data[:] = self.background

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
        # render.data[:] = self.game_scene.background

    def end_game(self):
        from engine.scenes.game_over import GameOverScene
        self.engine.set_scene(GameOverScene(self.engine, self.state.score,
                                            self.state.victory))
