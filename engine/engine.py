from mlx import Mlx
from engine.render import Render


mlx = Mlx()


class Engine:

    def __init__(self,  win_w: int, win_h: int):
        self.win_w = win_w
        self.win_h = win_h
        self.win_h = win_h
        self.mlx_ptr = mlx.mlx_init()
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

    def set_scene(self, scene):
        self.current_scene = scene
        print(f"SCENE DEFINIDA{scene}")

    def onClose(self, _param: object = None):
        mlx.mlx_loop_exit(self.mlx_ptr)

    def onClick(self, button, x, y, _param: object):
        if self.current_scene:
            self.current_scene.handle_click(button, x, y)

    def loop_hook(self, _param: object = None):
        print("Menu Scene")
        if self.current_scene:
            self.current_scene.draw(self.render)
        mlx.mlx_put_image_to_window(self.mlx_ptr, self.win, self.img, 0, 0)

    def run(self):
        mlx.mlx_hook(self.win, 33, 0, self.onClose, None)
        mlx.mlx_mouse_hook(self.win, self.onClick, None)
        mlx.mlx_loop_hook(self.mlx_ptr, self.loop_hook, None)
        mlx.mlx_loop(self.mlx_ptr)
