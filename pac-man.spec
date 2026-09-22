# PyInstaller spec for Pac-Man.
#
# Build from the project root:
#     make package
# or:
#     uv run --with pyinstaller pyinstaller pac-man.spec --noconfirm
#
# Produces dist/pac-man/, a self-contained folder: zip it and upload it.

import os

from PyInstaller.utils.hooks import collect_dynamic_libs

ROOT = os.path.abspath(SPECPATH)

# mlx ships libmlx.so inside the package and loads it from its own directory,
# so it has to keep that layout in the bundle.
mlx_binaries = collect_dynamic_libs("mlx", destdir="mlx")

a = Analysis(
    [os.path.join(ROOT, "pac-man.py")],
    pathex=[ROOT],
    binaries=mlx_binaries,
    datas=[
        (os.path.join(ROOT, "img"), "img"),          # sprites and glyphs
        (os.path.join(ROOT, "config.json"), "."),    # default configuration
    ],
    hiddenimports=["mazegenerator"],
    hookspath=[],
    runtime_hooks=[os.path.join(SPECPATH, "packaging", "runtime_chdir.py")],
    excludes=["mypy", "flake8", "pytest"],
)

pyz = PYZ(a.pure, a.zipped_data)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="pac-man",
    console=False,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=False,
    name="pac-man",
)
