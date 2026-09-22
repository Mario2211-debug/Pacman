import random
import time
from typing import Any

from mazegenerator import MazeGenerator
from .config import Config
from .game_types import Direction, GameStatus, GhostStatus, GhostBehavior, \
    PacManStatus
from .display import Display
from .highscores import open_highscores_file, clear_highscores_file, \
    save_to_highscores_file
from .stats import Stats

from .pacman import PacMan
from .ghost import Ghost
from .pacgum import pacgums_generate

TICK_RATE = 60
TICK_TIME = 1.0 / TICK_RATE
EDIBLE_TIME = 10


class Game:
    def __init__(self, config: Config):
        self.config: Config = config

        self.stats: Stats = Stats(self)

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
        self.menu_cur = 0

        self.pause_menu_list = [("Resume", "resume"),
                                ("Main menu", "main_menu")]
        self.pause_menu_cur = 0

        self.hs_menu_list = [("Main menu", "main_menu"),
                             ("Clear", "clear")]
        self.hs_menu_cur = 0

        self.score_menu_list = [("Save score", "save"),
                                ("Cancel", "cancel")]
        self.score_menu_cur = 0

        self.time: int = int(time.perf_counter())
        self.previous: float = self.time
        self.edible_time = 0
        self.accumulator = 0.0
        self.player_name: str = ""

    def exit(self, error: Any = None) -> None:
        for image in self.display.images.values():
            self.display.mlx.mlx_destroy_image(self.display.mlx_ptr, image.img)
        self.display.mlx.mlx_loop_exit(self.display.mlx_ptr)

    #
    # VICTORY SCREEN
    #

    def score_menu_handle_key_press(self, key: int, nothing: Any) -> None:
        # self.display.show(self.display.images["save_score_tmp"], 0, 0)
        # print("Handle")
        if key == 65307 and self.stats.stats["score"] == 0:  # ESC
            self.menu()
            return
        elif key == 65293 or key == 65421:  # ENTER
            if self.score_menu_list[self.score_menu_cur][1] == "save":
                if self.player_name:
                    save_to_highscores_file(self.config.highscore_filename,
                                            {"name": self.player_name,
                                             "score": self.stats.stats["score"]
                                             })
                    if self.display.images.get("highscores_screen"):
                        self.display.mlx.mlx_destroy_image(
                            self.display.mlx_ptr,
                            self.display.images["highscores_screen"].img
                            )
                        self.display.images.pop("highscores_screen")
                    self.menu()
                return
            if self.score_menu_list[self.score_menu_cur][1] == "cancel":
                self.menu()
                return
        elif key == 65362 or key == 65361:
            self.score_menu_cur -= 1
            if self.score_menu_cur < 0:
                self.score_menu_cur = len(self.score_menu_list) - 1
            self.show_score_menu()
        elif key == 65364 or key == 65363:
            self.score_menu_cur += 1
            if self.score_menu_cur >= len(self.score_menu_list):
                self.score_menu_cur = 0
            self.show_score_menu()
        elif key == 65288:  # Backspace
            if len(self.player_name):
                self.player_name = self.player_name[0: -1]
                self.show_score_input()
        else:
            if (len(self.player_name) < 10
                and chr(key).isalnum()
                and self.display.images.get(chr(key))
                or (len(self.player_name) > 0 and
                    chr(key) == " "
                    and self.player_name[-1] != " ")):
                self.player_name += chr(key)
                self.show_score_input()

    def show_score_menu(self) -> None:
        pos_x_1 = self.display.screen_width // 2 - \
            (self.display.images["button"].width + 20)
        pos_y = self.display.screen_height - \
            self.display.images["button"].height - 100
        for i in range(len(self.score_menu_list)):
            pos_x = pos_x_1 + (self.display.images["button"].width + 20) * i
            self.display.show_button(self.score_menu_list[i][0],
                                     pos_x, pos_y,
                                     ("hover" if i == self.score_menu_cur
                                      else "normal"))

    def show_score_input(self) -> None:
        self.display.show_filled_block(self.display.images["emptiness"],
                                       700, 640, 13, 2, 4, 4)
        if self.player_name:
            self.display.show_text(self.player_name, 720, 660)

    def no_score_menu_handle_key_press(self, key: int, nothing: Any) -> None:
        if key == 65307 or key == 65293 or key == 65421:  # ESC or ENTER
            self.menu()
            return

    def victory(self) -> None:
        self.status = GameStatus.VICTORY

        if self.stats.stats["score"] != 0:
            self.display.show(self.display.images["save_score_tmp"], 0, 0)
            self.display.show(self.display.images["victory"],
                              self.display.screen_width // 2
                              - self.display.images["victory"].width // 2,
                              150)
            self.display.show_text(str(self.stats.stats["score"]), 1040, 500)
            self.display.mlx.mlx_hook(self.display.win, 2, 1,
                                      self.score_menu_handle_key_press,
                                      self.menu_cur)
        else:
            self.display.show(self.display.images["big_background"], 0, 0)
            self.display.show(self.display.images["victory"],
                              self.display.screen_width // 2
                              - self.display.images["victory"].width // 2,
                              150)
            self.display.show_text("Your score: 0", 960, 550, "center")
            button_x = 960 - self.display.images["button_hover"].width // 2
            self.display.show_button("Main menu", button_x, 700, "hover")
            self.display.mlx.mlx_hook(self.display.win, 2, 1,
                                      self.no_score_menu_handle_key_press,
                                      self.menu_cur)

    #
    # TIME OUT SCREEN
    #

    def time_out(self) -> None:
        # print("TIME OUT")
        # self.display.clear_window()
        self.status = GameStatus.GAME_OVER

        if self.stats.stats["score"] != 0:
            self.display.show(self.display.images["save_score_tmp"], 0, 0)
            self.display.show(self.display.images["time_out"],
                              self.display.screen_width // 2
                              - self.display.images["time_out"].width // 2,
                              150)
            self.display.show_text(str(self.stats.stats["score"]), 1040, 500)
            self.display.mlx.mlx_hook(self.display.win, 2, 1,
                                      self.score_menu_handle_key_press,
                                      self.menu_cur)
        else:
            self.display.show(self.display.images["big_background"], 0, 0)
            self.display.show(self.display.images["time_out"],
                              self.display.screen_width // 2
                              - self.display.images["time_out"].width // 2,
                              150)
            self.display.show_text("Your score: 0", 960, 550, "center")
            button_x = 960 - self.display.images["button_hover"].width // 2
            self.display.show_button("Main menu", button_x, 700, "hover")
            self.display.mlx.mlx_hook(self.display.win, 2, 1,
                                      self.no_score_menu_handle_key_press,
                                      self.menu_cur)

    #
    # GAME OVER SCREEN
    #

    def game_over(self) -> None:
        # print("GAME OVER")
        # self.display.clear_window()
        self.status = GameStatus.GAME_OVER

        if self.stats.stats["score"] != 0:
            self.display.show(self.display.images["save_score_tmp"], 0, 0)
            self.display.show(self.display.images["game_over"],
                              self.display.screen_width // 2
                              - self.display.images["game_over"].width // 2,
                              150)
            self.display.show_text(str(self.stats.stats["score"]), 1040, 500)
            self.display.mlx.mlx_hook(self.display.win, 2, 1,
                                      self.score_menu_handle_key_press,
                                      self.menu_cur)
        else:
            self.display.show(self.display.images["big_background"], 0, 0)
            self.display.show(self.display.images["game_over"],
                              self.display.screen_width // 2
                              - self.display.images["game_over"].width // 2,
                              150)
            self.display.show_text("Your score: 0", 960, 550, "center")
            button_x = 960 - self.display.images["button_hover"].width // 2
            self.display.show_button("Main menu", button_x, 700, "hover")
            self.display.mlx.mlx_hook(self.display.win, 2, 1,
                                      self.no_score_menu_handle_key_press,
                                      self.menu_cur)

    #
    # LEVEL COMPLETED SCREEN
    #

    def level_completed_handle_key_press(self, key: int, nothing: Any) -> None:
        if key == 65307 or key == 65293 or key == 65421:  # ESC or ENTER
            self.next_level()
            return

    def level_completed(self) -> None:
        if self.stats.stats["level"] == len(self.config.level):
            self.victory()
            return
        self.status = GameStatus.PAUSED
        self.display.show(self.display.images["big_background"], 0, 0)

        self.display.show(self.display.images["level_complete"],
                          self.display.screen_width // 2
                          - self.display.images["level_complete"].width // 2,
                          350)
        button_x = 960 - self.display.images["button_hover"].width // 2
        self.display.show_button("Next level", button_x, 700, "hover")

        self.display.mlx.mlx_hook(self.display.win, 2, 1,
                                  self.level_completed_handle_key_press,
                                  self.menu_cur)

    #
    # MAIN MENU SCREEN
    #

    def menu_handle_key_press(self, key: int, nothing: Any) -> None:
        # print(f"Pressed key {key}")
        if key == 65293 or key == 65421:  # ENTER
            if self.menu_list[self.menu_cur][1] == "exit":
                self.exit()
                return
            elif self.menu_list[self.menu_cur][1] == "start":
                self.start()
                return
            elif self.menu_list[self.menu_cur][1] == "highscores":
                self.highscores()
                return
            elif self.menu_list[self.menu_cur][1] == "instructions":
                self.instructions()
                return
        if key == 65362:
            self.menu_cur -= 1
            if self.menu_cur < 0:
                self.menu_cur = len(self.menu_list) - 1
            self.show_menu()
        elif key == 65364:
            self.menu_cur += 1
            if self.menu_cur >= len(self.menu_list):
                self.menu_cur = 0
            self.show_menu()

    def show_menu(self) -> None:
        pos_x = self.display.screen_width // 2 - \
            self.display.images["button"].width // 2
        pos_y_1 = self.display.images["logo_big"].height + 100
        for i in range(len(self.menu_list)):
            pos_y = pos_y_1 + (self.display.images["button"].height + 10) * i
            self.display.show_button(self.menu_list[i][0],
                                     pos_x, pos_y,
                                     ("hover" if i == self.menu_cur
                                      else "normal"))

    def menu(self) -> None:
        if not self.display:
            return

        self.hs_menu_cur = 0
        self.display.show(self.display.images["big_background"], 0, 0)
        self.display.show(self.display.images["logo_big"],
                          self.display.screen_width // 2
                          - self.display.images["logo_big"].width // 2,
                          50)

        for i in range(5):
            for ghost in self.ghosts:

                rand_x = random.randint(50, 450)
                rand_y = random.randint(50, self.display.screen_height - 100)
                if random.getrandbits(1):
                    rand_x += 1430
                if rand_x > self.display.screen_width // 2:
                    self.display.show(self.display.images[ghost.name+"_left"],
                                      rand_x, rand_y)
                else:
                    self.display.show(self.display.images[ghost.name+"_right"],
                                      rand_x, rand_y)

        self.show_menu()
        self.display.mlx.mlx_hook(self.display.win, 2, 1,
                                  self.menu_handle_key_press,
                                  self.menu_cur)

    #
    # PAUSE SCREEN
    #

    def pause_menu_handle_key_press(self, key: int, nothing: Any) -> None:
        # print(f"PAUSE Pressed key {key}")
        if key == 65307:  # ESC
            self.resume()
            return
        if key == 65293 or key == 65421:  # ENTER
            if self.pause_menu_list[self.pause_menu_cur][1] == "resume":
                self.resume()
                return
            if self.pause_menu_list[self.pause_menu_cur][1] == "main_menu":
                self.menu()
                return
        if key == 65362:
            self.pause_menu_cur -= 1
            if self.pause_menu_cur < 0:
                self.pause_menu_cur = len(self.pause_menu_list) - 1
            self.show_pause_menu()
        elif key == 65364:
            self.pause_menu_cur += 1
            if self.pause_menu_cur >= len(self.pause_menu_list):
                self.pause_menu_cur = 0
            self.show_pause_menu()

    def show_pause_menu(self) -> None:
        pos_x = self.display.screen_width // 2 - \
            self.display.images["button"].width // 2
        pos_y_1 = self.display.screen_height // 2 - \
            (self.display.images["button"].height + 20)
        for i in range(len(self.pause_menu_list)):
            pos_y = pos_y_1 + (self.display.images["button"].height + 20) * i
            self.display.show_button(self.pause_menu_list[i][0],
                                     pos_x, pos_y,
                                     ("hover" if i == self.pause_menu_cur
                                      else "normal"))

    def pause(self) -> None:
        if not self.display.images.get("pause_background"):
            self.display.create_rectangle("pause_background",
                                          self.display.screen_width,
                                          self.display.screen_height,
                                          0xAA000000)
        self.display.show(self.display.images["pause_background"], 0, 0)
        self.show_pause_menu()
        self.display.mlx.mlx_hook(self.display.win, 2, 1,
                                  self.pause_menu_handle_key_press,
                                  self.pause_menu_cur)

    #
    # GENERATE LEVEL
    #

    def create_level(self, level_num: int) -> None:
        maze_width = self.config.level[level_num - 1]["width"]
        maze_height = self.config.level[level_num - 1]["height"]
        try:
            mazegen = MazeGenerator((maze_width, maze_height),
                                    False,
                                    (0, 0),
                                    (maze_width - 1, maze_height - 1),
                                    self.config.seed + level_num)
        except Exception:
            self.status = GameStatus.ERROR
            return

        if not mazegen.maze:
            self.status = GameStatus.ERROR
            return
        self.maze = mazegen.maze
        self.maze_width = len(mazegen.maze[0])
        self.maze_height = len(mazegen.maze)

        self.pacman.set_image("right")
        self.pacman.set_start_position(maze_width // 2, maze_height // 2)

        pacgums = pacgums_generate(mazegen.maze, self.config.pacgum)
        self.pacgums = pacgums

        for ghost in self.ghosts:
            ghost.set_image("right")
            ghost.status = GhostStatus.ACTIVE
            if self.pacman.status != PacManStatus.INVISIBLE:
                ghost.set_behavior(ghost.behavior_default)
            else:
                ghost.set_behavior(GhostBehavior.RANDOM)
            ghost.speed_reset()

        self.ghosts[0].set_start_position(0, 0)
        self.ghosts[1].set_start_position(maze_width - 1, 0)
        self.ghosts[2].set_start_position(0, maze_height - 1)
        self.ghosts[3].set_start_position(maze_width - 1, maze_height - 1)

        self.display.create_maze_bitmap()
        # print("LEVEL CREATED")

    #
    # GAME SCREEN
    #

    def death(self) -> None:
        # print("LIVES:", self.stats.stats["lives"])
        self.stats.increase_lives(-1)
        if self.stats.stats["lives"] == 0:
            self.game_over()
            return
        for ghost in self.ghosts:
            ghost.speed = 15
            ghost.set_behavior(GhostBehavior.TO_START)
        self.pacman.death()

    def edible_mode(self, on: bool = True) -> None:
        if on:
            self.edible_time += EDIBLE_TIME
        pos_x_base = self.display.cell_width + 5 + self.display.maze_x
        pos_y_base = self.display.cell_width + 5 + self.display.maze_x
        for ghost in self.ghosts:
            if ghost.status != GhostStatus.DEATH:
                if on:
                    ghost.status = GhostStatus.EDIBLE
                    ghost.set_behavior(GhostBehavior.SCARED)
                else:
                    ghost.status = GhostStatus.ACTIVE
                    ghost.set_behavior(ghost.behavior_default)

            pos_x = pos_x_base + ghost.x_px
            pos_y = pos_y_base + ghost.y_px
            self.display.add_to_bitmap("maze_screen", ghost.mask.name,
                                       pos_x, pos_y)
            ghost.set_image("right")

    def eat_ghost(self, ghost: Ghost) -> None:
        if ghost.status != GhostStatus.EDIBLE:
            return
        ghost.death()
        self.stats.increase_score(self.config.points_per_ghost)

    def check_pacgums(self) -> None:
        if sum(1 for row in self.pacgums for x in row if x != 0) > 0:
            return
        self.status = GameStatus.PAUSED
        self.level_completed()

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

    def game_handle_key_press(self, key: int, nothing: Any) -> None:
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
        elif key == 110:  # N
            self.level_completed()
        elif key == 105:  # I
            self.pacman.invisible()
        # elif key == 119 or key == 65362:
        elif key == 65362:
            self.pacman.direction_next = Direction.TOP
        # elif key == 100 or key == 65363:
        elif key == 65363:
            self.pacman.direction_next = Direction.RIGHT
        # elif key == 115 or key == 65364:
        elif key == 65364:
            self.pacman.direction_next = Direction.BOTTOM
        # elif key == 97 or key == 65361:
        elif key == 65361:
            self.pacman.direction_next = Direction.LEFT

        if not self.pacman.direction:
            self.pacman.direction = self.pacman.direction_next

    def move_object(self, obj: PacMan | Ghost) -> None:
        if self.status != GameStatus.RUN:
            return
        shift_x = self.display.cell_width + 5 + self.display.maze_x
        shift_y = self.display.cell_width + 5 + self.display.maze_y
        # Clear old (show mask)
        pos_x = shift_x + obj.x_px
        pos_y = shift_y + obj.y_px
        # self.display.show(obj.mask, pos_x, pos_y)
        self.display.add_to_bitmap("maze_screen", obj.mask.name, pos_x, pos_y)

        if obj.direction == Direction.RIGHT:
            obj.set_image("right")
            if obj.x_px < obj.next_x * self.display.cell_width:
                obj.x_px += obj.speed
            if obj.x_px >= obj.next_x * self.display.cell_width:
                obj.move()
        elif obj.direction == Direction.LEFT:
            obj.set_image("left")
            if obj.x_px > obj.next_x * self.display.cell_width:
                obj.x_px -= obj.speed
            if obj.x_px <= obj.next_x * self.display.cell_width:
                obj.move()
        elif obj.direction == Direction.TOP:
            if isinstance(obj, PacMan):
                obj.set_image("top")
            if obj.y_px > obj.next_y * self.display.cell_width:
                obj.y_px -= obj.speed
            if obj.y_px <= obj.next_y * self.display.cell_width:
                obj.move()
        elif obj.direction == Direction.BOTTOM:
            if isinstance(obj, PacMan):
                obj.set_image("bottom")
            if obj.y_px < obj.next_y * self.display.cell_width:
                obj.y_px += obj.speed
            if obj.y_px >= obj.next_y * self.display.cell_width:
                obj.move()

        # Show pacgum
        if isinstance(obj, Ghost):
            if self.pacgums[obj.y][obj.x] == 1:
                self.display.show_pacgum(obj.x, obj.y, "small")
            elif self.pacgums[obj.y][obj.x] == 2:
                self.display.show_pacgum(obj.x, obj.y, "big")

        # Show new
        pos_x = shift_x + obj.x_px
        pos_y = shift_y + obj.y_px
        self.display.add_to_bitmap("maze_screen", obj.image.name, pos_x, pos_y)

    def playing(self, nothing: Any) -> None:
        if self.status != GameStatus.RUN:
            return

        current = time.perf_counter()
        frame_time = current - self.previous
        if self.time < int(current):
            self.stats.increase_time(-1)
            if self.stats.stats["time"] <= 0:
                self.time_out()
                return
            if self.edible_time >= 1:
                self.edible_time -= 1
                if self.edible_time == 0:
                    self.edible_mode(False)
            self.time = int(current)
        self.previous = current

        self.accumulator += frame_time

        while self.accumulator >= TICK_TIME:
            self.accumulator -= TICK_TIME

            self.display.show(self.display.images["maze_screen"], 0, 0)

            self.move_object(self.pacman)
            for ghost in self.ghosts:
                self.move_object(ghost)
                if (ghost.status != GhostStatus.DEATH
                   and self.pacman.x_px-ghost.image.width//1.5 <= ghost.x_px
                   and ghost.x_px <= self.pacman.x_px+ghost.image.width//1.5
                   and self.pacman.y_px-ghost.image.height//1.5 <= ghost.y_px
                   and ghost.y_px <= self.pacman.y_px+ghost.image.height//1.5):

                    if ghost.status == GhostStatus.EDIBLE:
                        self.eat_ghost(ghost)
                    elif (ghost.behavior != GhostBehavior.TO_START and
                            self.pacman.status != PacManStatus.INVISIBLE):
                        self.death()

    def resume(self) -> None:
        self.display.show(self.display.images["maze_screen"], 0, 0)
        self.stats.show_stats()

        self.previous = time.perf_counter()
        self.time = int(self.previous)
        self.accumulator = 0.0

        self.status = GameStatus.RUN

        self.display.mlx.mlx_hook(self.display.win, 2, 1,
                                  self.game_handle_key_press, self.pacman)
        self.display.mlx.mlx_loop_hook(self.display.mlx_ptr,
                                       self.playing, None)

    def next_level(self) -> None:
        # print("New level")
        self.stats.increase_level()
        if self.stats.stats["level"] > len(self.config.level):
            self.victory()
            return
        self.create_level(self.stats.stats["level"])
        if self.status == GameStatus.ERROR:
            print("\033[91mAn unexpected error occured.\033[0m")
            self.exit()
            return
        self.stats.reset_time()
        self.pacman.speed_reset()
        self.pacman.direction = None
        self.pacman.direction_next = None
        self.pacman.set_image("right")
        self.resume()

    def start(self) -> None:
        self.display.clear_window()
        self.score_menu_cur = 0
        self.player_name = ""
        # print("Let's start!")
        self.stats.reset_stats()
        self.pacman.status = PacManStatus.NORMAL
        self.pacman.speed_reset()
        self.pacman.direction = None
        self.pacman.direction_next = None
        self.pacman.set_image("right")
        self.create_level(self.stats.stats["level"])
        if self.status == GameStatus.ERROR:
            print("\033[91mAn unexpected error occured.\033[0m")
            self.exit()
            return
        for ghost in self.ghosts:
            ghost.make_freeze(False)
            ghost.reborn()
        self.resume()

    #
    # HIGHSCORES SCREEN
    #

    def highscores_over_handle_key_press(self, key: int, nothing: Any) -> None:
        # print(f"PAUSE Pressed key {key}")
        if key == 65307:  # ESC
            self.menu()
            return
        if key == 65293 or key == 65421:  # ENTER
            if self.hs_menu_list[self.hs_menu_cur][1] == "clear":
                # print("clear highscores")
                clear_highscores_file(self.config.highscore_filename)
                if self.display.images.get("highscores_screen"):
                    self.display.mlx.mlx_destroy_image(
                        self.display.mlx_ptr,
                        self.display.images["highscores_screen"].img
                        )
                    self.display.images.pop("highscores_screen")
                self.highscores()
                return
            if self.hs_menu_list[self.hs_menu_cur][1] == "main_menu":
                self.menu()
                return
        if key == 65362 or key == 65361:
            self.hs_menu_cur -= 1
            if self.hs_menu_cur < 0:
                self.hs_menu_cur = len(self.hs_menu_list) - 1
            self.highscores()
        elif key == 65364 or key == 65363:
            self.hs_menu_cur += 1
            if self.hs_menu_cur >= len(self.hs_menu_list):
                self.hs_menu_cur = 0
            self.highscores()

    def show_highscores_menu(self) -> None:
        pos_x_1 = self.display.screen_width // 2 - \
            (self.display.images["button"].width + 20)
        pos_y = self.display.screen_height - \
            self.display.images["button"].height - 100
        for i in range(len(self.hs_menu_list)):
            pos_x = pos_x_1 + (self.display.images["button"].width + 20) * i
            self.display.show_button(self.hs_menu_list[i][0],
                                     pos_x, pos_y,
                                     ("hover" if i == self.hs_menu_cur
                                      else "normal"),
                                     "highscores_screen")

    def highscores(self) -> None:
        if not self.display.images.get("highscores_screen"):
            self.display.create_bitmap("highscores_screen",
                                       self.display.screen_width,
                                       self.display.screen_height)

            self.display.add_to_bitmap("highscores_screen", "big_background",
                                       0, 0)

            self.display.show_filled_block(self.display.images["emptiness"],
                                           400, 50, 31, 20, 4, 4,
                                           "highscores_screen")

            hs_json = open_highscores_file(self.config.highscore_filename)
            if hs_json:
                highscores_str = "".join(rec["name"] + " - " +
                                         str(rec["score"])[:21] + "\n"
                                         for rec in sorted(
                                             hs_json,
                                             key=lambda rec: rec['score'],
                                             reverse=True
                                             )[0:10])
                self.display.show_text(highscores_str,
                                       420, 80,
                                       "left", "highscores_screen")

        self.show_highscores_menu()
        self.display.show(self.display.images["highscores_screen"], 0, 0)

        self.display.mlx.mlx_hook(self.display.win, 2, 1,
                                  self.highscores_over_handle_key_press,
                                  None)

    #
    # INSTRUCTIONS SCREEN
    #

    def instructions(self) -> None:
        if not self.display.images.get("instructions_screen"):
            self.display.create_bitmap("instructions_screen",
                                       self.display.screen_width,
                                       self.display.screen_height)

            self.display.add_to_bitmap("instructions_screen", "big_background",
                                       0, 0)
            logo_pos_x = self.display.screen_width // 2 - \
                self.display.images["logo_big"].width // 2
            self.display.add_to_bitmap("instructions_screen", "logo_big",
                                       logo_pos_x, 50)
            self.display.show_filled_block(self.display.images["emptiness"],
                                           500, 350, 25, 16, 4, 4,
                                           "instructions_screen")
            self.display.show_text("Use arrows to play.\n"
                                   "Press ESC to pause.\n"
                                   "Secret cheats:\n"
                                   "L - add extra live\n"
                                   "S - increase player speed\n"
                                   "F - freeze enemies\n"
                                   "I - invincibility\n"
                                   "N - Skip level",
                                   520, 370,
                                   "left", "instructions_screen")

        self.display.show(self.display.images["instructions_screen"], 0, 0)

        self.display.mlx.mlx_hook(self.display.win, 2, 1,
                                  self.no_score_menu_handle_key_press,
                                  self.menu_cur)

    def create_save_score_templates(self) -> None:
        if self.display.images.get("save_score_tmp"):
            return

        self.display.create_bitmap("save_score_tmp",
                                   self.display.screen_width,
                                   self.display.screen_height)
        self.display.add_to_bitmap("save_score_tmp", "big_background", 0, 0)

        # for i in range(10):
        plants: list[str] = [name for name in self.display.images.keys()
                             if name.startswith("plant_")] * 20
        for plant in plants:
            rand_x = random.randint(0, 450)
            rand_y = random.randint(0, self.display.screen_height - 25)
            if random.getrandbits(1):
                rand_x += 1430

            self.display.add_to_bitmap("save_score_tmp", plant, rand_x, rand_y)

        self.display.show_text("Your score:\nEnter your name:",
                               700, 500, "align", "save_score_tmp")
        self.display.show_filled_block(self.display.images["emptiness"],
                                       700, 640, 13, 2, 4, 4,
                                       "save_score_tmp")

        pos_x_1 = self.display.screen_width // 2 - \
            (self.display.images["button"].width + 20)
        pos_y = self.display.screen_height - \
            self.display.images["button"].height - 100
        for i in range(len(self.score_menu_list)):
            pos_x = pos_x_1 + (self.display.images["button"].width + 20) * i
            self.display.show_button(self.score_menu_list[i][0],
                                     pos_x, pos_y,
                                     "normal",
                                     "save_score_tmp")
