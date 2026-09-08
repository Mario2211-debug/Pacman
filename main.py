from mazegenerator import MazeGenerator
import pygame
import sys


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
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        screen.fill((40, 40, 40))
        text = font.render("Game Started!", True, WHITE)
        screen.blit(text, (250, 250))

        pygame.display.update()


def start_menu():
    while True:

        screen.fill(BG)
        mouse = pygame.mouse.get_pos()

        play_button = pygame.Rect(300, 300, 140, 50)
        quit_button = pygame.Rect(300, 300, 140, 50)

        pygame.draw.rect(screen,
                         LIGHT if play_button.collidepoint(mouse) else DARK,
                         play_button)
        pygame.draw.rect(screen,
                         LIGHT if quit_button.collidepoint(mouse) else DARK,
                         quit_button)

        play_text = font.render("Play", True, WHITE)
        quit_text = font.render("Quit", True, WHITE)

        screen.blit(play_text, (335, 305))
        screen.blit(quit_text, (335, 385))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.collidepoint(mouse):
                    game()

                if quit_button.collidepoint(mouse):
                    pygame.quit()
                    sys.exit()
        pygame.display.update()


if __name__ == "__main__":
    start_menu()
    print(maze)
