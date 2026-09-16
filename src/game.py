from enum import Enum
from typing import TYPE_CHECKING

from .types import GameStatus
from .display import Display
from mazegenerator import MazeGenerator

if TYPE_CHECKING:
    from .pacman import PacMan
    from .ghost import Ghost
    from .config import Config

class Game:
    def __init__(self):
        self.config: Config
        self.pacman: PacMan
        self.ghosts: list[Ghost]
        self.display: Display
        self.status = GameStatus.RUN
        self.level = 1
        self.points = 0
        self.maze: list[list[int]] = []
        if self.maze:
            self.maze_width = len(self.maze[0])
            self.maze_height = len(self.maze)
        self.pacgums: list[list[int]] = []

        self.menu_list = [("Start game", "start"),
                ("Highscores", "highscores"),
                ("Instructions", "instructions"),
                ("Exit", "exit")]
        self.menu_current = 0

        self.pause_menu_list = [("Resume", "resume"),
                ("Main menu", "main_menu")]
        self.pause_menu_current = 0

    def set_maze(self, maze: list[list[int]]) -> None:
        self.maze = maze
        if maze:
            self.maze_width = len(maze[0])
            self.maze_height = len(maze)

    def exit(self, error = ""):
        for image in self.display.images.values():
            self.display.mlx.mlx_destroy_image(self.display.mlx_ptr, image.img)
        self.display.mlx.mlx_loop_exit(self.display.mlx_ptr)
        # exit()

    # MENU SCREEN

    def menu_handle_key_press(self, key, current_hover):
        # print(f"Pressed key {key}")
        if key == 65293:
            if self.menu_list[self.menu_current][1] == "exit":
                self.exit()
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
            self.display.show_button(pos_x, pos_y,
                                     self.menu_list[i][0],
                                     ("hover" if i == self.menu_current else "normal"))

    def menu(self) -> None:
        if not self.display:
            return
        # self.display.clear_window()
        self.display.show_filled_block(self.display.images["background1"], 0, 0,
                                       self.display.screen_width // self.display.images["background1"].width + 1,
                                       self.display.screen_height // self.display.images["background1"].height + 1)
        self.display.show(self.display.images["logo_big"],
                          self.display.screen_width // 2
                          - self.display.images["logo_big"].width // 2,
                          50)
        self.show_menu()
        self.display.mlx.mlx_hook(self.display.win, 2, 1, self.menu_handle_key_press, self.menu_current)

    # PAUSE SCREEN

    def pause_menu_handle_key_press(self, key, current_hover) -> None:
        # print(f"PAUSE Pressed key {key}")
        if key == 65293:
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
            self.display.show_button(pos_x, pos_y,
                                     self.pause_menu_list[i][0],
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


    # GAME SCREEN
