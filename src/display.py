from os import listdir
from os.path import isfile, join

from os import listdir
from os.path import isfile, join

from mlx import Mlx

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

        self.images: dict[str, ImgData] = {}

        self.corridor_width = 36
        self.wall_width = 10

    def show(self, img: ImgData, x: int, y: int) -> None:
        self.mlx.mlx_put_image_to_window(self.mlx_ptr, self.win, img.img, x, y)

    def clear_all(self) -> None:
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
        self.images.update({name: new_img})

    def create_mask(self, name: str) -> ImgData:
        new_img = ImgData()
        new_img.width = self.images[name].width
        new_img.height = self.images[name].height
        new_img.img = self.mlx.mlx_new_image(self.mlx_ptr, new_img.width, new_img.height)
        if not new_img.img:
            raise Exception(f"Can't create image {name}")
        new_img.data, new_img.bpp, new_img.sl, new_img.iformat = \
            self.mlx.mlx_get_data_addr(new_img.img)
        for i in range(0, new_img.sl * new_img.height, 4):
            color = 0xFF000000
            if self.images[name].data[i + 3] == 0:
                color = 0x00000000
            new_img.data[i:i + 4] = color.to_bytes(4, 'little')
        self.images.update({name+"_mask": new_img})

    def create_rectangle(self, name: str, width: int, height: int, color) -> None:
        new_img = ImgData()
        new_img.width = width
        new_img.height = height
        new_img.img = self.mlx.mlx_new_image(self.mlx_ptr,
                                             new_img.width, new_img.height)
        if not new_img.img:
            raise Exception(f"Can't create image {name}")
        new_img.data, new_img.bpp, new_img.sl, new_img.iformat = \
            self.mlx.mlx_get_data_addr(new_img.img)
        # Fill image with color
        for i in range(0, new_img.sl * new_img.height, 4):
            new_img.data[i:i + 4] = color.to_bytes(4, 'little')
        self.images.update({name: new_img})

    def show_filled_block(self, img: ImgData, x: int, y: int,
                          num_x: int, num_y: int,
                          shift_x: int = 0, shift_y: int = 0) -> None:
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
