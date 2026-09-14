
class Text:
    def __init__(self, x, y, text: str, color=0xFFFFFFFF, on_click=None):
        self.x: int = x
        self.y: int = y
        self.text = text
        self.width: int = 64
        self.heigth: int = 24
        self.children: list = []
        self.on_click = on_click
        self.color: int = color

    def draw(self, renderer):
        renderer.draw_text(self.text, self.x, self.y, self.color)

        for child in self.children:
            child.draw(renderer)

    def click(self):
        print(f"button {self.text} pressed")
