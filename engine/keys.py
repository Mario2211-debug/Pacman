"""X11 keysyms delivered by the MLX key hooks."""

ESCAPE = 65307
ENTER = 65293
KP_ENTER = 65421
BACKSPACE = 65288
SPACE = 32
LEFT = 65361
UP = 65362
RIGHT = 65363
DOWN = 65364
W = 119
A = 97
S = 115
D = 100
P = 112
K = 107
N = 110
ONE = 49
TWO = 50
THREE = 51

CONFIRM = (ENTER, KP_ENTER, SPACE)
MENU_UP = (UP, W)
MENU_DOWN = (DOWN, S)
PAUSE = (ESCAPE, P)


def to_char(key: int) -> str:
    """Letter or digit typed (uppercase), or '' for any other key."""
    if 32 < key < 127 and chr(key).isalnum():
        return chr(key).upper()
    return ""
