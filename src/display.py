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

    def show(self, img, x: int, y: int) -> None:
        self.mlx.mlx_put_image_to_window(self.mlx_ptr, self.win, img.img, x, y)

    def clear_all(self) -> None:
        self.mlx.mlx_clear_window(self.mlx_ptr, self.win)

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

    def create_block_image(self, name: str, width: int, height: int, color) -> None:
        new_img = ImgData()
        new_img.width = width
        new_img.height = height
        new_img.img = self.mlx.mlx_new_image(self.mlx_ptr, new_img.width, new_img.height)
        if not new_img.img:
            raise Exception(f"Can't create image {name}")
        new_img.data, new_img.bpp, new_img.sl, new_img.iformat = \
            self.mlx.mlx_get_data_addr(new_img.img)
        # Fill image with color
        for i in range(0, new_img.sl * new_img.width, 4):
            new_img.data[i:i + 4] = color.to_bytes(4, 'little')
        self.images.update({name: new_img})

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
