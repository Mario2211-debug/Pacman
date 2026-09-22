# Risk analysis

Every risk below actually happened during the project; the mitigation column
says what was done about it.

## 1. The game only started on Python 3.14

**What happened.** `src/stats.py` imports `Game` under `if TYPE_CHECKING:` to
break the import cycle with `src/game.py`, then used it as a plain annotation
on `Stats.__init__`. Up to Python 3.13 a parameter annotation is evaluated when
the `def` is read, so the game crashed at import with
`NameError: name 'Game' is not defined`. It ran on the machine with Python
3.14, where PEP 649 made annotations lazy, and nowhere else.

**Impact.** High: the project declares `requires-python = ">=3.10"` and would
have failed to start on an evaluation machine with any earlier version.

**Mitigation.** `from __future__ import annotations` at the top of
`src/stats.py`, which gives the 3.14 behaviour on every version from 3.7.
Lesson: test on the lowest version the project claims to support, not only on
the developer's own interpreter.

## 2. Depending on another group's package

**What happened.** The maze generator is assigned and must be used as-is; the
reviewer will reinstall their copy. It is also less predictable than our own
code: it reseeds Python's global random generator, which silently made our
"random" levels identical on every run.

**Impact.** Medium: a working game can break when the package is replaced, and
subtle behaviour like the reseeding is easy to miss.

**Mitigation.** The package is installed from its wheel and never edited; the
call is isolated in `Game.create_level()`, wrapped in `try/except` with a clean
error state; level seeds are drawn with `random.SystemRandom()` so the global
generator cannot influence them.

## 3. Both of us doing the same work at the same time

**What happened.** On 2026-09-22 the `mypy` clean-up was done twice, eight
minutes apart, on two branches, by two different routes: `src/__init__.py`
versus `explicit_package_bases`, `game_types.py` versus `pac_types.py`, the
generator as a wheel versus as a directory. Merging the two produced ten
conflicts, one of them a rename/rename.

**Impact.** Medium: a full day of work on one side was thrown away.

**Mitigation.** We kept one of the two versions whole instead of merging line
by line, and rebuilt the remaining fixes on top of it. Lesson: announce the
file or the task being taken before starting it, especially for cross-cutting
work like a typing or style pass.

## 4. Crashes during the review

**What happened.** The subject states that an unhandled exception during the
review makes the project non-functional. Two real cases were found: a `raise`
of a string instead of an exception, and an `UnboundLocalError` in the
highscore writer when the file could not be written.

**Impact.** High, since it is an explicit failure condition.

**Mitigation.** Every external input is guarded (configuration file, highscore
file, maze generator); the error paths are tested on purpose, including a
read-only directory — see [`test-plan.md`](test-plan.md).

## 5. Graphics library and environment

**What happened.** MLX needs an X11 display; the game cannot run headless, and
the assets are loaded from relative paths, so the working directory matters.

**Impact.** Medium for packaging: a bundled build must ship the `img/`
directory and start in the right directory.

**Mitigation.** `make run` always launches from the project root; packaging is
documented in [`../packaging/`](../packaging).

**TO COMPLETE** — any risk you identified before starting that never
materialised, which is also worth listing.
