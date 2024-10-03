import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Blackjack Game")

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Define button dimensions
BUTTON_WIDTH = 120
BUTTON_HEIGHT = 50
BUTTON_MARGIN = 20

# Create button class
class Button:
    def __init__(self, x, y, width, height, text, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        font = pygame.font.Font(None, 36)
        text = font.render(self.text, True, BLACK)
        text_rect = text.get_rect(center=self.rect.center)
        surface.blit(text, text_rect)

# Create buttons
hit_button = Button(WIDTH // 2 - BUTTON_WIDTH - BUTTON_MARGIN, HEIGHT - BUTTON_HEIGHT - BUTTON_MARGIN, BUTTON_WIDTH, BUTTON_HEIGHT, "Hit", GREEN)
stand_button = Button(WIDTH // 2 + BUTTON_MARGIN, HEIGHT - BUTTON_HEIGHT - BUTTON_MARGIN, BUTTON_WIDTH, BUTTON_HEIGHT, "Stand", RED)
double_button = Button(WIDTH // 2 - BUTTON_WIDTH // 2, HEIGHT - 2 * (BUTTON_HEIGHT + BUTTON_MARGIN), BUTTON_WIDTH, BUTTON_HEIGHT, "Double", WHITE)
new_game_button = Button(WIDTH // 2 - BUTTON_WIDTH // 2, HEIGHT - 3 * (BUTTON_HEIGHT + BUTTON_MARGIN), BUTTON_WIDTH, BUTTON_HEIGHT, "New Game", BLUE)

# Define card values
card_values = {
    'A': 11, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 10, 'Q': 10, 'K': 10
}

# Create a deck of cards
def create_deck():
    suits = ['S', 'H', 'D', 'C']
    ranks = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
    return [f"{rank}{suit}" for suit in suits for rank in ranks]

# Calculate hand value
def calculate_hand(hand):
    value = sum(card_values[card[:-1]] for card in hand)
    aces = sum(card.startswith('A') for card in hand)
    while value > 21 and aces:
        value -= 10
        aces -= 1
    return value

# Draw text on screen
def draw_text(surface, text, size, x, y):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    surface.blit(text_surface, text_rect)

# Main game loop
def main():
    deck = create_deck()
    random.shuffle(deck)
    player_hand = []
    dealer_hand = []
    game_state = "betting"
    player_score = 0
    dealer_score = 0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if game_state == "player_turn":
                    if hit_button.rect.collidepoint(event.pos):
                        player_hand.append(deck.pop())
                        if calculate_hand(player_hand) > 21:
                            game_state = "dealer_turn"
                    elif stand_button.rect.collidepoint(event.pos):
                        game_state = "dealer_turn"
                    elif double_button.rect.collidepoint(event.pos):
                        player_hand.append(deck.pop())
                        game_state = "dealer_turn"
                elif game_state == "game_over":
                    if new_game_button.rect.collidepoint(event.pos):
                        # Reset the game
                        deck = create_deck()
                        random.shuffle(deck)
                        player_hand = []
                        dealer_hand = []
                        game_state = "betting"

        # Clear the screen
        screen.fill(BLACK)

        if game_state == "betting":
            player_hand = [deck.pop(), deck.pop()]
            dealer_hand = [deck.pop(), deck.pop()]
            game_state = "player_turn"

        elif game_state == "dealer_turn":
            while calculate_hand(dealer_hand) < 17:
                dealer_hand.append(deck.pop())
            game_state = "game_over"

        # Draw hands
        draw_text(screen, f"Player: {' '.join(player_hand)} ({calculate_hand(player_hand)})", 24, WIDTH // 2, HEIGHT // 2 - 50)
        if game_state == "player_turn":
            draw_text(screen, f"Dealer: {dealer_hand[0]} ?", 24, WIDTH // 2, HEIGHT // 2 - 100)
        else:
            draw_text(screen, f"Dealer: {' '.join(dealer_hand)} ({calculate_hand(dealer_hand)})", 24, WIDTH // 2, HEIGHT // 2 - 100)

        # Draw buttons
        if game_state == "player_turn":
            stand_button.draw(screen)
            double_button.draw(screen)
            hit_button.draw(screen)        
        elif game_state == "game_over":
            player_score = calculate_hand(player_hand)
            dealer_score = calculate_hand(dealer_hand)
            if player_score > 21:
                result = "Player Busts! Dealer Wins!"
            elif dealer_score > 21:
                result = "Dealer Busts! Player Wins!"
            elif player_score > dealer_score:
                result = "Player Wins!"
            elif dealer_score > player_score:
                result = "Dealer Wins!"
            else:
                result = "It's a Tie!"
            draw_text(screen, result, 36, WIDTH // 2, HEIGHT // 2 + 50)
            new_game_button.draw(screen)

        # Update the display
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
