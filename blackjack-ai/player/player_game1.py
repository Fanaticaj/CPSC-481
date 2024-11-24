import pygame
from games.game1 import Blackjack
import random

class PlayerBlackjack:
    def __init__(self, screen=None):
        self.show_hand = False
        self.screen = screen
        self.game = Blackjack()
        if self.screen:
            pygame.font.init()  # Initialize fonts if using graphics
            self.font = pygame.font.Font(None, 36)
        else:
            self.font = None  # No font needed in headless mode

    def run(self):
        self.game.new_game()
        print(self.game.player_hand)
        print(f'Dealer: {self.game.dealer_hand}')
        running = True
        while running:
            if self.screen:
                # Only handle Pygame events if a screen is present
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
            elif action == "Double":
                self.game.deal_card(self.game.player_hand)
                self.show_hand = True
                running = False  # End player's turn, proceed to dealer
            elif action == "Stand":
                self.show_hand = True
                running = False  # End player's turn, proceed to check winner
            elif action == "Split" and self.game.can_split(self.game.player_hand):
                split_hands = self.game.split_hand(self.game.player_hand)
                self.play_split_hands(split_hands)
                running = False

            self.game.play_dealer_hand() # Deal the dealer's hand at the end
            # Display game state if screen is available
            if self.screen:
                self.display_game_state()
                pygame.display.flip()

        # Display result if screen is available
        if self.screen:
            self.display_result()

    def get_player_action(self):
        """Return 'Hit', 'Double', or 'Stand' based on player input or policy."""
        if self.screen:
            # Handle interactive keys if screen is present
            keys = pygame.key.get_pressed()
            if keys[pygame.K_h]:
                return "Hit"
            elif keys[pygame.K_s]:
                return "Stand"
            elif keys[pygame.K_d]:
                return "Double"
            elif keys[pygame.K_p] and self.game.can_split(self.game.player_hand):
                return "Split"
        else:
            # In headless mode, return random or policy-based actions
            return "Hit" if random.random() < 0.5 else "Stand"  # Example: random action for testing
    
    def play_split_hands(self, split_hands):
        for hand in split_hands:
            hand_running = True
            while hand_running:
                action = self.get_player_action()
                if action == "Hit":
                    self.game.deal_card(hand)
                    if self.game.is_bust(hand):
                        hand_running = False
                elif action == "Stand":
                    hand_running = False
                elif action == "Double":
                    self.game.deal_card(hand)
                    hand_running = False

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
        # PLAYER HAND
        for i in self.game.player_hand:
            player_score = pygame.font.Font(None, 30).render(str(i[0]), True, "black")
            pygame.draw.rect(self.screen, 'white', [player_x_position, player_y_position, 100, 150], 0, 5)
            # Draw the text inside the rectangle
            top_left_text_position = (player_x_position + 10, player_y_position + 10)
            bottom_right_text_position = (player_x_position + 75, player_y_position + 125)
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
                bottom_right_text_position = (dealer_x_position + 75, dealer_y_position + 125)
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
            bottom_right_text_position = (dealer_x_position + 75, dealer_y_position + 125)
            self.screen.blit(dealer_score, top_left_text_position)
            self.screen.blit(dealer_score, bottom_right_text_position)
            dealer_x_position += 110  # Add spacing between cards
            self.screen.blit(dealer_text, (50, 400))

        # pygame.draw.rect(self.screen, 'white', [400, 300, 100, 150], 0, 5)
        self.screen.blit(player_text, (50, 100))

    def display_result(self):
        """Display the game result on screen."""
        result = self.game.check_winner()
        result_text = self.font.render(result, True, (255, 255, 255))
        self.screen.blit(result_text, (50, 300))
        pygame.display.flip()
        pygame.time.wait(3000)
