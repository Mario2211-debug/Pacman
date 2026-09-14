from engine import keys
from .buttons import Button


class MenuList:

    def __init__(self, x, y, width, options, button_height=40, spacing=12,
                 bg_color=0x000080FF, label_color=0xFFFFFFFF):
        self.buttons: list[Button] = []
        for i, (label, on_click) in enumerate(options):
            self.buttons.append(Button(x, y + i * (button_height + spacing),
                                       on_click=on_click,
                                       bg_color=bg_color,
                                       width=width,
                                       height=button_height,
                                       label=label,
                                       label_color=label_color))
        self.index = 0
        self.select(0)

    def select(self, index):
        if not self.buttons:
            return
        self.buttons[self.index].selected = False
        self.index = index % len(self.buttons)
        self.buttons[self.index].selected = True

    def draw(self, renderer):
        for button in self.buttons:
            button.draw(renderer)

    def handle_key(self, key):
        if not self.buttons:
            return
        if key in keys.MENU_UP:
            self.select(self.index - 1)
        elif key in keys.MENU_DOWN:
            self.select(self.index + 1)
        elif key in keys.CONFIRM:
            self.buttons[self.index].click()

    def handle_click(self, button, x, y):
        if button != 1:
            return
        for i, btn in enumerate(self.buttons):
            if btn.contains(x, y):
                self.select(i)
                btn.click()
                return
