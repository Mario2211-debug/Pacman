class Render:
    def __init__(self, ptr, mlx, win, data, size_line, img_format):
        self.mlx = mlx
        self.win = win
        self.ptr = ptr
        self.data = data
        self.size_line = size_line
        self.img_format = img_format
        self.order = "little" if self.img_format == 0 else "big"

    def pack(self, color: int):
        return color.to_bytes(4, self.order)

    def fill_rect(self, px, py, w, h, colour):
        packed = self.pack(colour)
        for yy in range(py, py + h):
            base = yy * self.size_line
            for xx in range(px, px + w):
                off = base + xx * 4
                self.data[off:off + 4] = packed

    def draw_rect(self, px, py, w, h, colour, thickness=1):
        self.fill_rect(px, py, w, thickness, colour)
        self.fill_rect(px, py + h - thickness, w, thickness, colour)
        self.fill_rect(px, py, thickness, h, colour)
        self.fill_rect(px + w - thickness, py, thickness, h, colour)

    def draw_text(self, text: str, x: int, y: int, color: int):
        self.mlx.mlx_string_put(self.ptr, self.win, x, y, color, text)

    def draw_sprite(self):
        pass
