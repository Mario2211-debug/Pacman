import time

from mlx import Mlx
from engine.render import Render


mlx = Mlx()

KEY_PRESS = 2
KEY_PRESS_MASK = 1
DESTROY_NOTIFY = 33
BACKGROUND = 0x000000FF
MAX_DT = 0.1


class Engine:

    def __init__(self, win_w: int, win_h: int, config, highscores):
        self.win_w = win_w
        self.win_h = win_h
        self.config = config
        self.highscores = highscores
        self.mlx_ptr = mlx.mlx_init()
        if not self.mlx_ptr:
            raise RuntimeError("mlx_init failed (no display?)")
        # screen_size = mlx.mlx_get_screen_size(self.mlx_ptr)
        # self.win_w = screen_size[1]
        # self.win_h = screen_size[2]
        self.win = mlx.mlx_new_window(self.mlx_ptr,
                                      self.win_w, self.win_h, "Packman")
        self.img = mlx.mlx_new_image(self.mlx_ptr, self.win_w, self.win_h)
        self.data, self.bpp, self.size_line, self.img_format = (
            mlx.mlx_get_data_addr(self.img))
        self.render = Render(self.mlx_ptr, mlx, self.win,
                             self.win_w, self.win_h,
                             self.data, self.size_line,
                             self.img_format)
        self.current_scene = None
        self.last_time = time.perf_counter()

    def set_scene(self, scene):
        self.current_scene = scene

    def onClose(self, _param: object = None):
        mlx.mlx_loop_exit(self.mlx_ptr)

    def onClick(self, button, x, y, _param: object):
        if self.current_scene:
            self.current_scene.handle_click(button, x, y)

    def onKey(self, key, _param: object = None):
        if self.current_scene:
            self.current_scene.handle_key(key)

    def loop_hook(self, _param: object = None):
        now = time.perf_counter()
        dt = min(now - self.last_time, MAX_DT)
        self.last_time = now
        self.render.clear(BACKGROUND)
        if self.current_scene:
            self.current_scene.update(dt)
        if self.current_scene:
            self.current_scene.draw(self.render)
        mlx.mlx_put_image_to_window(self.mlx_ptr, self.win, self.img, 0, 0)
        self.render.flush_text()

    def run(self):
        mlx.mlx_hook(self.win, DESTROY_NOTIFY, 0, self.onClose, None)
        mlx.mlx_hook(self.win, KEY_PRESS, KEY_PRESS_MASK, self.onKey, None)
        mlx.mlx_mouse_hook(self.win, self.onClick, None)
        mlx.mlx_loop_hook(self.mlx_ptr, self.loop_hook, None)
        self.last_time = time.perf_counter()
        mlx.mlx_loop(self.mlx_ptr)
