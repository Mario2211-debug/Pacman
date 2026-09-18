from os import listdir
from os.path import isfile, join
# from time import sleep

from os import listdir
from os.path import isfile, join

from mlx import Mlx
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .game import Game

class ImgData:
    """Structure for image data"""
    def __init__(self):
        self.img = None
        self.width = 0
        self.height = 0
        self.data = None
        self.sl = 0  # size line
        self.bpp = 0  # bits per pixel
        self.iformat = 0
        self.name = None

class Display:
    """Structure for main vars"""
    def __init__(self):
        try:
            self.mlx = Mlx()
        except Exception as e:
            raise Exception("Error: Can't initialize MLX")
        self.mlx_ptr = self.mlx.mlx_init()
        screen_size = self.mlx.mlx_get_screen_size(self.mlx_ptr)
        self.screen_width = screen_size[1]
        self.screen_height = screen_size[2]
        try:
            self.win = self.mlx.mlx_new_window(self.mlx_ptr, self.screen_width, self.screen_height, "Pac-Man")
            if not self.win:
                raise Exception("Can't create main window")
        except Exception as e:
            raise("Can't create main window")

        self.game: Game
        self.images: dict[str, ImgData] = {}

        self.corridor_width = 36
        self.wall_width = 10
        self.cell_width = self.corridor_width + self.wall_width

    def show(self, img: ImgData, x: int, y: int) -> None:
        self.mlx.mlx_put_image_to_window(self.mlx_ptr, self.win, img.img, x, y)

    def clear_window(self) -> None:
        self.mlx.mlx_clear_window(self.mlx_ptr, self.win)

    def load_all_images(self) -> None:
        try:
            for file in [f for f in listdir("img/chars/letters") if isfile(join("img/chars/letters", f)) and f.endswith(".png")]:
                self.load_image(file[0], join("img/chars/letters", file))
            for file in [f for f in listdir("img/chars/numbers") if isfile(join("img/chars/numbers", f)) and f.endswith(".png")]:
                self.load_image(file[0], join("img/chars/numbers", file))

            self.load_image(":", "img/chars/colon.png")
            self.load_image(",", "img/chars/comma.png")
            self.load_image(".", "img/chars/dot.png")
            self.load_image("=", "img/chars/equal.png")
            self.load_image("!", "img/chars/exclamation.png")
            self.load_image("-", "img/chars/minus.png")
            self.load_image("+", "img/chars/plus.png")
            self.load_image("?", "img/chars/question.png")

            self.load_image("logo_small", "img/logo_400.png")
            self.load_image("logo_big", "img/logo_800.png")
            self.load_image("game_over", "img/game_over_800.png")
            self.load_image("victory", "img/victory_800.png")
            self.load_image("background1", "img/walls_128.png")
            self.load_image("background2", "img/walls_256.png")
            self.load_image("emptiness", "img/emptiness.png")
            self.load_image("button", "img/button.png")
            self.load_image("button_hover", "img/button_hover.png")

            self.create_background("background2", "big_background", self.screen_width // self.images["background2"].width + 1, self.screen_height // self.images["background2"].height + 1)
            self.create_background("background1", "background_left", 10, self.screen_height // self.images["background1"].height + 1)
            self.create_background("background2", "background_right", 3, self.screen_height // self.images["background2"].height + 1)
            # self.create_background("emptiness", "stat_window", 13, 2)

            self.load_image("pacman_right", "img/pacman_24.png")
            self.create_mask("pacman_right", "pacman_right_mask")
            self.create_mirror("pacman_right", "pacman_left")
            self.create_mask("pacman_left", "pacman_left_mask")
            self.create_rotate90("pacman_right", "pacman_bottom")
            self.create_mask("pacman_bottom", "pacman_bottom_mask")
            self.create_rotate90("pacman_left", "pacman_top")
            self.create_mask("pacman_top", "pacman_top_mask")

            for file in [f for f in listdir("img/ghosts") if isfile(join("img/ghosts", f)) and f.endswith(".png")]:
                name = file.rstrip(".png")
                self.load_image(name + "_right", join("img/ghosts", file))
                self.create_mask(name + "_right", name + "_right_mask")
                self.create_mirror(name + "_right", name + "_left")
                self.create_mask(name + "_left", name + "_left_mask")

        except Exception as e:
            raise(e)

    def load_image(self, name: str, img: str) -> None:
        new_img = ImgData()
        result = self.mlx.mlx_png_file_to_image(self.mlx_ptr, img)
        if not result:
            raise Exception(f"Can't load PNG {img}")
        new_img.img, new_img.width, new_img.height = result
        if not new_img.img:
            raise Exception(f"Can't create png {name}")
        new_img.data, new_img.bpp, new_img.sl, new_img.iformat = \
            self.mlx.mlx_get_data_addr(new_img.img)
        new_img.name = name
        self.images.update({name: new_img})

    def create_mask(self, source: str, name_new: str) -> ImgData:
        new_img = ImgData()
        new_img.width = self.images[source].width
        new_img.height = self.images[source].height
        new_img.img = self.mlx.mlx_new_image(self.mlx_ptr, new_img.width, new_img.height)
        if not new_img.img:
            raise Exception(f"Can't create image {source}")
        new_img.data, new_img.bpp, new_img.sl, new_img.iformat = \
            self.mlx.mlx_get_data_addr(new_img.img)
        for i in range(0, new_img.sl * new_img.height, 4):
            color = 0xFF000000
            if self.images[source].data[i + 3] == 0:
                color = 0x00000000
            new_img.data[i:i + 4] = color.to_bytes(4, 'little')
        new_img.name = name_new
        self.images.update({name_new: new_img})

    def create_mirror(self, source: str, name_new: str) -> ImgData:
        new_img = ImgData()
        new_img.width = self.images[source].width
        new_img.height = self.images[source].height
        new_img.img = self.mlx.mlx_new_image(self.mlx_ptr, new_img.width, new_img.height)
        if not new_img.img:
            raise Exception(f"Can't create image {source}")
        new_img.data, new_img.bpp, new_img.sl, new_img.iformat = \
            self.mlx.mlx_get_data_addr(new_img.img)

        for y in range(0, self.images[source].height):
            for x in range(0, self.images[source].sl, 4):
                pos = x + (y * new_img.sl)
                pos_new = new_img.sl - x - 4 + y * new_img.sl
                # print(pos, "=>", pos_new)
                new_img.data[pos_new:pos_new + 4] = self.images[source].data[pos:pos + 4]
        new_img.name = name_new
        self.images.update({name_new: new_img})

        # j = self.images[source].sl * self.images[source].height
        # for i in range(0, self.images[source].sl * self.images[source].height, 4):
        #     j -= 4
        #     new_img.data[j:j + 4] = self.images[source].data[i:i + 4]
        # new_img.name = name_new
        # self.images.update({name_new: new_img})

    def create_rotate90(self, source: str, name_new: str) -> ImgData:
        new_img = ImgData()
        new_img.width = self.images[source].height
        new_img.height = self.images[source].width
        new_img.img = self.mlx.mlx_new_image(self.mlx_ptr, new_img.width, new_img.height)
        if not new_img.img:
            raise Exception(f"Can't create image {source}")
        new_img.data, new_img.bpp, new_img.sl, new_img.iformat = \
            self.mlx.mlx_get_data_addr(new_img.img)
        for y in range(0, self.images[source].height):
            for x in range(0, self.images[source].sl, 4):
                pos = x + (y * new_img.sl)
                pos_new = (self.images[source].height - y - 1) * 4 + x * self.images[source].height
                # print(pos, "=>", pos_new)
                new_img.data[pos_new:pos_new + 4] = self.images[source].data[pos:pos + 4]
        new_img.name = name_new
        self.images.update({name_new: new_img})

    def create_rectangle(self, name_new: str, width: int, height: int, color) -> None:
        new_img = ImgData()
        new_img.width = width
        new_img.height = height
        new_img.img = self.mlx.mlx_new_image(self.mlx_ptr,
                                             new_img.width, new_img.height)
        if not new_img.img:
            raise Exception(f"Can't create image {name_new}")
        new_img.data, new_img.bpp, new_img.sl, new_img.iformat = \
            self.mlx.mlx_get_data_addr(new_img.img)
        # Fill image with color
        for i in range(0, new_img.sl * new_img.height, 4):
            new_img.data[i:i + 4] = color.to_bytes(4, 'little')
        new_img.name = name_new
        self.images.update({name_new: new_img})

    def create_background(self, source: str, name_new: str, num_x: int, num_y: int) -> None:
        new_img = ImgData()
        new_img.width = self.images[source].height * num_x
        new_img.height = self.images[source].width * num_y
        new_img.img = self.mlx.mlx_new_image(self.mlx_ptr, new_img.width, new_img.height)
        if not new_img.img:
            raise Exception(f"Can't create image {name_new}")
        new_img.data, new_img.bpp, new_img.sl, new_img.iformat = \
            self.mlx.mlx_get_data_addr(new_img.img)
        # for i in range(0, new_img.sl * new_img.height, 4):
        #     new_img.data[i:i + 4] = (0x00000000).to_bytes(4, 'little')
        for pos_x in range(num_x):
            for pos_y in range(num_y):
                for y in range(0, self.images[source].height):
                    for x in range(0, self.images[source].sl, 4):
                        pos = x + (y * self.images[source].sl)
                        pos_new = pos_x * self.images[source].sl + x +  ((pos_y * self.images[source].height + y) * new_img.sl)
                        new_img.data[pos_new:pos_new + 4] = self.images[source].data[pos:pos + 4]
        new_img.name = name_new
        self.images.update({name_new: new_img})

    def create_matrix(self, name_new: str, width, height) -> None:
        if self.images.get(name_new):
            self.mlx.mlx_destroy_image(self.mlx_ptr, self.images.get(name_new).img)
        self.create_rectangle(name_new, width, height, 0xFF000000)

    def add_to_matrix(self, matrix: str, source: str, pos_x: int, pos_y: int) -> None:
        for y in range(0, self.images[source].height):
            for x in range(0, self.images[source].sl, 4):
                pos = x + (y * self.images[source].sl)
                if self.images[source].data[pos + 3] < 50:
                    continue
                pos_new = pos_x * 4 + x + ((pos_y + y) * self.images[matrix].sl)
                # print(pos, "=>", pos_new)
                self.images[matrix].data[pos_new:pos_new + 4] = self.images[source].data[pos:pos + 4]

    def create_maze_matrix(self):
        # self.create_matrix("maze_matrix", self.game.maze_width * self.cell_width * 2, self.game.maze_height * self.cell_width * 2)
        self.create_matrix("maze_matrix", int(self.screen_width * 1.3), int(self.screen_height * 1.3))
        self.add_to_matrix("maze_matrix", "background_left", 0, 0)
        self.add_to_matrix("maze_matrix", "background_right", 1350, 0)
        self.add_to_matrix("maze_matrix", "logo_small", 1450, 50)
        pos_y = 0
        for y in range(self.game.maze_height):
            pos_y += self.corridor_width
            pos_x = 0
            for x in range(self.game.maze_width):
                pos_x += self.corridor_width
                if self.game.maze[y][x] == 15:
                    pos_x += self.wall_width
                    # self.add_to_matrix("maze_matrix", "block_42_img", pos_x, pos_y + self.wall_width)
                    continue

                if not self.game.maze[y][x] & 8:
                    # print(x, y, "don't has left wall")
                    self.add_to_matrix("maze_matrix", "emptiness", pos_x, pos_y + self.wall_width)
                pos_x += self.wall_width
                if not self.game.maze[y][x] & 1:
                    # print(x, y, "don't has top wall")
                    # print("add_to_matrix:", self.images["maze_matrix"].width, self.images["maze_matrix"].height, pos_x, pos_y)
                    self.add_to_matrix("maze_matrix", "emptiness", pos_x, pos_y)

                self.add_to_matrix("maze_matrix", "emptiness", pos_x, pos_y + self.wall_width)

                if self.game.pacgums[y][x] == 1:
                    self.show_pacgum(x, y, "small")
                elif self.game.pacgums[y][x] == 2:
                    self.show_pacgum(x, y, "big")

            pos_y += self.wall_width


    def show_filled_block(self, img: ImgData, x: int, y: int, num_x: int, num_y: int, shift_x: int = 0, shift_y: int = 0) -> None:
        img_width = img.width - shift_x
        img_height = img.height - shift_x
        for i in range(num_x):
            pos_x = x + img_width * i
            for j in range(num_y):
                # self.show(img, pos_x, y + img_height * j)
                self.add_to_matrix("maze_matrix", img.name, pos_x, y + img_height * j)

    def show_pacgum(self, x: int, y: int, type: str) -> None:
        pos_x = (x + 1) * (self.corridor_width + self.wall_width)
        pos_y = y * (self.corridor_width + self.wall_width) + self.corridor_width
        # pos_y = (y + 1) * (self.corridor_width) + y * self.wall_width
        if type == "small":
            self.add_to_matrix("maze_matrix", ".", pos_x + 5, pos_y + self.wall_width + 5)
        elif type == "big":
            self.add_to_matrix("maze_matrix", "+", pos_x, pos_y + self.wall_width)
        # pos_x = (x + 1) * (self.corridor_width + self.wall_width)
        # pos_y = y * (self.corridor_width + self.wall_width) + self.corridor_width
        # # pos_y = (y + 1) * (self.corridor_width) + y * self.wall_width
        # if type == "small":
        #     self.show(self.images["."], pos_x + 5, pos_y + self.wall_width + 5)
        # elif type == "big":
        #     self.show(self.images["+"], pos_x, pos_y + self.wall_width)

    def show_maze(self):
        pos_y = 0
        for y in range(self.game.maze_height):
            pos_y += self.corridor_width
            pos_x = 0
            for x in range(self.game.maze_width):
                pos_x += self.corridor_width
                if self.game.maze[y][x] == 15:
                    pos_x += self.wall_width
                    self.show(self.images["block_42_img"], pos_x, pos_y + self.wall_width)
                    continue

                if not self.game.maze[y][x] & 8:
                    # print(x, y, "don't has left wall")
                    self.show(self.images["emptiness"], pos_x, pos_y + self.wall_width)
                pos_x += self.wall_width
                if not self.game.maze[y][x] & 1:
                    # print(x, y, "don't has top wall")
                    self.show(self.images["emptiness"], pos_x, pos_y)

                self.show(self.images["emptiness"], pos_x, pos_y + self.wall_width)

                if self.game.pacgums[y][x] == 1:
                    self.show_pacgum(x, y, "small")
                elif self.game.pacgums[y][x] == 2:
                    self.show_pacgum(x, y, "big")

            pos_y += self.wall_width

    def show_text(self, text: str, x: int, y: int, align: str = "left", matrix: str | None = None) -> None:
        if align == "center":
            max_height = 0
            text_width =  0
            for letter in text.lower():
                if letter == " ":
                    text_width += self.images.get(".").width
                    continue
                letter_img = self.images.get(letter)
                if letter_img:
                    text_width += letter_img.width
                    max_height = max(max_height, letter_img.height)
            x = x - text_width // 2
            y = y - max_height // 2

        pos_x = x
        pos_y = y
        for letter in text.lower():
            if letter == "\n":
                pos_x = x
                pos_y += int(self.images.get("q").height * 1.5)
            elif letter == " ":
                pos_x += self.images.get(".").width
            else:
                letter_img = self.images.get(letter)
                if letter_img:
                    if not matrix:
                        self.show(letter_img, pos_x, pos_y)
                    else:
                        self.add_to_matrix(matrix, letter_img.name, pos_x, pos_y)
                    pos_x += letter_img.width


    def show_button(self, text: str, x: int, y: int, type: str = "normal"):
        if type == "hover":
            self.show(self.images["button_hover"], x, y)
        else:
            self.show(self.images["button"], x, y)
        self.show_text(text,
                       x + self.images["button"].width // 2,
                       y + self.images["button"].height // 2,
                       "center")