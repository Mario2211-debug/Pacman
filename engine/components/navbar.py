class Navbar:
    def __init__(self, x, y, width, height, bg_color=0x1A1A1AFF):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.bg_color = bg_color
        self.children = []

    def add(self, component):
        self.children.append(component)
        component.parent = self

    def draw(self, renderer):
        renderer.fill_rect(self.x, self.y, self.width,
                           self.height, self.bg_color)
        for child in self.children:
            child.draw(renderer)

    def handle_click(self, button, x, y):
        if self.x <= x <= self.width and self.y <= y <= self.height:
            print("click no navbar", x, y)
        pass