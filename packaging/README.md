# Packaging

The game is packaged with [PyInstaller](https://pyinstaller.org/) into a
self-contained folder that runs without Python, without `uv` and without the
project sources.

| File | Role |
| --- | --- |
| [`../pac-man.spec`](../pac-man.spec) | PyInstaller spec, at the root of the repository as the subject requires |
| [`runtime_chdir.py`](runtime_chdir.py) | Runtime hook: makes the bundle start in its own directory, so the relative `img/...` paths resolve |

## Build

```bash
make package
```

which is:

```bash
uv run --with pyinstaller pyinstaller pac-man.spec --noconfirm
```

The result is `dist/pac-man/`, about 29 MB, containing the `pac-man`
executable and an `_internal/` directory with the interpreter, `libmlx.so`,
the maze generator, every sprite and a default `config.json`.

### What the spec takes care of

- `img/` is bundled whole; the runtime hook changes the working directory to
  the bundle so the game finds it wherever it is launched from.
- `libmlx.so` is collected from the `mlx` package and kept in an `mlx/`
  subdirectory, because the library loads it from next to its own `__init__.py`.
- `mazegenerator` is declared as a hidden import: it is only reached through
  `from mazegenerator import MazeGenerator`, which PyInstaller does not follow
  on its own.

### Verified

Built on Linux, then run from `/tmp`, outside the project and with no virtual
environment active:

- `./pac-man config.json` — the game starts and plays.
- `./pac-man` — prints the usage message and exits with status 1.
- `./pac-man missing.json` — falls back to the default configuration and runs.

The build is Linux-only: PyInstaller does not cross-compile, and `libmlx.so`
is a Linux library. A Windows or macOS build would need that platform and an
MLX port for it.

## Publish on itch.io

The build has not been uploaded yet — it needs the team's own account.

1. Create the game page on itch.io, set to **unlisted**, kind "Downloadable",
   platform Linux, price free.
2. Zip the folder:
   ```bash
   cd dist && zip -r pac-man-linux.zip pac-man
   ```
3. Upload it, either by dragging the zip onto the page, or with
   [butler](https://itch.io/docs/butler/):
   ```bash
   butler push dist/pac-man <user>/<game>:linux
   ```
4. Tick "This file will be played in the browser" **off**, and mark the upload
   as executable.
5. In the page description, repeat the controls and the cheat keys, and say
   that `config.json` sits next to the executable and can be edited.

**TO COMPLETE** — the URL of the page, and the credentials or the account that
owns it, so the build can be regenerated and pushed during the review.
