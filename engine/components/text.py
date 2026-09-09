from utils import colors


class Text:
    def __init__(self,  x, y, text: str, on_click: None, bg_color=0x1A1A1AFF):
        self.x: int = x
        self.y: int = y
        self.text = text
        self.width: int = 64
        self.heigth: int = 24
        self.children: list = []
        self.on_click = on_click
        self.bg_color: int = bg_color

    def draw(self, renderer):
        renderer.draw_text(self.text, self.x, self.y, self.bg_color)

        for child in self.children:
            child.draw(renderer)

    def click(self):
        print(f"button {self.text} pressed")
