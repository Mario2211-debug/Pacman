# Specification checklist

Every requirement of the subject, with where it is implemented and its current
status. Keep this file up to date: it is the list we walk through before the
defense.

Legend: ✅ done · ⚠️ done, with a decision or a limit worth knowing · ❌ missing

---

## III.1 General rules

| # | Requirement | Where | Status |
| --- | --- | --- | --- |
| 1 | Written in Python 3.10 or later | `pyproject.toml` | ✅ |
| 2 | Passes `flake8` | `make lint` | ✅ |
| 3 | Exceptions handled, no crash during the review | config, highscores and maze generator are all guarded | ✅ |
| 4 | Resources released, context managers for files | `src/config.py`, `src/highscores.py` | ✅ |
| 5 | Type hints everywhere, `mypy` clean | `make lint` and `make lint-strict` | ✅ |
| 6 | Docstrings (PEP 257) on functions and classes | all modules | ✅ 107/107 |

## III.2 Makefile

| # | Rule | Status |
| --- | --- | --- |
| 7 | `install` | ✅ |
| 8 | `run` | ✅ |
| 9 | `debug` (under `pdb`) | ✅ |
| 10 | `clean` | ✅ |
| 11 | `lint` with the exact flags of the subject | ✅ |
| 12 | `lint-strict` (optional) | ✅ |

## III.3 Additional guidelines

| # | Requirement | Status |
| --- | --- | --- |
| 13 | `.gitignore` for Python artifacts | ✅ |
| 14 | Test programs (not submitted, not graded) | ⚠️ scripted runs exist outside the repository, see `project-management/test-plan.md` |
| 15 | Virtual environment | ✅ `uv`, driven by the Makefile |

## V.1 Usage

| # | Requirement | Where | Status |
| --- | --- | --- | --- |
| 16 | `python3 pac-man.py config.json` | `pac-man.py` | ✅ |
| 17 | Exactly one argument | `pac-man.py` | ✅ usage message, exit 1 |
| 18 | Any error handled cleanly, never a traceback | `src/config.py` | ✅ tested with a missing file, a non-JSON file and bad values |

## V.2 / V.3 Configuration file

| # | Requirement | Where | Status |
| --- | --- | --- | --- |
| 19 | JSON with `#` comments (and `//`) | `open_config_file()` | ✅ |
| 20 | Keys documented in the README, robust defaults | `README.md`, `CONFIG_DEFAULTS` | ✅ |
| 21 | Invalid values clamped to a default, with a message | `Config.check_level_list()` | ✅ |
| 22 | Unknown keys ignored | pydantic model | ✅ |
| 23 | Works with a configuration changed during the defense | — | ⚠️ test a few odd configurations before the defense |

## V.4 Maze generator

| # | Requirement | Where | Status |
| --- | --- | --- | --- |
| 24 | Assigned package used as-is, never modified | `mazegenerator-2.1.0-py3-none-any.whl` | ✅ installed as a wheel |
| 25 | Our loader adapts to their interface | `Game.create_level()` | ✅ |
| 26 | `PERFECT` set to `False` | `Game.create_level()` | ✅ |
| 27 | Generator failure handled cleanly | `try/except` → `GameStatus.ERROR` | ✅ |

## V.5 Highscore system

| # | Requirement | Where | Status |
| --- | --- | --- | --- |
| 28 | Persistent | JSON file named by `highscore_filename` | ✅ |
| 29 | Robust to file errors | `src/highscores.py` | ✅ tested: corrupted file, unwritable file |
| 30 | Names: 10 characters max, alphanumeric and spaces | `Game.score_menu_handle_key_press()` | ⚠️ only lowercase, the font has no uppercase glyphs |
| 31 | Scores: non-negative integers | score only ever increases | ✅ |
| 32 | Top 10 kept | `Game.highscores()` | ⚠️ the top 10 is what is displayed; the file keeps every record |
| 33 | Loaded at game start, saved at game end | `Game.highscores()`, `save_to_highscores_file()` | ⚠️ loaded when the highscores screen opens, not at startup |
| 34 | Name asked at the end of a game, win or lose | victory / game over / time out screens | ✅ |
| 35 | Displayed from the main menu | `Game.highscores()` | ✅ |

## VI.1 Level structure

| # | Requirement | Where | Status |
| --- | --- | --- | --- |
| 36 | Maze from the A-Maze-ing package | `Game.create_level()` | ✅ |
| 37 | First level on a fixed seed | `config.seed` | ✅ |
| 38 | Later levels randomly generated | `SystemRandom().randrange()` | ✅ the package reseeds the global RNG, hence `SystemRandom` |
| 39 | Pacgums in most corridors | `pacgums_generate()` | ✅ count from `pacgum` |
| 40 | Super-pacgums in the 4 corners | `pacgums_generate()` | ✅ |
| 41 | 4 ghosts, one per corner | `Game.create_level()` | ✅ |
| 42 | Player starts in the middle | `Game.create_level()` | ✅ |

## VI.2 Player

| # | Requirement | Where | Status |
| --- | --- | --- | --- |
| 43 | Moves through corridors only | `PacMan.move()` | ✅ |
| 44 | Four directions, arrow keys or WASD | `Game.game_handle_key_press()` | ⚠️ arrow keys only; the subject allows either |
| 45 | Starts with 3 lives | `config.lives` | ✅ |
| 46 | Loses a life when touched by a ghost | `Game.playing()` → `Game.death()` | ✅ |
| 47 | Respawns in the middle after losing a life | `PacMan.death()` | ✅ |
| 48 | Game over when all lives are lost | `Game.death()` | ✅ |
| 49 | Wins the level when every pacgum is eaten | `Game.check_pacgums()` | ✅ |
| 50 | Wins the game when every level is done | `Game.next_level()` → `Game.victory()` | ✅ |
| 51 | Pacgum, super-pacgum and ghost give points | `Game.eat_pacgum()`, `Game.eat_ghost()` | ✅ |

## VI.3 Ghosts

| # | Requirement | Where | Status |
| --- | --- | --- | --- |
| 52 | Move autonomously through corridors | `Ghost.move()` | ✅ BFS path finding |
| 53 | Chase the player when not edible | `GhostBehavior.PLAYER` / `CORNERS` / `RANDOM` | ✅ |
| 54 | Run away when edible | `GhostBehavior.SCARED` | ✅ |
| 55 | Respawn in their corner after being eaten | `Ghost.death()` / `Ghost.reborn()` | ✅ after 5 s |

## VI.4 Pacgums and super-pacgums

| # | Requirement | Where | Status |
| --- | --- | --- | --- |
| 56 | Small dots in the corridors, large ones in the corners | `pacgums_generate()`, `Display.show_pacgum()` | ✅ |
| 57 | A super-pacgum makes the ghosts edible for a while | `Game.edible_mode()` | ✅ 10 s |

## VI.5 Cheat mode

| # | Requirement | Key | Status |
| --- | --- | --- | --- |
| 58 | Invincibility | `I` | ✅ |
| 59 | Level skip | `N` | ✅ |
| 60 | Ghost freeze | `F` | ✅ |
| 61 | Extra lives | `L` | ✅ |
| 62 | Increased speed | `S` | ✅ |
| 63 | Listed where the reviewer can find them | Instructions screen | ✅ |

## VI.6 Scoring

| # | Requirement | Status |
| --- | --- | --- |
| 64 | Points for pacgum, super-pacgum and edible ghost | ✅ |
| 65 | The score never decreases | ✅ |

## VI.7 Game progression

| # | Requirement | Where | Status |
| --- | --- | --- | --- |
| 66 | At least 10 levels | `Config.check_level_list()` pads up to 10 | ✅ |
| 67 | Time limit per level | `config.level_max_time` | ✅ |
| 68 | Something happens when the time runs out | `Game.time_out()` | ⚠️ the game ends whatever the lives left — our choice, the subject allows it, but see `TODO.md` |
| 69 | Completing a level moves to the next one | `Game.next_level()` | ✅ |
| 70 | Score and lives kept between levels | `Stats` | ✅ |
| 71 | The game ends on the last level or on the last life | `Game.victory()` / `Game.game_over()` | ✅ |
| 72 | Pause and resume | `Game.pause()` / `Game.resume()` | ✅ |
| 73 | Final score shown, name asked | end screens | ✅ |
| 74 | Back to the main menu afterwards | `Game.menu()` | ✅ |

## VI.8 User interface

| # | Requirement | Status |
| --- | --- | --- |
| 75 | Main menu: Start, Highscores, Instructions, Exit | ✅ |
| 76 | HUD: score, lives, level, remaining time | ✅ |
| 77 | Pause menu: Resume, Main menu | ✅ |
| 78 | Game over screen: final score + name entry | ✅ |
| 79 | Victory screen: final score, congratulations, name entry | ✅ |

## VII Packaging

| # | Requirement | Where | Status |
| --- | --- | --- | --- |
| 80 | Installable, launchable build | `make package` → `dist/pac-man/` | ✅ built and run outside the project |
| 81 | Published on a public platform, unlisted | itch.io | ❌ **not done** |
| 82 | Instructions inside the package | `config.json` next to the binary, in-game Instructions screen | ⚠️ add the controls to the itch.io page |
| 83 | Packaging spec at the root of the repository | `pac-man.spec` | ✅ |
| 84 | The package can be regenerated during the review | `make package` | ✅ |

## VIII Project management

| # | Requirement | Where | Status |
| --- | --- | --- | --- |
| 85 | Dedicated directory with evidence | `project-management/` | ✅ |
| 86 | Timeline and actual progress | `project-management/timeline.md` | ⚠️ planned dates still missing |
| 87 | Team organisation, decisions | `project-management/team-organisation.md` | ⚠️ how decisions were made still missing |
| 88 | Risk analysis | `project-management/risk-analysis.md` | ✅ |
| 89 | Acceptance test plan | `project-management/test-plan.md` | ⚠️ manual sessions still missing |

## IX README

| # | Required section | Status |
| --- | --- | --- |
| 90 | First line in italics with the logins | ✅ |
| 91 | Description | ✅ |
| 92 | Instructions | ✅ |
| 93 | Resources, including how AI was used | ⚠️ written, to be read and owned by both of us |
| 94 | Configuration | ✅ |
| 95 | Highscore | ✅ |
| 96 | Maze Generation | ✅ |
| 97 | Implementation | ✅ |
| 98 | General Software Architecture | ✅ |
| 99 | Project Management | ✅ |
| 100 | Written in English | ✅ |

## X Defense

| # | Requirement | Status |
| --- | --- | --- |
| 101 | Be ready for a small change asked during the evaluation | ⚠️ both of us must be able to explain every part |
