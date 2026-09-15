from engine import keys
from engine.render import CHAR_H

PADDING = 8


class TextInput:
    def __init__(self, x, y, width, max_length=10, on_submit=None,
                 color=0xFFFFFFFF, bg_color=0x1A1A1AFF,
                 border_color=0xFFFF00FF):
        self.x: int = x
        self.y: int = y
        self.value = ""
        self.blink = 0.0
        self.color: int = color
        self.width: int = width
        self.on_submit = on_submit
        self.max_length = max_length
        self.bg_color: int = bg_color
        self.border_color: int = border_color
        self.height: int = CHAR_H + PADDING * 2

    def update(self, dt):
        self.blink = (self.blink + dt) % 1.0

    def handle_key(self, key):
        if key == keys.BACKSPACE:
            self.value = self.value[:-1]
        elif key in (keys.ENTER, keys.KP_ENTER):
            if self.value and self.on_submit:
                self.on_submit(self.value)
        else:
            char = keys.to_char(key)
            if char and len(self.value) < self.max_length:
                self.value += char

    def draw(self, renderer):
        renderer.fill_rect(self.x, self.y, self.width,
                           self.height, self.bg_color)
        renderer.draw_rect(self.x, self.y, self.width, self.height,
                           self.border_color, 2)
        cursor = ""
        if self.blink < 0.5 and len(self.value) < self.max_length:
            cursor = "_"
        renderer.draw_text(self.value + cursor, self.x + PADDING,
                           self.y + PADDING, self.color)
