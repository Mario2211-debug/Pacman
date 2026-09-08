from mlx import Mlx # type ignore


mlx = Mlx()
mlx_ptr = mlx.mlx_init()
_, screen_w, screen_h = mlx.mlx_get_screen_size(mlx_ptr)


if __name__ == "__main__":
    print(mlx)
