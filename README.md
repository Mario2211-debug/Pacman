*This project has been created as part of the 42 curriculum by mafonso, dmikhail.*

# Pac-Man

## Description

A complete, playable Pac-Man written in Python with the MLX graphical library.
The player eats every pacgum of a maze while four ghosts chase them, then moves
on to the next level. The game ships with a main menu, a highscore table, an
instructions screen, a pause menu, and game over / victory screens where the
player can save their score.

Every maze comes from an external *A-Maze-ing* package written by another
group, and all game parameters (number of lives, points, maze sizes, level
time, …) are read from a JSON configuration file given on the command line.

## Instructions

### Requirements

- Python 3.10 or later
- [uv](https://docs.astral.sh/uv/) (the `Makefile` drives everything through it)
- An X11 display (the MLX library opens a window)

The two native dependencies ship with the repository as wheels and are
installed by `make install`: `mlx-2.2-py3-none-any.whl` (graphics) and
`mazegenerator-2.1.0-py3-none-any.whl` (the assigned maze generator).

### Install and play

```bash
make install     # create the virtual environment and install every dependency
make run         # same as: python3 pac-man.py config.json
```

The program takes **exactly one argument**, the configuration file:

```bash
python3 pac-man.py config.json
```

Any other number of arguments prints a usage message and exits.

### Other Makefile rules

| Rule          | What it does                                                     |
| ------------- | ---------------------------------------------------------------- |
| `install`     | `uv sync` plus the two local wheels                               |
| `run`         | Launch the game with `config.json`                                |
| `debug`       | Launch the game under `python -m pdb`                             |
| `clean`       | Remove `__pycache__` and `.mypy_cache`                            |
| `fclean`      | `clean` plus the virtual environment                              |
| `lint`        | `flake8 .` and `mypy .` with the flags required by the subject    |
| `lint-strict` | `flake8 .` and `mypy . --strict`                                  |

### Controls

| Key            | Action                          |
| -------------- | ------------------------------- |
| Arrow keys     | Move / navigate the menus       |
| Enter or Space | Confirm the selected menu entry |
| ESC            | Pause, or go back               |
| Backspace      | Erase a letter of your name     |

Cheat keys, meant for the peer review, are listed on the in-game
**Instructions** screen:

| Key | Cheat                                         |
| --- | --------------------------------------------- |
| `L` | One extra life                                |
| `S` | Increase the player speed (wraps back to base)|
| `F` | Freeze the ghosts                             |
| `I` | Invincibility: ghosts cannot eat the player   |
| `N` | Skip the current level                        |

## Configuration

The configuration file is JSON with comments: every line whose first
non-blank character is `#` or `//` is dropped before parsing. Unknown keys are
ignored. A missing or invalid value never stops the game: it is replaced by
the default below, and the reason is printed to the terminal.

| Key                       | Accepted values                     | Default          |
| ------------------------- | ----------------------------------- | ---------------- |
| `highscore_filename`      | non-empty string ending in `.json`  | `highscore.json` |
| `level`                   | list of at least 10 `{width, height}` objects | 10 mazes of 25×20 |
| `level[].width`           | 10 … 25                             | 25               |
| `level[].height`          | 10 … 20                             | 20               |
| `lives`                   | ≥ 1                                 | 3                |
| `pacgum`                  | ≥ 1 (pacgums placed per maze)       | 42               |
| `points_per_pacgum`       | ≥ 1                                 | 10               |
| `points_per_super_pacgum` | ≥ 1                                 | 250              |
| `points_per_ghost`        | ≥ 1                                 | 200              |
| `seed`                    | ≥ 0 (seed of the first maze)        | 42               |
| `level_max_time`          | ≥ 10 (seconds per level)            | 90               |

A level whose `width` and `height` are both missing is dropped. If fewer than
ten levels are left, the list is padded with default mazes, because the
subject requires at least ten levels.

Example:

```json
{
    // the file the scores are stored in
    "highscore_filename": "highscore.json",
    "level": [
        {"width": 25, "height": 20},
        {"width": 15, "height": 15}
    ],
    "lives": 3,
    # number of pacgums per maze
    "pacgum": 150,
    "points_per_pacgum": 10,
    "points_per_super_pacgum": 100,
    "points_per_ghost": 333,
    "seed": 1,
    "level_max_time": 300
}
```

## Highscore

Scores live in a plain JSON file, named by `highscore_filename`, holding a
list of `{"name": ..., "score": ...}` records. We chose a JSON file next to
the project because it is the same format as the configuration, it is readable
and editable by a human during the review, and it needs no database or extra
dependency.

How it behaves:

- The file is read when the highscores screen is opened and written when a
  player saves a score, so a crash can never lose more than the current run.
- Records without a name or without a score are dropped while reading.
- If the file is missing, empty or not valid JSON, the game starts a fresh
  empty table instead of failing; a file that cannot be written only prints an
  error message.
- The highscores screen shows the **top 10**, sorted by score, highest first.
- A name is at most 10 characters, letters, digits and single spaces. The
  in-game font only has lowercase glyphs, so names are typed in lowercase.
- The **Clear** entry of the highscores screen empties the file.

## Maze Generation

Mazes are generated by the *A-Maze-ing* package assigned to us, installed
as-is from `mazegenerator-2.1.0-py3-none-any.whl`. We never modified it and
never wrote a generator of our own; our loader adapts to its interface:

```python
mazegen = MazeGenerator((width, height), False, (0, 0),
                        (width - 1, height - 1), seed)
```

- `PERFECT` is always `False`, so the maze has loops and is playable as a
  Pac-Man board.
- The entry cell is the top-left corner and the exit cell the bottom-right one.
- **Level 1 uses the `seed` from the configuration file**, so the first maze is
  always the same. **Every later level uses a random seed.** That seed is drawn
  with `random.SystemRandom()` on purpose: the package reseeds Python's global
  random generator, so a plain `random.randrange()` would produce the same
  "random" mazes on every run.
- If the generator raises, or returns an empty maze, the game enters its error
  state, prints a message and exits cleanly — no traceback.

Each maze cell is a bitmask of its walls (1 top, 2 right, 4 bottom, 8 left);
the value 15 marks a full block, which the player and the ghosts cannot enter.

## Implementation

- **Game loop.** MLX calls `Game.playing()` on every iteration of its loop.
  The elapsed time is accumulated and consumed in fixed steps of 1/60 s, so
  movement speed does not depend on the machine. A one-second counter drives
  the level timer and the edible countdown.
- **Drawing.** The static part of a level (walls, side panels, HUD labels) is
  composed once into an off-screen bitmap named `maze_screen`. Each frame
  blits that bitmap, then erases the previous sprite positions with their
  black masks and draws the sprites at their new position. Text is drawn with
  one PNG per character, so the same routine writes menus, HUD and scores.
- **Movement.** The player and the ghosts move between maze cells; the pixel
  position is interpolated between the current and the next cell, and the next
  cell is chosen when they line up. The player keeps a "next direction" so a
  key pressed slightly early is still honoured at the next junction.
- **Ghosts.** Each ghost searches its path with a breadth-first search over
  the maze cells, avoiding the cells the other ghosts are heading for. The
  target depends on the behavior: the player (red), a random corner (blue), a
  random cell (orange), a cell far from the player when scared, or their own
  corner when returning home. A super-pacgum makes the ghosts edible for 10
  seconds; an eaten ghost returns to its corner and comes back to life 5
  seconds later.
- **Error handling.** The configuration, the highscore file and the maze
  generator are all guarded: invalid input is replaced by a default or reported
  with a message, and the game never shows a Python traceback.
- **Typing and style.** The whole code base passes `flake8`, `mypy` with the
  flags required by the subject, and `mypy --strict`.

## General Software Architecture

```
pac-man.py            entry point: reads the config, builds Display, Game and
                      the four Ghosts, then hands control to the MLX loop
└── src/
    ├── config.py     Config (pydantic model) + open_config_file()
    ├── game.py       Game: the state machine of every screen
    ├── display.py    Display, ImgData, ImgType: window, images, drawing
    ├── stats.py      Stats and Stats.Window: score, lives, level, time + HUD
    ├── pacman.py     PacMan: the player
    ├── ghost.py      Ghost: one ghost, its behavior and its path finding
    ├── pacgum.py     pacgums_generate(): pacgum placement
    ├── highscores.py read, append and reset the highscore file
    └── game_types.py the shared enums (Direction, GameStatus, …)
```

`Game` is the hub: it owns the `Config`, the `Stats`, the `PacMan` and the
four `Ghost` objects, and it is the only class that talks to `Display`. Each
screen is a method of `Game` that draws itself and registers the key handler it
needs, which is how the game switches between menu, gameplay, pause and the end
screens. `PacMan`, `Ghost` and `Stats` keep a reference back to their `Game` to
read the maze and to report what they did; `Display` knows nothing about the
rules and only draws what it is told to draw.

## Project Management

How we organised the work, the timeline, the division of tasks, the risks we
met and the acceptance tests are documented in
[`project-management/`](project-management/).

## Resources

- [MLX (MiniLibX) documentation](https://harm-smits.github.io/42docs/libs/minilibx)
  — window, images, hooks and event loop.
- X11 keysym values, used for the raw key codes returned by the MLX key hooks.
- [PEP 8](https://peps.python.org/pep-0008/),
  [PEP 257](https://peps.python.org/pep-0257/) and
  [PEP 484](https://peps.python.org/pep-0484/) — style, docstrings and type
  hints.
- [pydantic](https://docs.pydantic.dev/) — validation of the configuration
  file, including the fallback to defaults on invalid values.
- [mypy](https://mypy.readthedocs.io/) and
  [flake8](https://flake8.pycqa.org/) documentation.
- [uv](https://docs.astral.sh/uv/) — environment and dependency management.
- Breadth-first search for the ghost path finding, from the classic
  shortest-path-in-a-grid formulation.

### Use of AI

AI (Claude Code) was used as a reviewer and as an assistant for repetitive
work, never to write the game logic:

- **Static typing pass.** Running `mypy` with the subject's flags and going
  through the errors it reported: missing annotations, a function that
  declared `tuple[int]` while returning a pair, attributes inferred as `None`.
- **Bug hunting.** It found `chr(key).isalnum` used without the parentheses in
  the name input (the test was therefore always true), a `raise` of a string
  instead of an exception, and a crash in the highscore writer when the
  destination could not be written (`UnboundLocalError` in a `finally` block).
  We reviewed and applied each fix ourselves.
- **Test scripts.** Scripts that drive the game without a human, to check the
  menus, the movement, the cheats, the pause, the level change and the end
  screens after a refactor.
- **Docstrings** for the existing functions and classes, and a first draft of
  this README, both reviewed and corrected by us.

Everything AI produced was read, tested and, where needed, rewritten before
being committed. The design of the game, the architecture and the gameplay
decisions are ours.
