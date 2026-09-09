from mlx import Mlx


mlx = Mlx()
mlx_ptr = mlx.mlx_init()


win_w = 800
win_h = 600
win = mlx.mlx_new_window(mlx_ptr, win_w, win_h, "Packman")

img = mlx.mlx_new_image(mlx_ptr, win_w, win_h)
data, bpp, size_line, img_format = mlx.mlx_get_data_addr(img)
order = "little" if img_format == 0 else "big"


def pack(color: int, order="big"):
    return color.to_bytes(4, order)


def fill_ret(data, size_line, order, win_h, win_w, px, py, w, h, colour):
    packed = pack(colour, order)
    for yy in range(py, py + h):
        base = yy * size_line
        for xx in range(px, px + w):
            off = base + xx * 4
            data[off:off + 4] = packed


fill_ret(data, size_line, order, win_w, win_h, 100, 100, 54, 24, 0xFF0000FF)


def onClose(_param: object):
    mlx.mlx_loop_exit(mlx_ptr)


def onClick(button, x, y, _param: object):
    if button == 1:
        print("Botão esquerdo do mouse pressionado em:", x, y)
    elif button == 3:
        print("Botão direito do mouse pressionado em:", x, y)


print(data)
mlx.mlx_put_image_to_window(mlx_ptr, win, img, 0, 0)
mlx.mlx_hook(win, 33, 0, onClose, None)
mlx.mlx_mouse_hook(win, onClick, None)
mlx.mlx_loop(mlx_ptr)
