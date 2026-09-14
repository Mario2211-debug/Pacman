from engine.render import CHAR_H, CHAR_W
from .text import Text


class Button:
    def __init__(self, x, y, on_click=None, bg_color=0x1A1A1AFF,
                 width=64, height=24, label="", label_color=0xFFFFFFFF,
                 selected_color=0xFFFF00FF):
        self.x: int = x
        self.y: int = y
        self.width: int = width
        self.height: int = height
        self.children: list = []
        self.on_click = on_click
        self.bg_color: int = bg_color
        self.selected_color: int = selected_color
        self.selected: bool = False
        if label:
            self.add(Text(x + (width - len(label) * CHAR_W) // 2,
                          y + (height - CHAR_H) // 2,
                          label, label_color))

    def add(self, component):
        self.children.append(component)
        component.parent = self
        return self

    def contains(self, x, y):
        return (self.x <= x < self.x + self.width
                and self.y <= y < self.y + self.height)

    def draw(self, renderer):
        renderer.fill_rect(self.x, self.y, self.width,
                           self.height, self.bg_color)
        if self.selected:
            renderer.draw_rect(self.x, self.y, self.width, self.height,
                               self.selected_color, 3)
        for child in self.children:
            child.draw(renderer)

    def click(self):
        if self.on_click:
            self.on_click()
