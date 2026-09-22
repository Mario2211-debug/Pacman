# Team organisation

Two people: **mafonso** (Mario Afonso) and **dmikhail** (Dmitrii Mikhailov)..

## Commits

| Author | Commits |
| --- | --- |
| Dmitrii Mikhailov | 145 |
| Mario Afonso / Mário Afonso / Mario2211-debug | 41 |

## Who worked where

Derived from `git log --name-only` per author.

| Author | Main files |
| --- | --- |
| dmikhail | `pac-man.py`, `src/game.py`, `src/ghost.py`, `src/pacman.py`, `src/display.py`, `src/config.py`, `src/stats.py`, `config.json` |
| mafonso | `engine/` (the alternative graphical architecture), `pac-man.py`, project configuration, static typing pass |

The split was mostly by area rather than by task: game rules, rendering and
the maze pipeline on one side; the scene/component engine, project setup and
the code-quality passes on the other.

## Branching model

- `master` — integration branch, always the version to review.
- `dmikhail` — Dmitrii's working branch, merged into `master` regularly
  (13 merge commits between 09-19 and 09-21).
- `mafonso` / `mafons` — Mario's working branches.
- `integra-mafonso` — branch created to merge the two architectures.

## Decisions taken during the project

1. **Two graphical architectures were written in parallel.** One is a
   scene/component engine (`engine/`, scenes and reusable widgets), the other
   draws each screen directly from `Game` (`src/`). We kept the second: it
   produced fewer indirections for a game this size, and it was the one where
   gameplay was already finished. The `engine/` code was dropped from the
   final version.
2. **The maze generator is used as a wheel**, not as a copied source
   directory, so the package really is "as-is" and can be swapped for the
   reviewer's copy without touching our code.
3. **The static typing pass was done twice, in parallel, by both of us** —
   see [`risk-analysis.md`](risk-analysis.md), risk 3. We kept Dmitrii's
   version and rebased the other work on top of it.

**TO COMPLETE** — how decisions were made day to day (in person, on Discord,
…) and how disagreements were settled.
