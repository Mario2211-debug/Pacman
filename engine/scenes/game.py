import math

from engine import keys
from src.game_state import GameState
from src.pacman import PacMan, PacManDirection
from src.pacgum import pacgums_generate
from engine.scenes.scene import Scene
from ..components.navbar import Navbar
from mazegenerator import MazeGenerator
from ..components.buttons import Button
from utils.colors import Basic, Grays, Pacman

HUD_H = 40
MZ_W = 20
MZ_H = 25
PACMAN_SPEED = 5  # cells per second



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


        self.pacgums = pacgums_generate(self.maze, engine.config.pacgum)
        self.pacman = PacMan()
        self.pacman.pitch = cell
        self.pacman.set_maze(self.maze)
        self.pacman.set_pacgums(self.pacgums)
        self.pacman.set_start_position(MZ_W // 2, MZ_H // 2, cell)

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
            return
        self.move_pacman(dt)

    def move_pacman(self, dt):
        pacman = self.pacman
        step = PACMAN_SPEED * self.cell * dt
        target_x = pacman.next_x * self.cell
        target_y = pacman.next_y * self.cell
        if pacman.x_px < target_x:
            pacman.x_px = min(pacman.x_px + step, target_x)
        elif pacman.x_px > target_x:
            pacman.x_px = max(pacman.x_px - step, target_x)
        if pacman.y_px < target_y:
            pacman.y_px = min(pacman.y_px + step, target_y)
        elif pacman.y_px > target_y:
            pacman.y_px = max(pacman.y_px - step, target_y)
        if pacman.x_px == target_x and pacman.y_px == target_y:
            eaten = self.pacgums[pacman.next_y][pacman.next_x]
            pacman.move()
            if eaten == 1:
                self.state.eat_pacgum()
            elif eaten == 2:
                self.state.eat_super_pacgum()


    def draw(self, renderer):
        renderer.data[:] = self.background
        self.draw_pacgums(renderer)
        sprite = renderer.images["pacman"]
        offset = (self.cell - self.wall - sprite.width) // 2
        renderer.blit(sprite,
                      self.maze_x + self.wall + offset + int(self.pacman.x_px),
                      self.maze_y + self.wall + offset + int(self.pacman.y_px))
        self.draw_hud(renderer)


    def draw_pacgums(self, renderer):
        inner = self.cell - self.wall
        small = max(2, inner // 6)
        big = max(4, inner // 2)
        for y, row in enumerate(self.pacgums):
            for x, value in enumerate(row):
                if not value:
                    continue
                size = small if value == 1 else big
                color = Pacman.DOT if value == 1 else Pacman.POWER_DOT
                renderer.fill_rect(
                    self.maze_x + self.wall + x * self.cell + (inner - size) // 2,
                    self.maze_y + self.wall + y * self.cell + (inner - size) // 2,
                    size, size, color)

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
        elif key in (keys.UP, keys.W):
            self.pacman.direction_next = PacManDirection.TOP
        elif key in (keys.RIGHT, keys.D):
            self.pacman.direction_next = PacManDirection.RIGHT
        elif key in (keys.DOWN, keys.S):
            self.pacman.direction_next = PacManDirection.BOTTOM
        elif key in (keys.LEFT, keys.A):
            self.pacman.direction_next = PacManDirection.LEFT

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
