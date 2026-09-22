# Timeline

All figures below are taken from the git history of this repository
(`git log --all`), not from memory: 186 commits between 2026-08-18 and
2026-09-22.

## Phases

| Phase | Dates | What was done |
| --- | --- | --- |
| Setup | 2026-08-18 | Repository created, project skeleton |
| Core game | 2026-09-08 → 2026-09-13 | MLX window and drawing, maze rendering, player and ghost movement, pacgums, configuration file |
| Screens and rules | 2026-09-14 → 2026-09-18 | Menus, HUD, pause, game over and victory screens, highscores, cheat mode, edible ghosts |
| Polish | 2026-09-19 → 2026-09-21 | Maze centring, invisible player, name input, random ghosts on the menu, flake8 clean-up |
| Quality | 2026-09-22 | `mypy` clean (standard and `--strict`), docstrings, packaging and documentation |

## Actual activity per day

```
2026-08-18   1     repository created
2026-09-08  24     ███████████
2026-09-09  18     ████████
2026-09-10  14     ██████
2026-09-11   7     ███
2026-09-12   7     ███
2026-09-13   8     ███
2026-09-14  32     ███████████████
2026-09-15   7     ███
2026-09-16   4     ██
2026-09-17  11     █████
2026-09-18   9     ████
2026-09-19  18     ████████
2026-09-20   8     ███
2026-09-21  11     █████
2026-09-22   7     ███
```

Two peaks stand out: **09-08** (start of the real implementation, both of us
working at the same time) and **09-14** (the screens and the highscore system
landing together).

## Progress against the plan

- The playable core was ready well before the deadline, which left the last
  days for quality work (`flake8`, `mypy --strict`, docstrings) instead of
  rushing features.
- Two graphical architectures were explored in parallel (see
  [`team-organisation.md`](team-organisation.md)); only one was kept, which
  cost time but produced the simpler code base.
- Still open at the time of writing: packaging for a public platform
  (see [`../packaging/`](../packaging)).

**TO COMPLETE** — the planned dates you fixed at the start of the project, so
that the table above can be read as *planned vs actual*.
