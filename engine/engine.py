from mlx import Mlx


mlx = Mlx()


class Engine:

    def __init__(self,  win_w: int, win_h: int):
        self.win_w = win_w
        self.win_h = win_h
        self.mlx_ptr = mlx.mlx_init()
        self.win = mlx.mlx_new_window(self.mlx_ptr,
                                      self.win_w, self.win_h, "Packman")
        self.img = mlx.mlx_new_image(self.mlx_ptr, self.win_w, self.win_h)
        self.data, self.bpp, self.size_line, self.img_format = (
            mlx.mlx_get_data_addr(self.img))
        self.order = "little" if self.img_format == 0 else "big"
        pass

    def pack(self, color: int, order="big"):
        return color.to_bytes(4, order)

    def fill_ret(self, px, py, w, h, colour):
        packed = self.pack(colour, self.order)
        for yy in range(py, py + h):
            base = yy * self.size_line
            for xx in range(px, px + w):
                off = base + xx * 4
                self.data[off:off + 4] = packed

    def onClose(self, _param: object):
        mlx.mlx_loop_exit(self.mlx_ptr)

    def onClick(self, button, x, y, _param: object):
        if button == 1:
            print("Botão esquerdo do mouse pressionado em:", x, y)
        elif button == 3:
            print("Botão direito do mouse pressionado em:", x, y)

    def run(self):
        print(self.data)
        mlx.mlx_put_image_to_window(self.mlx_ptr, self.win, self.img, 0, 0)
        mlx.mlx_hook(self.win, 33, 0, self.onClose, None)
        mlx.mlx_mouse_hook(self.win, self.onClick, None)
        mlx.mlx_loop(self.mlx_ptr)
