from mazegenerator import MazeGenerator

config = MazeGenerator((15, 15), (0, 0), (10, 10))
config.generate()
maze = config.maze

if __name__ == "__main__":
    print(maze)