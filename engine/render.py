import sys
from os import listdir
from os.path import isfile, join
from models.ImageModel import ImgData
from mazegenerator import MazeGenerator
# mlx_string_put draws each glyph as 10x20 px with y at the top
# (disassembled from libmlx.so, the font atlas cells are 12 px wide)
CHAR_W = 10
CHAR_H = 20


class Render:
    def __init__(self, ptr, mlx, win, win_w,
                 win_h, data, size_line, img_format):
        self.mlx = mlx
        self.win = win
        self.ptr = ptr
        self.data = data
        self.width = win_w
        self.height = win_h
        self.text_queue = []
        self.wall_width = 10
        self.corridor_width = 36
        self.size_line = size_line
        self.img_format = img_format
        self.clear_cache = (None, b"")
        self.images: dict[str, ImgData] = {}
        self.order = "little" if self.img_format == 0 else "big"

    def pack(self, color: int):
        r = (color >> 24) & 0xFF
        g = (color >> 16) & 0xFF
        b = (color >> 8) & 0xFF
        a = color & 0xFF

        if self.order == "little":
            return bytes([b, g, r, a])
        else:
            return bytes([a, r, g, b])

    def clear(self, colour):
        cached_colour, frame = self.clear_cache
        if cached_colour != colour:
            frame = self.pack(colour) * (len(self.data) // 4)
            self.clear_cache = (colour, frame)
        self.data[:] = frame

    def fill_rect(self, px, py, w, h, colour):
        x0, x1 = max(px, 0), min(px + w, self.width)
        y0, y1 = max(py, 0), min(py + h, self.height)
        if x0 >= x1 or y0 >= y1:
            return
        row = self.pack(colour) * (x1 - x0)
        for yy in range(y0, y1):
            base = yy * self.size_line
            self.data[base + x0 * 4:base + x1 * 4] = row

    def draw_rect(self, px, py, w, h, colour, thickness=1):
        self.fill_rect(px, py, w, thickness, colour)
        self.fill_rect(px, py + h - thickness, w, thickness, colour)
        self.fill_rect(px, py, thickness, h, colour)
        self.fill_rect(px + w - thickness, py, thickness, h, colour)

    def to_mlx_color(self, color: int):
        r = (color >> 24) & 0xFF
        g = (color >> 16) & 0xFF
        b = (color >> 8) & 0xFF
        a = color & 0xFF
        return int.from_bytes(bytes([b, g, r, a]), sys.byteorder)

    def text_width(self, text: str):
        return len(text) * CHAR_W

    def draw_text(self, text: str, x: int, y: int, color: int):
        self.text_queue.append((text, x, y, color))

    def draw_text_centered(self, text: str, cx: int, y: int, color: int):
        self.draw_text(text, max(0, cx - self.text_width(text) // 2), y, color)

    def flush_text(self):
        for text, x, y, color in self.text_queue:
            self.mlx.mlx_string_put(self.ptr, self.win, x, y,
                                    self.to_mlx_color(color), text)
        self.text_queue.clear()

    def tile_image(self, img, x, y, w, h):
        x0, x1 = max(x, 0), min(x + w, self.width)
        y0, y1 = max(y, 0), min(y + h, self.height)
        if x0 >= x1 or y0 >= y1:
            return
        rows = []
        reps = (x1 - x0) // img.width + 2
        start = ((x0 - x) % img.width) * 4
        for ty in range(img.height):
            src = bytes(img.data[ty * img.sl:ty * img.sl + img.width * 4])
            rows.append((src * reps)[start:start + (x1 - x0) * 4])
        for yy in range(y0, y1):
            base = yy * self.size_line
            self.data[base + x0 * 4:base + x1 * 4] = rows[(yy - y) % img.height]

    def draw_maze(self, maze, x, y, cell, wall, wall_img,
                  corridor_color, block_color):
        width, height = len(maze[0]), len(maze)
        self.tile_image(wall_img, x, y, width * cell + wall,
                        height * cell + wall)
        inner = cell - wall
        for cy, row in enumerate(maze):
            for cx, walls in enumerate(row):
                px, py = x + cx * cell + wall, y + cy * cell + wall
                if walls == 15:
                    self.fill_rect(px, py, inner, inner, block_color)
                    continue
                self.fill_rect(px, py, inner, inner, corridor_color)
                if not walls & 2 and cx + 1 < width:
                    self.fill_rect(px + inner, py, wall, inner, corridor_color)
                if not walls & 4 and cy + 1 < height:
                    self.fill_rect(px, py + inner, inner, wall, corridor_color)


    def show(self, img: ImgData, x: int, y: int) -> None:
        self.mlx.mlx_put_image_to_window(self.ptr, self.win, img.img, x, y)

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

            self.load_image("logo", "img/logo_400.png")
            self.load_image("background1", "img/walls_100.png")
            self.load_image("background2", "img/walls_200.png")
            self.load_image("emptiness", "img/emptiness.png")
            self.load_image("pacman", "img/pacman_24.png")

            self.load_image("ghost_red", "img/ghosts/red.png")
            self.load_image("ghost_blue", "img/ghosts/blue.png")
            self.load_image("ghost_orange", "img/ghosts/orange.png")
            self.load_image("ghost_pink", "img/ghosts/pink.png")
            self.load_image("ghost_dead", "img/ghosts/dead.png")
        except Exception as e:
            raise (e)

    def load_image(self, name: str, img: str) -> None:
        new_img = ImgData()
        result = self.mlx.mlx_png_file_to_image(self.ptr, img)
        if not result:
            raise RuntimeError(f"mlx_png_file_to_image returned None for {img}")
        new_img.img, new_img.width, new_img.height = result
        new_img.data, new_img.bpp, new_img.sl, new_img.iformat = \
            self.mlx.mlx_get_data_addr(new_img.img)
        self.images[name] = new_img

    def create_rectangle(self, name: str, width: int,
                         height: int, color) -> None:
        new_img = ImgData()
        new_img.width = width
        new_img.height = height
        new_img.img = self.mlx.mlx_new_image(self.ptr,
                                             new_img.width, new_img.height)
        if not new_img.img:
            raise Exception(f"Can't create image {name}")
        new_img.data, new_img.bpp, new_img.sl, new_img.iformat = \
            self.mlx.mlx_get_data_addr(new_img.img)
        # Fill image with color
        for i in range(0, new_img.sl * new_img.width, 4):
            new_img.data[i:i + 4] = color.to_bytes(4, 'little')
        self.images.update({name: new_img})

    def show_filled_block(self, img: ImgData, x: int, y: int,
                          num_x: int, num_y: int, shift_x: int = 0,
                          shift_y: int = 0) -> None:
        for i in range(num_x):
            for j in range(num_y):
                self.show(img, x + (img.width - shift_x) * i,
                          y + (img.height - shift_y) * j)

    def create_text(self, text: str, x: int, y: int) -> None:
        pos_x = x
        pos_y = y
        for letter in text.lower():
            if letter == "\n":
                pos_x = x
                pos_y += int(self.images.get("q").height * 1.5)
            elif letter == " ":
                pos_x += self.images.get("i").width
            else:
                letter_img = self.images.get(letter)
                if letter_img:
                    self.show(letter_img, pos_x, pos_y)
                    pos_x += letter_img.width

    def clear_all(self) -> None:
        self.mlx.mlx_clear_window(self.ptr, self.win)

    def gen_maze(self, width: int, height: int, perfect: bool,
                 start: tuple, end: tuple, seed: int):
        mazegen = MazeGenerator((width, height), perfect, start, end, seed)
        pos_y = 0
        for y in range(height):
            pos_y += self.corridor_width
            pos_x = 0
            for x in range(width):
                pos_x += self.corridor_width
                if mazegen.maze[y][x] == 15:
                    pos_x += self.wall_width
                    self.show(self.images["block_42_img"],
                              pos_x, pos_y + self.wall_width)
                    continue

                if not mazegen.maze[y][x] & 8:
                    # print(x, y, "don't has left wall")
                    self.show(self.images["emptiness"],
                              pos_x, pos_y + self.wall_width)
                pos_x += self.wall_width
                if not mazegen.maze[y][x] & 1:
                    # print(x, y, "don't has top wall")
                    self.show(self.images["emptiness"], pos_x, pos_y)
                self.show(self.images["emptiness"],
                          pos_x, pos_y + self.wall_width)
            pos_y += self.wall_width

        pass
