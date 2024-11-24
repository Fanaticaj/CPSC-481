import pygame
from games.game2 import SpanishBlackjack  
import random

class PlayerSpanishBlackjack:
    def __init__(self, screen=None):
        self.screen = screen
        self.show_hand = False
        self.game = SpanishBlackjack()
        if self.screen:
            pygame.font.init()  # Initialize fonts if using graphics
            self.font = pygame.font.Font(None, 36)
        else:
            self.font = None  # No font needed in headless mode

    def run(self):
        self.game.new_game()
        running = True
        while running:
            if self.screen:
                # Handle Pygame events if a screen is present
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False

            # Handle player actions for hitting or standing
            action = self.get_player_action()
            if action == "Hit":
                self.game.deal_card(self.game.player_hand)
                pygame.time.wait(100) # Without this it keeps on hitting every single frame, instead of just once
                if self.game.hand_value(self.game.player_hand) > 21:
                    running = False  # Player busts, end game
            elif action == "Stand":
                self.show_hand = True
                running = False  # End player's turn, proceed to check winner

            # Display game state if screen is available
            if self.screen:
                self.display_game_state()
                pygame.display.flip()

            # Dealer plays their hand
            self.game.play_dealer_hand()

        # Display result if screen is available
        if self.screen:
            self.display_result()

    def get_player_action(self):
        """Return 'Hit' or 'Stand' based on player input or policy."""
        if self.screen:
            # Handle interactive keys if screen is present
            keys = pygame.key.get_pressed()
            if keys[pygame.K_h]:
                return "Hit"
            elif keys[pygame.K_s]:
                return "Stand"
        else:
            # In headless mode, return random or policy-based actions
            return "Hit" if random.random() < 0.5 else "Stand"  # Example: random action for testing

    def display_game_state(self):
        """Display the player's and dealer's hand values on screen."""
        player_x_position = 400
        player_y_position = 100
        dealer_x_position = 400
        dealer_y_position = 400
        player_val = self.game.hand_value(self.game.player_hand)
        dealer_val = self.game.hand_value(self.game.dealer_hand[:1])  # Dealer shows only one card

        player_text = self.font.render(f"Player Hand: {player_val}", True, (255, 255, 255))
        dealer_text = self.font.render(f"Dealer Hand: {dealer_val}", True, (255, 255, 255))

        self.screen.fill((0, 100, 0))  # Green background
        self.screen.blit(player_text, (50, 100))
        for i in self.game.player_hand:
            player_score = pygame.font.Font(None, 30).render(str(i[0]), True, "black")
            pygame.draw.rect(self.screen, 'white', [player_x_position, player_y_position, 100, 150], 0, 5)
            # Draw the text inside the rectangle
            top_left_text_position = (player_x_position + 10, player_y_position + 10)
            bottom_right_text_position = (player_x_position + 70, player_y_position + 120)
            self.screen.blit(player_score, top_left_text_position)
            self.screen.blit(player_score, bottom_right_text_position)
            # Move to the next position for the next card
            player_x_position += 110  # Add spacing between cards
        
         # DEALER HAND
        if self.show_hand == True:
            for i in self.game.dealer_hand:
                dealer_score = pygame.font.Font(None, 30).render(str(i[0]), True, "black")
                pygame.draw.rect(self.screen, 'white', [dealer_x_position, dealer_y_position, 100, 150], 0, 5)
                # Draw the text inside the rectangle
                top_left_text_position = (dealer_x_position + 10, dealer_y_position + 10)
                bottom_right_text_position = (dealer_x_position + 70, dealer_y_position + 120)
                self.screen.blit(dealer_score, top_left_text_position)
                self.screen.blit(dealer_score, bottom_right_text_position)
                dealer_x_position += 110  # Add spacing between cards
                dealer_val = self.game.hand_value(self.game.dealer_hand)
                dealer_text = self.font.render(f"Dealer Hand: {dealer_val}", True, (255, 255, 255))
                self.screen.blit(dealer_text, (50, 400))
        else: # Show just the first card, before the player ends their turn
            dealer_score = pygame.font.Font(None, 30).render(str(dealer_val), True, "black")
            pygame.draw.rect(self.screen, 'white', [dealer_x_position, dealer_y_position, 100, 150], 0, 5)
            # Draw the text inside the rectangle
            top_left_text_position = (dealer_x_position + 10, dealer_y_position + 10)
            bottom_right_text_position = (dealer_x_position + 70, dealer_y_position + 120)
            self.screen.blit(dealer_score, top_left_text_position)
            self.screen.blit(dealer_score, bottom_right_text_position)
            dealer_x_position += 110  # Add spacing between cards
            self.screen.blit(dealer_text, (50, 400))

    def display_result(self):
        """Display the game result on screen."""
        result = self.game.check_winner()
        result_text = self.font.render(result, True, (255, 255, 255))
        self.screen.blit(result_text, (50, 300))
        pygame.display.flip()
        pygame.time.wait(3000)

# Example usage:
if __name__ == "__main__":
    screen = pygame.display.set_mode((800, 600))
    game = PlayerSpanishBlackjack(screen=screen)
    game.run()
    pygame.quit()
