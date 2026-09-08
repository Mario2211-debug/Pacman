from mazegenerator import MazeGenerator
import pygame

pygame.init()
config = MazeGenerator((15, 15), (0, 0), (10, 10))
config.generate()
maze = config.maze


screen = pygame.display.set_mode((720, 720))
pygame.display.set_caption("Pacman")


WHITE = (255, 255, 255)
LIGHT = (170, 170, 170)
DARK = (100, 100, 100)
BG = (60, 25, 60)

font = pygame.font.SysFont("Corbel", 40)


def game():
    while True:
        for event in pygame.event.get():
            
if __name__ == "__main__":
    print(maze)
