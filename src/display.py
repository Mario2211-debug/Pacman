"""MLX window, image loading and every drawing primitive."""

from os import listdir
from os.path import isfile, join
from enum import Enum
import random
from typing import TYPE_CHECKING, Any

from mlx import Mlx
from .game_types import PacManStatus
if TYPE_CHECKING:
    from .game import Game


class ImgType(Enum):
    """What an image is used for: regular, mask or pacman sprite."""
    REGULAR = 0
    MASK = 1
    PACMAN = 2


class ImgData:
    """Structure for image data"""
    def __init__(self) -> None:
        """Create an empty image holder."""
        self.img = None
        self.width = 0
        self.height = 0
        self.data: list[int] = []
        self.sl = 0  # size line
        self.bpp = 0  # bits per pixel
        self.iformat = 0
        self.name: str = ""
        self.type = ImgType.REGULAR


class Display:
    """Structure for main vars"""
    def __init__(self) -> None:
        """Open the MLX window and prepare the image table."""
        try:
            self.mlx = Mlx()
        except Exception:
            raise Exception("Error: Can't initialize MLX")
        self.mlx_ptr = self.mlx.mlx_init()
        screen_size = self.mlx.mlx_get_screen_size(self.mlx_ptr)
        self.screen_width = screen_size[1]
        self.screen_height = screen_size[2]
        try:
            self.win = self.mlx.mlx_new_window(self.mlx_ptr,
                                               self.screen_width,
                                               self.screen_height,
                                               "Pac-Man")
            if not self.win:
                raise Exception("Can't create main window")
        except Exception:
            raise Exception("Can't create main window")

        self.game: Game
        self.images: dict[str, ImgData] = {}

        self.corridor_width = 36
        self.wall_width = 10
        self.cell_width = self.corridor_width + self.wall_width

        self.maze_x = 0
        self.maze_y = 0

    def show(self, img: ImgData, x: int, y: int) -> None:
        """Draw an image on the window at (x, y)."""
        self.mlx.mlx_put_image_to_window(self.mlx_ptr, self.win, img.img, x, y)

    def clear_window(self) -> None:
        """Erase the whole window."""
        self.mlx.mlx_clear_window(self.mlx_ptr, self.win)

    def load_all_images(self) -> None:
        """Load every PNG asset and build the derived images."""
        try:
            for file in [f for f in listdir("img/chars/letters")
                         if (isfile(join("img/chars/letters", f))
                             and f.endswith(".png"))]:
                self.load_image(file[0], join("img/chars/letters", file))
            for file in [f for f in listdir("img/chars/numbers")
                         if (isfile(join("img/chars/numbers", f))
                             and f.endswith(".png"))]:
                self.load_image(file[0], join("img/chars/numbers", file))

            self.load_image(":", "img/chars/colon.png")
            self.load_image(",", "img/chars/comma.png")
            self.load_image(".", "img/chars/dot.png")
            self.load_image("=", "img/chars/equal.png")
            self.load_image("!", "img/chars/exclamation.png")
            self.load_image("-", "img/chars/minus.png")
            self.load_image("+", "img/chars/plus.png")
            self.load_image("?", "img/chars/question.png")

            self.load_image("logo_small", "img/logo_small.png")
            self.load_image("logo_big", "img/logo_big.png")
            self.load_image("game_over", "img/game_over.png")
            self.load_image("time_out", "img/time_out.png")
            self.load_image("level_complete", "img/level_complete.png")
            self.load_image("victory", "img/victory.png")
            self.load_image("background1", "img/walls_128.png")
            self.load_image("background2", "img/walls_256.png")
            self.load_image("emptiness", "img/emptiness.png")
            self.load_image("button", "img/button.png")
            self.load_image("button_hover", "img/button_hover.png")

            self.load_image("pacgum", "img/pacgum_12.png")
            self.load_image("pacgum_big", "img/pacgum_24.png")

            self.create_background("background2", "big_background",
                                   self.screen_width //
                                   self.images["background2"].width + 1,
                                   self.screen_height //
                                   self.images["background2"].height + 1)
            self.create_background("background1", "background_left",
                                   10, self.screen_height //
                                   self.images["background1"].height + 1)
            self.create_background("background2", "background_right",
                                   3, self.screen_height //
                                   self.images["background2"].height + 1)

            for file in [f for f in listdir("img/pacman")
                         if (isfile(join("img/pacman", f))
                             and f.endswith(".png"))]:
                name = file.rstrip(".png")
                self.load_image("pacman_" + name + "_right",
                                join("img/pacman", file))
                self.create_mask("pacman_" + name + "_right",
                                 "pacman_" + name + "_right_mask")
                self.create_mirror("pacman_" + name + "_right",
                                   "pacman_" + name + "_left")
                self.create_mask("pacman_" + name + "_left",
                                 "pacman_" + name + "_left_mask")
                self.create_rotate90("pacman_" + name + "_right",
                                     "pacman_" + name + "_bottom")
                self.create_mask("pacman_" + name + "_bottom",
                                 "pacman_" + name + "_bottom_mask")
                self.create_rotate90("pacman_" + name + "_left",
                                     "pacman_" + name + "_top")
                self.create_mask("pacman_" + name + "_top",
                                 "pacman_" + name + "_top_mask")
                self.images["pacman_" + name + "_right"].type = ImgType.PACMAN
                self.images["pacman_" + name + "_left"].type = ImgType.PACMAN
                self.images["pacman_" + name + "_bottom"].type = ImgType.PACMAN
                self.images["pacman_" + name + "_top"].type = ImgType.PACMAN

            for file in [f for f in listdir("img/ghosts")
                         if (isfile(join("img/ghosts", f))
                             and f.endswith(".png"))]:
                name = file.rstrip(".png")
                self.load_image(name + "_right", join("img/ghosts", file))
                self.create_mask(name + "_right", name + "_right_mask")
                self.create_mirror(name + "_right", name + "_left")
                self.create_mask(name + "_left", name + "_left_mask")

            for file in [f for f in listdir("img/plants")
                         if (isfile(join("img/plants", f))
                             and f.endswith(".png"))]:
                name = file.rstrip(".png")
                self.load_image("plant_" + name, join("img/plants", file))

        except Exception as e:
            raise (e)

    def load_image(self, name: str, img: str) -> None:
        """Load one PNG into the image table under `name`."""
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

    def create_mask(self, source: str, name_new: str) -> None:
        """Build the silhouette of `source`, used to erase it from a bitmap."""
        new_img = ImgData()
        new_img.width = self.images[source].width
        new_img.height = self.images[source].height
        new_img.img = self.mlx.mlx_new_image(self.mlx_ptr,
                                             new_img.width, new_img.height)
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
        new_img.type = ImgType.MASK
        self.images.update({name_new: new_img})

    def create_mirror(self, source: str, name_new: str) -> None:
        """Build a horizontally mirrored copy of `source`."""
        new_img = ImgData()
        new_img.width = self.images[source].width
        new_img.height = self.images[source].height
        new_img.img = self.mlx.mlx_new_image(self.mlx_ptr,
                                             new_img.width, new_img.height)
        if not new_img.img:
            raise Exception(f"Can't create image {source}")
        new_img.data, new_img.bpp, new_img.sl, new_img.iformat = \
            self.mlx.mlx_get_data_addr(new_img.img)

        for y in range(0, self.images[source].height):
            for x in range(0, self.images[source].sl, 4):
                pos = x + (y * new_img.sl)
                pos_new = new_img.sl - x - 4 + y * new_img.sl
                # print(pos, "=>", pos_new)
                new_img.data[pos_new:pos_new + 4] = \
                    self.images[source].data[pos:pos + 4]
        new_img.name = name_new
        self.images.update({name_new: new_img})

    def create_rotate90(self, source: str, name_new: str) -> None:
        """Build a copy of `source` rotated by 90 degrees."""
        new_img = ImgData()
        new_img.width = self.images[source].height
        new_img.height = self.images[source].width
        new_img.img = self.mlx.mlx_new_image(self.mlx_ptr,
                                             new_img.width, new_img.height)
        if not new_img.img:
            raise Exception(f"Can't create image {source}")
        new_img.data, new_img.bpp, new_img.sl, new_img.iformat = \
            self.mlx.mlx_get_data_addr(new_img.img)
        for y in range(0, self.images[source].height):
            for x in range(0, self.images[source].sl, 4):
                pos = x + (y * new_img.sl)
                pos_new = (self.images[source].height - y - 1) * 4 + \
                    x * self.images[source].height
                new_img.data[pos_new:pos_new + 4] = \
                    self.images[source].data[pos:pos + 4]
        new_img.name = name_new
        self.images.update({name_new: new_img})

    def create_rectangle(self, name_new: str,
                         width: int, height: int, color: Any) -> None:
        """Create a width x height image filled with `color`."""
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

    def create_background(self, source: str, name_new: str,
                          num_x: int, num_y: int) -> None:
        """Tile `source` num_x by num_y times into a new image."""
        new_img = ImgData()
        new_img.width = self.images[source].height * num_x
        new_img.height = self.images[source].width * num_y
        new_img.img = self.mlx.mlx_new_image(self.mlx_ptr,
                                             new_img.width, new_img.height)
        if not new_img.img:
            raise Exception(f"Can't create image {name_new}")
        new_img.data, new_img.bpp, new_img.sl, new_img.iformat = \
            self.mlx.mlx_get_data_addr(new_img.img)
        for pos_x in range(num_x):
            for pos_y in range(num_y):
                for y in range(0, self.images[source].height):
                    for x in range(0, self.images[source].sl, 4):
                        pos = x + (y * self.images[source].sl)
                        pos_new = pos_x * self.images[source].sl + x + \
                            ((pos_y * self.images[source].height + y) *
                             new_img.sl)
                        new_img.data[pos_new:pos_new + 4] = \
                            self.images[source].data[pos:pos + 4]
        new_img.name = name_new
        self.images.update({name_new: new_img})

    def create_bitmap(self, name_new: str, width: int, height: int) -> None:
        """Create, or replace, an off-screen bitmap of the given size."""
        img = self.images.get(name_new)
        if img:
            self.mlx.mlx_destroy_image(self.mlx_ptr, img.img)
        self.create_rectangle(name_new, width, height, 0xFF000000)

    def add_to_bitmap(self, bitmap: str, source: str,
                      pos_x: int, pos_y: int) -> None:
        """Blend `source` into `bitmap`, skipping transparent pixels."""
        for y in range(0, self.images[source].height):
            for x in range(0, self.images[source].sl, 4):
                pos = x + (y * self.images[source].sl)
                if self.images[source].data[pos + 3] < 200:
                    continue
                if pos_x * 4 + x >= self.images[bitmap].sl:
                    continue
                pos_new = pos_x*4 + x + ((pos_y + y) * self.images[bitmap].sl)
                if pos_new >= self.images[bitmap].sl * \
                        self.images[bitmap].height:
                    return
                self.images[bitmap].data[pos_new:pos_new + 4] = \
                    self.images[source].data[pos:pos + 4]
                if (self.game.pacman.status == PacManStatus.INVISIBLE
                        and self.images[source].type == ImgType.PACMAN):
                    # print("Invisible pacman")
                    self.images[bitmap].data[pos_new + 3] = 12
                    self.images[bitmap].data[pos_new] = 225

    def create_maze_bitmap(self) -> None:
        """Compose the in-game screen: side panels, logo and plants."""
        self.create_bitmap("maze_screen",
                           self.screen_width, self.screen_height)
        self.add_to_bitmap("maze_screen", "background_left", 0, 0)
        self.add_to_bitmap("maze_screen", "background_right", 1330, 0)
        self.show_filled_block(self.images["emptiness"],
                               1250, 0, 3, 30, 4, 4, "maze_screen")
        self.add_to_bitmap("maze_screen", "logo_small", 1450, 50)
        plants: list[str] = [name for name in self.images.keys()
                             if name.startswith("plant_")]
        self.maze_x = 575 - self.game.maze_width * self.cell_width // 2
        self.maze_y = 465 - self.game.maze_height * self.cell_width // 2
        pos_y = self.maze_y
        for y in range(self.game.maze_height):
            pos_y += self.corridor_width
            pos_x = self.maze_x
            for x in range(self.game.maze_width):
                pos_x += self.corridor_width
                if self.game.maze[y][x] == 15:
                    # print("Closed room")
                    pos_x += self.wall_width
                    self.add_to_bitmap("maze_screen", "emptiness",
                                       pos_x, pos_y + self.wall_width)
                    plant = random.choice(plants)
                    plants.remove(plant)
                    plant_x = pos_x + self.corridor_width // 2 - \
                        self.images[plant].width // 2
                    plant_y = pos_y + self.corridor_width // 2 - \
                        self.images[plant].width // 2 + self.wall_width + 2
                    self.add_to_bitmap("maze_screen", plant,
                                       plant_x, plant_y)
                    continue

                if not self.game.maze[y][x] & 8:
                    # print(x, y, "don't has left wall")
                    self.add_to_bitmap("maze_screen", "emptiness",
                                       pos_x, pos_y + self.wall_width)
                pos_x += self.wall_width
                if not self.game.maze[y][x] & 1:
                    # print(x, y, "don't has top wall")
                    self.add_to_bitmap("maze_screen", "emptiness",
                                       pos_x, pos_y)

                self.add_to_bitmap("maze_screen", "emptiness",
                                   pos_x, pos_y + self.wall_width)

                if self.game.pacgums[y][x] == 1:
                    self.show_pacgum(x, y, "small")
                elif self.game.pacgums[y][x] == 2:
                    self.show_pacgum(x, y, "big")

            pos_y += self.wall_width

    def show_filled_block(self, img: ImgData, x: int, y: int,
                          num_x: int, num_y: int,
                          shift_x: int = 0, shift_y: int = 0,
                          bitmap: str | None = None) -> None:
        """Draw `img` num_x by num_y times, on screen or into a bitmap."""
        img_width = img.width - shift_x
        img_height = img.height - shift_x
        for i in range(num_x):
            pos_x = x + img_width * i
            for j in range(num_y):
                if not bitmap:
                    self.show(img, pos_x, y + img_height * j)
                else:
                    self.add_to_bitmap(bitmap, img.name,
                                       pos_x, y + img_height * j)

    def show_pacgum(self, x: int, y: int, type: str) -> None:
        """Draw a small or big pacgum at the maze cell (x, y)."""
        pos_x = (x + 1) * (self.corridor_width + self.wall_width) + self.maze_x
        pos_y = (y + 1) * (self.corridor_width + self.wall_width) + self.maze_y
        # pos_y = (y + 1) * (self.corridor_width) + y * self.wall_width
        if type == "small":
            self.add_to_bitmap("maze_screen", "pacgum",
                               pos_x + 13, pos_y + 13)
        elif type == "big":
            self.add_to_bitmap("maze_screen", "pacgum_big",
                               pos_x + 7, pos_y + 7)

    def show_text(self, text: str, x: int, y: int,
                  align: str = "left", bitmap: str | None = None) -> None:

        """Draw `text` with the letter images, optionally centered."""
        q_letter = self.images.get("q")
        a_letter = self.images.get("a")
        dot_letter = self.images.get(".")
        if q_letter is None or a_letter is None or dot_letter is None:
            return

        if align == "center":
            max_height = 0
            text_width = 0
            for letter in text.lower():
                if letter == " ":
                    text_width += dot_letter.width
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
                pos_y += int(q_letter.height * 1.5)
            elif letter == " ":
                pos_x += dot_letter.width
            else:
                letter_img = self.images.get(letter)
                if letter_img is not None:
                    pos_x_current = pos_x
                    pos_y_current = pos_y
                    if letter == "." or letter == ",":
                        pos_y_current += int(a_letter.height-dot_letter.height)
                    elif (letter == "-" or letter == "+"
                          or letter == "=" or letter == ":"):
                        pos_y_current += int(a_letter.height//2 -
                                             letter_img.height//2)
                    if not bitmap:
                        self.show(letter_img, pos_x_current, pos_y_current)
                    else:
                        self.add_to_bitmap(bitmap, letter_img.name,
                                           pos_x_current, pos_y_current)
                    pos_x += letter_img.width

    def show_button(self, text: str, x: int, y: int,
                    type: str = "normal", bitmap: str | None = None) -> None:
        """Draw a button and its label, in normal or hover state."""
        if not bitmap:
            if type == "hover":
                self.show(self.images["button_hover"], x, y)
            else:
                self.show(self.images["button"], x, y)
            self.show_text(text,
                           x + self.images["button"].width // 2,
                           y + self.images["button"].height // 2,
                           "center")
        else:
            if type == "hover":
                self.add_to_bitmap(bitmap, "button_hover", x, y)
            else:
                self.add_to_bitmap(bitmap, "button", x, y)
            self.show_text(text,
                           x + self.images["button"].width // 2,
                           y + self.images["button"].height // 2,
                           "center", bitmap)
