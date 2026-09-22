# Acceptance test plan

The game opens a window and is driven by the MLX event loop, so it cannot be
tested by a plain unit-test runner. We test it in two ways:

1. **Scripted runs** — a script builds `Game`, `Display` and the four `Ghost`
   objects exactly as `pac-man.py` does, then calls the key handlers and the
   frame function directly. That exercises the real code, including drawing,
   without a human at the keyboard.
2. **Manual play** — for anything visual: sprites, animation, flicker,
   readability of the screens.

## Features covered

| # | Feature | How it is checked | Result |
| --- | --- | --- | --- |
| 1 | Main menu and navigation | Up/Down move the cursor, Enter runs the entry | pass |
| 2 | Highscores screen | Opens, reads the file, shows the top 10 | pass |
| 3 | Instructions screen | Opens and lists controls, rules and cheats | pass |
| 4 | Start a game | Level 1 built, status `RUN`, 3 lives, timer set | pass |
| 5 | Movement in 4 directions | Player changes cell, walls are respected | pass |
| 6 | Eating pacgums | Score increases by `points_per_pacgum` | pass |
| 7 | Super-pacgum and edible ghosts | All four ghosts become `EDIBLE` | pass |
| 8 | Eating a ghost | Score increases by `points_per_ghost` | pass |
| 9 | Cheats `L` `S` `F` `I` | Extra life, speed, freeze, invincibility | pass |
| 10 | Cheat `N` | "Level complete" screen, then next level | pass |
| 11 | Pause and resume | `ESC` → `PAUSED`, `ESC` again → `RUN` | pass |
| 12 | Losing a life | Lives decrease, level restarts | pass |
| 13 | Game over | Last life → game over screen | pass |
| 14 | Victory | Last level completed → victory screen | pass |
| 15 | Name input | Letters, digits and spaces only, 10 characters max | pass |
| 16 | Level seeds | Level 1 reproducible, later levels differ per run | pass |

## Error handling

| # | Case | Expected | Result |
| --- | --- | --- | --- |
| 17 | No argument, or more than one | Usage message, exit, no traceback | pass |
| 18 | Configuration file missing | Message, defaults loaded, game runs | pass |
| 19 | File that is not JSON | Message, defaults loaded, game runs | pass |
| 20 | Out-of-range values (`width`, `height`) | Clamped to defaults, one message per value | pass |
| 21 | Fewer than 10 levels | Padded up to 10, message | pass |
| 22 | Highscore file corrupted | File reset, game keeps running | pass |
| 23 | Highscore file not writable | Error message, no crash | pass |
| 24 | Maze generator failing | Error state, clean exit | by code review |

## Code quality gates

| Gate | Command | Result |
| --- | --- | --- |
| Style | `make lint` (`flake8 .`) | clean |
| Types | `make lint` (`mypy` with the subject's flags) | clean, 11 files |
| Types, strict | `make lint-strict` (`mypy --strict`) | clean, 11 files |
| Docstrings | every module, class and function | 107/107 |

## Bugs found by these tests

| Bug | Where | Status |
| --- | --- | --- |
| `chr(key).isalnum` without parentheses: the test was always true, so punctuation was accepted in player names | `src/game.py` | fixed |
| `raise ("...")` raising a string, which would have masked the real window error | `src/display.py` | fixed |
| `UnboundLocalError` when the highscore file cannot be written | `src/highscores.py` | fixed |
| `find_next_position()` declared `tuple[int]` but returned a pair | `src/ghost.py` | fixed |
| Levels after the first were not random: the maze package reseeds the global RNG | `src/game.py` | fixed |
| `make debug` ran a file named `pdb` instead of the module | `Makefile` | fixed |
| The game did not start on Python below 3.14 | `src/stats.py` | fixed |
| `GameStatus.VICTORY` has the same value as `GAME_OVER`, so it is an alias and the two states cannot be told apart | `src/game_types.py` | open |
| Running out of time ends the game whatever the number of lives left | `src/game.py` | open, by design for now |

**TO COMPLETE** — the manual play sessions: who played, on which machine, and
what was observed.
