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
        self.text_queue = []

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

    def draw_text(self, text: str, x: int, y: int, color: int):
        self.text_queue.append((text, x, y, color))

    def flush_text(self):
        for text, x, y, color in self.text_queue:
            self.mlx.mlx_string_put(self.ptr, self.win, x, y,
                                    self.to_mlx_color(color), text)
        self.text_queue.clear()

    def draw_sprite(self):
        pass
