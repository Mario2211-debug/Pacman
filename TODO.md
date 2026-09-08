# GOAL
In this project, you will create a complete and playable Pac-Man game in Python, using
object-oriented programming, a simple graphical library (MLX or similar), and a modular, reusable architecture.
### The game must support:
- A custom configuration via a file (JSON with comments) to set game parameters.
- Robust error handling, no crash!
- Level generation based on an external ‘A-Maze-ing‘ package (not yours!).
- A persistent highscore system of your choice (stored in a json file on project, saved
to disk, etc.).
- A polished graphical UI with main menu, game view, and game-over handling.
- A cheat mode for evaluation purposes.
- Deployment to a public gaming platform (Steam/Itch.io or similar) for demonstration.
# Configuration file
The config file uses JSON. In addition to the standard JSON format, you must handle comments. Lines starting with # are comments and must be ignored. You may also support additional comment styles (e.g., C or C++). The exact structure is up to you, but document your keys in the README and provide robust defaults.

Suggested keys (names are indicative):
- highscore_filename
- level array of multiple levels
- width , height for each level
- lives : 3
- pacgum : 42
- points_per_pacgum : 10
- points_per_super_pacgum : 50
- points_per_ghost : 200
- seed : 42
- level_max_time : 90
## Faulty config handlingV.3 Faulty config handling