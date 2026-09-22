"""Run from the bundle directory, so that "img/..." paths resolve."""
import os
import sys

if hasattr(sys, "_MEIPASS"):
    os.chdir(sys._MEIPASS)
else:
    os.chdir(os.path.dirname(sys.executable))
