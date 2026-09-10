
class Button:
    def __init__(self, x, y, on_click: None, bg_color=0x1A1A1AFF):
        self.x: int = x
        self.y: int = y
        self.width: int = 64
        self.heigth: int = 24
        self.children: list = []
        self.on_click = on_click
        self.bg_color: int = bg_color

    def add(self, component):
        self.children.append(component)
        component.parent = self
        return self

    def draw(self, renderer):
        renderer.fill_rect(self.x, self.y, self.width,
                           self.heigth, self.bg_color)
        for child in self.children:
            child.draw(renderer)

    def click(self):
        print(f"button {self.text} pressed")
