class Ghost:
    def __init__(self, image=None, x=0, y=0):
        self.image = image
        self.x = x
        self.y = y
        self.next_x = x
        self.next_y = y
        self.x_px = x * 10
        self.y_px = y * 10
        self.edible = False
        self.freeze = False