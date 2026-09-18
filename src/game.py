from enum import Enum
import random

import time
# from typing import TYPE_CHECKING

from .types import GameStatus
from .display import Display
from mazegenerator import MazeGenerator
from .types import Direction, GameStatus

# if TYPE_CHECKING:
from .stats import Stats
from .pacman import PacMan
from .ghost import Ghost, Behavior as GhostBehavior, GhostStatus
from .config import Config
from .pacgum import pacgums_generate


TICK_RATE = 60
TICK_TIME = 1.0 / TICK_RATE


class Game:
    def __init__(self):
        self.config: Config

        self.stats: Stats = Stats(self)
        self.stats.level = 1
        self.stats.points = 0

        self.pacman: PacMan = PacMan()
        self.pacman.game = self
        self.ghosts: list[Ghost]
        self.display: Display
        self.status = GameStatus.PAUSED

        self.maze: list[list[int]] = []
        self.maze_width: int
        self.maze_height: int
        self.pacgums: list[list[int]] = []

        self.menu_list = [("Start game", "start"),
                ("Highscores", "highscores"),
                ("Instructions", "instructions"),
                ("Exit", "exit")]
        self.menu_current = 0

        self.pause_menu_list = [("Resume", "resume"),
                ("Main menu", "main_menu")]
        self.pause_menu_current = 0

        self.time = int(time.perf_counter())
        self.previous = time.perf_counter()
        self.accumulator = 0.0

    def exit(self, error = ""):
        for image in self.display.images.values():
            self.display.mlx.mlx_destroy_image(self.display.mlx_ptr, image.img)
        self.display.mlx.mlx_loop_exit(self.display.mlx_ptr)
        # exit()

    # GAME OVER SCREEN

    def game_over_handle_key_press(self, key, current_hover):
        if key == 65307 or key == 65293:  # ESC or ENTER
            self.menu()
            return

    def game_over(self):
        self.display.show_filled_block(self.display.images["background2"], 0, 0,
                                       self.display.screen_width // self.display.images["background2"].width + 1,
                                       self.display.screen_height // self.display.images["background2"].height + 1)
        self.display.show(self.display.images["game_over"],
                          self.display.screen_width // 2
                          - self.display.images["game_over"].width // 2,
                          350)
        # self.display.show_text("Game Over", 960, 500, "center")
        self.display.show_button("Main menu", 960 - self.display.images["button_hover"].width // 2, 700, "hover")

        self.display.mlx.mlx_hook(self.display.win, 2, 1, self.game_over_handle_key_press, self.menu_current)


    # LEVEL FINISHED SCREEN

    def level_finished_handle_key_press(self, key, current_hover):
        if key == 65307 or key == 65293:  # ESC or ENTER
            self.next_level()
            return

    def level_finished(self):
        self.display.show_filled_block(self.display.images["background2"], 0, 0,
                                       self.display.screen_width // self.display.images["background2"].width + 1,
                                       self.display.screen_height // self.display.images["background2"].height + 1)
        self.display.show(self.display.images["logo_big"],
                          self.display.screen_width // 2
                          - self.display.images["logo_big"].width // 2,
                          50)
        self.display.show_text("Level finished", 960, 500, "center")
        self.display.show_button("Next level", 960 - self.display.images["button_hover"].width // 2, 700, "hover")

        self.display.mlx.mlx_hook(self.display.win, 2, 1, self.level_finished_handle_key_press, self.menu_current)


    # MENU SCREEN

    def menu_handle_key_press(self, key, current_hover):
        # print(f"Pressed key {key}")
        if key == 65293:  # ENTER
            if self.menu_list[self.menu_current][1] == "exit":
                self.exit()
                return
            elif self.menu_list[self.menu_current][1] == "start":
                self.start()
                return
        if key == 119 or key == 65362:
            self.menu_current -= 1
            if self.menu_current < 0:
                self.menu_current = len(self.menu_list) - 1
            self.show_menu()
        elif key == 115 or key == 65364:
            self.menu_current += 1
            if self.menu_current >= len(self.menu_list):
                self.menu_current = 0
            self.show_menu()

    def show_menu(self) -> None:
        pos_x = self.display.screen_width // 2 - self.display.images["button"].width // 2
        pos_y_start = self.display.images["logo_big"].height + 100
        for i in range(len(self.menu_list)):
            pos_y = pos_y_start + self.display.images["button"].height * i
            self.display.show_button(self.menu_list[i][0],
                                     pos_x, pos_y,
                                     ("hover" if i == self.menu_current else "normal"))

    def menu(self) -> None:
        if not self.display:
            return
        # self.display.clear_window()
        self.display.show_filled_block(self.display.images["background2"], 0, 0,
                                       self.display.screen_width // self.display.images["background2"].width + 1,
                                       self.display.screen_height // self.display.images["background2"].height + 1)
        self.display.show(self.display.images["logo_big"],
                          self.display.screen_width // 2
                          - self.display.images["logo_big"].width // 2,
                          50)

        for i in range(3):
            for ghost in self.ghosts:
                rand_x = random.randint(50, self.display.screen_width - 50)
                rand_y = random.randint(50, self.display.screen_height - 100)
                if self.display.screen_width // 2 - self.display.images["button"].width - 50 // 2 <= rand_x <= self.display.screen_width // 2:
                    rand_x -= self.display.images["button"].width
                elif self.display.screen_width // 2 <= rand_x <= self.display.screen_width // 2 + self.display.images["button"].width // 2:
                    rand_x += self.display.images["button"].width
                if rand_x > self.display.screen_width // 2:
                    self.display.show(self.display.images[ghost.name + "_left"], rand_x, rand_y)
                else:
                    self.display.show(self.display.images[ghost.name + "_right"], rand_x, rand_y)

        self.show_menu()
        self.display.mlx.mlx_hook(self.display.win, 2, 1, self.menu_handle_key_press, self.menu_current)


    # PAUSE SCREEN

    def pause_menu_handle_key_press(self, key, current_hover) -> None:
        # print(f"PAUSE Pressed key {key}")
        if key == 65307:  # ESC
            self.resume()
            return
        if key == 65293:  # ENTER
            if self.pause_menu_list[self.pause_menu_current][1] == "resume":
                self.resume()
                return
            if self.pause_menu_list[self.pause_menu_current][1] == "main_menu":
                self.menu()
                return
        if key == 119 or key == 65362:
            self.pause_menu_current -= 1
            if self.pause_menu_current < 0:
                self.pause_menu_current = len(self.pause_menu_list) - 1
            self.show_pause_menu()
        elif key == 115 or key == 65364:
            self.pause_menu_current += 1
            if self.pause_menu_current >= len(self.pause_menu_list):
                self.pause_menu_current = 0
            self.show_pause_menu()

    def show_pause_menu(self) -> None:
        pos_x = self.display.screen_width // 2 - self.display.images["button"].width // 2
        pos_y_start = self.display.screen_height // 2 - self.display.images["button"].height
        for i in range(len(self.pause_menu_list)):
            pos_y = pos_y_start + self.display.images["button"].height * i
            self.display.show_button(self.pause_menu_list[i][0],
                                     pos_x, pos_y,
                                     ("hover" if i == self.pause_menu_current else "normal"))

    def pause(self) -> None:
        if not self.display:
            return
        if not self.display.images.get("pause_background"):
            self.display.create_rectangle("pause_background", 256, 256, 0xAA000000)
        self.display.show_filled_block(self.display.images["pause_background"], 0, 0,
                                       self.display.screen_width // self.display.images["pause_background"].width + 1,
                                       self.display.screen_height // self.display.images["pause_background"].height + 1)
        self.show_pause_menu()
        self.display.mlx.mlx_hook(self.display.win, 2, 1, self.pause_menu_handle_key_press, self.pause_menu_current)


    # GENERATE LEVEL

    def create_level(self, level_num) -> None:
        maze_width = self.config.level[level_num - 1]["width"]
        maze_height = self.config.level[level_num - 1]["height"]

        mazegen = MazeGenerator((maze_width, maze_height), False, (0, 0), (1, 1), self.config.seed)
        if not mazegen.maze:
            return
        self.maze = mazegen.maze
        self.maze_width = len(mazegen.maze[0])
        self.maze_height = len(mazegen.maze)

        self.pacman.set_image("pacman_right")
        self.pacman.set_start_position(maze_width // 2, maze_height // 2)

        pacgums = pacgums_generate(mazegen.maze, self.config.pacgum)
        self.pacgums = pacgums

        for ghost in self.ghosts:
            ghost.set_image(ghost.name + "_right")
            ghost.set_behavior(ghost.behavior_standart)
            ghost.speed = 2

        self.ghosts[0].set_start_position(0, 0)
        self.ghosts[1].set_start_position(maze_width - 1, 0)
        self.ghosts[2].set_start_position(0, maze_height - 1)
        self.ghosts[3].set_start_position(maze_width - 1, maze_height - 1)
        # print("LEVEL CREATED")


    # GAME SCREEN

    def death(self) -> None:
        print("LIVES:", self.stats.stats["lives"])
        self.stats.increase_lives(-1)
        if self.stats.stats["lives"] == 0:
            self.game_over()
            self.status = GameStatus.GAME_OVER
            return
        for ghost in self.ghosts:
            ghost.speed = 15
            ghost.set_behavior(GhostBehavior.TO_START)
        self.pacman.death()

    def edible_mode(self) -> None:
        for ghost in self.ghosts:
            ghost.status = GhostStatus.EDIBLE
            ghost.set_behavior(GhostBehavior.SCARED)
            # ghost.target = ghost.get_random_cell_far_from_pacman()
            ghost.set_image(ghost.name + "_right")

    def eat_ghost(self, ghost: Ghost) -> None:
        ghost.death()
        self.stats.increase_score(self.config.points_per_ghost)

    def check_pacgums(self) -> None:
        if sum(1 for row in self.pacgums for x in row if x != 0) > 0:
            return
        self.status = GameStatus.PAUSED
        self.level_finished()

    def eat_pacgum(self, x: int, y: int) -> None:
        if self.pacgums[y][x] == 2:
            self.pacgums[y][x] = 0
            self.stats.increase_score(self.config.points_per_super_pacgum)
            self.edible_mode()
            self.check_pacgums()
        elif self.pacgums[y][x] == 1:
            # self.game.stats.score += 1
            self.pacgums[y][x] = 0
            self.stats.increase_score(self.config.points_per_pacgum)
            self.check_pacgums()
            # print(self.game.points)

    def game_handle_key_press(self, key, pacman):
        # print(f"Pressed key {key}")
        if key == 65307:  # ESC
            if self.status == GameStatus.RUN:
                self.status = GameStatus.PAUSED
                self.pause()
            return
        elif key == 115:  # S
            self.pacman.increase_speed()
        elif key == 108:  # L
            self.stats.increase_lives()
        elif key == 102:  # F
            for ghost in self.ghosts:
                ghost.make_freeze()
        # elif key == 119 or key == 65362:
        elif key == 65362:
            pacman.direction_next = Direction.TOP
        # elif key == 100 or key == 65363:
        elif key == 65363:
            pacman.direction_next = Direction.RIGHT
        # elif key == 115 or key == 65364:
        elif key == 65364:
            pacman.direction_next = Direction.BOTTOM
        # elif key == 97 or key == 65361:
        elif key == 65361:
            pacman.direction_next = Direction.LEFT

        if not pacman.direction:
            pacman.direction = pacman.direction_next

    def move_object(self, obj: PacMan | Ghost):
        if self.status != GameStatus.RUN:
            return
        shift_x = self.display.cell_width + 5
        shift_y = self.display.cell_width + 5
        # Clear old
        pos_x = shift_x + obj.x_px
        pos_y = shift_y + obj.y_px
        self.display.show(obj.mask, pos_x, pos_y)

        if obj.direction == Direction.RIGHT:
            obj.set_image(obj.name + "_right")
            if obj.x_px < obj.next_x * self.display.cell_width:
                obj.x_px += obj.speed
            if obj.x_px >= obj.next_x * self.display.cell_width:
                obj.move()
        elif obj.direction == Direction.LEFT:
            obj.set_image(obj.name + "_left")
            if obj.x_px > obj.next_x * self.display.cell_width:
                obj.x_px -= obj.speed
            if obj.x_px <= obj.next_x * self.display.cell_width:
                obj.move()
        elif obj.direction == Direction.TOP:
            if type(obj) == PacMan:
                obj.set_image("pacman_top")
            if obj.y_px > obj.next_y * self.display.cell_width:
                obj.y_px -= obj.speed
            if obj.y_px <= obj.next_y * self.display.cell_width:
                obj.move()
        elif obj.direction == Direction.BOTTOM:
            if type(obj) == PacMan:
                obj.set_image("pacman_bottom")
            if obj.y_px < obj.next_y * self.display.cell_width:
                obj.y_px += obj.speed
            if obj.y_px >= obj.next_y * self.display.cell_width:
                obj.move()

        #Show pacgum
        if type(obj) == Ghost:
            if self.pacgums[obj.y][obj.x] == 1:
                self.display.show_pacgum(obj.x, obj.y, "small")
            elif self.pacgums[obj.y][obj.x] == 2:
                self.display.show_pacgum(obj.x, obj.y, "big")

        # Show new
        pos_x = shift_x + obj.x_px
        pos_y = shift_y + obj.y_px
        self.display.show(obj.image, pos_x, pos_y)


    def make_turn(self, nothing):
        if self.status != GameStatus.RUN:
            return

        current = time.perf_counter()
        frame_time = current - self.previous
        if self.time < int(current):
            self.stats.increase_time(-1)
            self.time = int(current)
        self.previous = current

        self.accumulator += frame_time

        while self.accumulator >= TICK_TIME:
            self.accumulator -= TICK_TIME

            # print("playing...")
            self.move_object(self.pacman)
            for ghost in self.ghosts:
                self.move_object(ghost)
                if (self.pacman.x_px - self.pacman.image.width // 1.5 <= ghost.x_px <= self.pacman.x_px + self.pacman.image.width // 1.5
                    and self.pacman.y_px - self.pacman.image.height // 1.5 <= ghost.y_px <= self.pacman.y_px + self.pacman.image.height // 1.5 and ghost.status != GhostStatus.DEATH):
                    print(f"!!!! CATCHED BY {ghost.name} at {ghost.x}, {ghost.y}")
                    print("GhostStatus:", ghost.status)
                    if ghost.status == GhostStatus.EDIBLE:
                        self.eat_ghost(ghost)
                    else:
                        self.death()

    def resume(self) -> None:
        self.display.clear_window()
        self.display.show_filled_block(self.display.images["background1"], 0, 0, 10, self.display.screen_height // self.display.images["background1"].height + 1)
        self.display.show_filled_block(self.display.images["background2"], 1350, 0, 3, self.display.screen_height // self.display.images["background2"].height + 1)

        self.display.show(self.display.images["logo_small"], 1450, 50)
        self.display.show_maze()

        self.stats.show_stats()

        self.previous = time.perf_counter()
        self.time = int(self.previous)
        self.accumulator = 0.0

        self.status = GameStatus.RUN

        self.display.mlx.mlx_hook(self.display.win, 2, 1, self.game_handle_key_press, self.pacman)
        self.display.mlx.mlx_loop_hook(self.display.mlx_ptr, self.make_turn, None)


    def next_level(self) -> None:
        print("New level")
        self.stats.increase_level()
        self.create_level(self.stats.stats["level"])
        # self.stats.reset_stats()
        self.pacman.speed = 3
        self.pacman.direction = None
        self.pacman.direction_next = None
        self.pacman.set_image("pacman_right")
        self.resume()

    def start(self) -> None:
        print("Let's start!")
        self.create_level(self.stats.stats["level"])
        self.stats.reset_stats()
        self.pacman.speed = 3
        self.pacman.direction = None
        self.pacman.direction_next = None
        self.pacman.set_image("pacman_right")
        for ghost in self.ghosts:
            ghost.reborn()
        self.resume()
        # self.display.clear_window()
        # self.display.show_filled_block(self.display.images["background1"], 0, 0, self.display.screen_width // self.display.images["background1"].width + 1, self.display.screen_height // self.display.images["background1"].height + 1)

        # # display.show_filled_block(display.images["emptiness"], 1300, 670, 15, 5, 4, 4)

        # self.display.show(self.display.images["logo_small"], 1350, 50)

        # # display.show_text("Test text.\n0123456789\n!?+-=.:,", 1200, 350)

        # self.display.show_maze()

        # self.status = GameStatus.RUN

        # self.display.mlx.mlx_hook(self.display.win, 2, 1, self.game_handle_key_press, self.pacman)
        # self.display.mlx.mlx_loop_hook(self.display.mlx_ptr, self.make_turn, None)