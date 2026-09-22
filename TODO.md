# TODO

What is left before the defense. The numbers in brackets point to the line of
[`SPECS.md`](SPECS.md) the item comes from.

## Blocking — a deliverable is missing

- [ ] **Publish the build on itch.io** as a free, unlisted game. [81]
      The build itself is done and tested (`make package`); only the upload is
      left. Steps in [`packaging/README.md`](packaging/README.md).
- [ ] Put the controls, the cheat keys and a word about `config.json` in the
      itch.io page description. [82]
- [ ] Write the page URL into `packaging/README.md`, and say who owns the
      account, so the build can be regenerated during the review. [81]

## Documents to finish

- [ ] `project-management/timeline.md` — the dates planned at the start, so the
      table reads as *planned vs actual*. [86]
- [ ] `project-management/team-organisation.md` — how decisions were taken day
      to day and how disagreements were settled. [87]
- [ ] `project-management/test-plan.md` — the manual play sessions: who, on
      which machine, what was observed. [89]
- [ ] `README.md`, section **Use of AI** — read it and make it ours. The
      subject is explicit: we have to be able to explain and defend anything AI
      touched. [93]

## Decisions to take, then code

- [ ] **`GameStatus.VICTORY` is an alias of `GAME_OVER`** (both are `3`, so
      Python makes them the same member). Nothing compares against them today,
      so the game behaves correctly, but the two states cannot be told apart.
      Giving `VICTORY` the value `5` is a one-line fix.
- [ ] **Running out of time ends the game**, whatever the number of lives left
      (`Game.time_out()`). The subject leaves the choice to us, so this is
      valid, but a player expects to lose one life and restart the level.
      Decide, and write the choice down in the README. [68]
- [ ] Keep only the top 10 in the highscore file, instead of keeping every
      record and sorting at display time. [32]
- [ ] Load the highscores once at startup instead of when the screen is
      opened, which is what the subject describes. [33]

## Nice to have

- [ ] Accept WASD as well as the arrow keys. [44]
- [ ] Uppercase glyphs for the letters, so names are not limited to
      lowercase. [30]
- [ ] Commit the scripted test runs, so a reviewer can replay them. [14]
- [ ] Remove the leftover `engine/`, `models/`, `utils/` and `test/`
      directories: the tracked files are gone, only orphan `__pycache__`
      directories are left.

## Before the defense

- [ ] Try a few odd configuration files: values out of range, missing keys,
      fewer than ten levels, an unreadable file. The configuration **will be
      changed during the defense**. [23]
- [ ] Reinstall the assigned A-Maze-ing package from its own wheel and check
      the game still runs, since the reviewer will do exactly that. [24]
- [ ] `make fclean && make install && make run` from a clean clone, on the
      machine used for the defense.
- [ ] Run through the game once with each cheat key, so the demonstration is
      fluid. [58-62]
- [ ] Both of us must be able to explain every part of the code, including the
      parts written by the other. [101]
