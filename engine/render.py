import sys


class Render:
    def __init__(self, ptr, mlx, win, win_w,
                 win_h, data, size_line, img_format):
        self.mlx = mlx
        self.win = win
        self.ptr = ptr
        self.data = data
        self.width = win_w
        self.height = win_h
        self.size_line = size_line
        self.img_format = img_format
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

    def fill_rect(self, px, py, w, h, colour):
        packed = self.pack(colour)
        for yy in range(py, py + h):
            if yy < 0 or yy >= self.height:
                continue
            base = yy * self.size_line
            for xx in range(px, px + w):
                if xx < 0 or xx >= self.width:
                    continue
                off = base + xx * 4
                self.data[off:off + 4] = packed

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

    def draw_text(self, text: str, x: int, y: int, color: int):
        self.mlx.mlx_string_put(self.ptr, self.win, x, y,
                                self.to_mlx_color(color), text)

    def draw_sprite(self):
        pass
