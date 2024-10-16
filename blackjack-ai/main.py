import pygame
from player.player_game1 import PlayerBlackjack

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

        # Placeholder start screen logic
        # Assuming we're just playing Blackjack for now
        player_blackjack = PlayerBlackjack(screen)
        player_blackjack.run()

        running = False  # Exit after one game for now

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
