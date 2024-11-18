import pygame
from player.player_game1 import PlayerBlackjack
from player.player_game2 import SpanishBlackjack
from player.player_game3 import PlayerBlackjackSwitch
import main_menu

# Initialize Pygame
pygame.init()

# Set up the game window
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Game Selection Screen")

def main():
    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                main_menu.main_menu()

        running = False  # Exit after one game for now

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
