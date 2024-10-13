import pygame
import csv
import sys
from PlayerSelect import player_select_screen

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Blackjack AI - Start Screen")

# Colors
BACKGROUND = (76, 84, 84)
BLACK = (0, 0, 0)
RED = (255, 113, 91)
GREEN = (30, 168, 150)
WHITE = (255, 255, 255)
BLUE = (52, 138, 167)

# Fonts
font_large = pygame.font.SysFont("arial", 30)
font_medium = pygame.font.SysFont("arial", 20)
font_small = pygame.font.SysFont("arial", 15)

def draw_button(text, x, y, width, height, color, text_color):
    pygame.draw.rect(screen, color, (x, y, width, height))
    text_surface = font_medium.render(text, True, text_color)
    text_rect = text_surface.get_rect(center=(x + width // 2, y + height // 2))
    screen.blit(text_surface, text_rect)

def get_player_cash():
    try:
        with open('blackjack-ai/player_cash.csv', 'r') as file:
            reader = csv.reader(file)
            cash = next(reader)[0]
        return int(cash)
    except:
        return 1000  # Default starting cash

def player_select_screen(selected_game, player_cash):
    # Move the implementation of player_select_screen here
    pass  # Replace this with the actual implementation

def start_screen(player_cash):
    # Move the implementation of start_screen here
    pass  # Replace this with the actual implementation

if __name__ == "__main__":
    selected_game, player_cash = start_screen()
    player_select_screen(selected_game, player_cash)  # Call player_select_screen here
    print(f"Selected game: {selected_game}")
