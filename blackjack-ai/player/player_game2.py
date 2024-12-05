import time
import pygame
from games.game2 import SpanishBlackjack  
from ai.q_table_spanish_manager import load_q_table_spanish_json
from ai.basic_strategy_spanishbj import choose_action

import random

class PlayerSpanishBlackjack:
    def __init__(self, screen=None, q_table=load_q_table_spanish_json()):
        self.screen = screen
        self.game = SpanishBlackjack()
        self.show_hand = False
        # Load the Q-table for regular blackjack
        self.q_table = q_table if q_table else {}

        if self.screen:
            pygame.font.init()  # Initialize fonts if using graphics
            self.font = pygame.font.Font(None, 36)
        else:
            self.font = None  # No font needed in headless mode

    def run(self):
        self.game.new_game()
        running = True
        ai_action = None

        while running:
            # Get the current state
            state = (
                self.game.hand_value(self.game.player_hand),
                str(self.game.dealer_hand[0][0]),  # Dealer's visible card
                self.game.has_usable_ace(self.game.player_hand)
            )

            # Calculate AI action if not already set
            if ai_action is None:
                ai_action = self.get_ai_action(state)

            # Display the game state with the current AI action
            if self.screen:
                self.display_game_state(ai_action)

                # Handle Pygame events
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False

            # Handle player actions for hitting or standing
            action = self.get_player_action()
            if action == "Hit":
                print("hit!")
                self.game.deal_card(self.game.player_hand)
                ai_action = None  # Reset AI action to recalculate next loop
                pygame.time.wait(100)
                if self.game.hand_value(self.game.player_hand) > 21:
                    running = False  # Player busts, end game
            elif action == "Stand":
                print("stand!")
                self.show_hand = True
                running = False  # End player's turn, proceed to check winner

            # Let the dealer play their hand if the player is done
            if not running and action == "Stand":
                self.game.play_dealer_hand()

            # Display game state if screen is available
            if self.screen:
                self.display_game_state(ai_action)
                pygame.display.flip()

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

    def display_game_state(self, ai_action=None):
        """Display the player's and dealer's hand values on screen."""
        player_x_position = 400
        player_y_position = 100
        dealer_x_position = 400
        dealer_y_position = 400
        player_val = self.game.hand_value(self.game.player_hand)
        dealer_val = self.game.hand_value(self.game.dealer_hand[:1])  # Dealer shows only one card

        # Fill background
        self.screen.fill((0, 100, 0))  # Green background

        # Draw AI suggestion box
        ai_box_x = 800  # Position of the box on the right
        ai_box_y = 50
        ai_box_width = 300
        ai_box_height = 100
        pygame.draw.rect(self.screen, (200, 200, 200), (ai_box_x, ai_box_y, ai_box_width, ai_box_height), 0, 10)  # Box with rounded corners

        # Display AI suggestion text in the box
        if ai_action:
            suggestion_text = self.font.render(f"AI Bot says: {ai_action}!", True, (0, 0, 0))
            suggestion_rect = suggestion_text.get_rect(center=(ai_box_x + ai_box_width // 2, ai_box_y + ai_box_height // 2))
            self.screen.blit(suggestion_text, suggestion_rect)

        # Render player cards
        for i in self.game.player_hand:
            player_score = pygame.font.Font(None, 30).render(str(i[0]), True, "black")
            pygame.draw.rect(self.screen, 'white', [player_x_position, player_y_position, 100, 150], 0, 5)
            # Draw the text inside the rectangle
            top_left_text_position = (player_x_position + 10, player_y_position + 10)
            bottom_right_text_position = (player_x_position + 75, player_y_position + 125)
            self.screen.blit(player_score, top_left_text_position)
            self.screen.blit(player_score, bottom_right_text_position)
            player_x_position += 110  # Add spacing between cards

        # Render dealer cards
        if self.show_hand:
            for i in self.game.dealer_hand:
                dealer_score = pygame.font.Font(None, 30).render(str(i[0]), True, "black")
                pygame.draw.rect(self.screen, 'white', [dealer_x_position, dealer_y_position, 100, 150], 0, 5)
                top_left_text_position = (dealer_x_position + 10, dealer_y_position + 10)
                bottom_right_text_position = (dealer_x_position + 75, dealer_y_position + 125)
                self.screen.blit(dealer_score, top_left_text_position)
                self.screen.blit(dealer_score, bottom_right_text_position)
                dealer_x_position += 110  # Add spacing between cards

            dealer_val = self.game.hand_value(self.game.dealer_hand)  # Dealer shows only one card
        else:
            dealer_score = pygame.font.Font(None, 30).render(str(dealer_val), True, "black")
            pygame.draw.rect(self.screen, 'white', [dealer_x_position, dealer_y_position, 100, 150], 0, 5)
            top_left_text_position = (dealer_x_position + 10, dealer_y_position + 10)
            bottom_right_text_position = (dealer_x_position + 75, dealer_y_position + 125)
            self.screen.blit(dealer_score, top_left_text_position)
            self.screen.blit(dealer_score, bottom_right_text_position)

        # Render Player and Dealer Hand text
        player_text = self.font.render(f"Player Hand: {player_val}", True, (255, 255, 255))
        dealer_text = self.font.render(f"Dealer Hand: {dealer_val}", True, (255, 255, 255))
        self.screen.blit(player_text, (50, 100))
        self.screen.blit(dealer_text, (50, 400))

    def get_ai_action(self, state):
        """Retrieve the best action from the Q-table for the current state."""
        if state in self.q_table:
            action_values = self.q_table[state]
        
            # Exclude "Double" if the player has more than two cards
            if len(self.game.player_hand) > 2 and "Double" in action_values:
                action_values = {k: v for k, v in action_values.items() if k != "Double"}
        
            # Exclude "Split" if the player's hand is not a pair
            if not self.is_pair(self.game.player_hand) and "Split" in action_values:
                action_values = {k: v for k, v in action_values.items() if k != "Split"}
        
            # Get the action with the highest value
            best_action = max(action_values, key=action_values.get)
        
            # Log state details and AI recommendation only once per state
            if not hasattr(self, "logged_states"):
                self.logged_states = set()
            if state not in self.logged_states:
                print(f"Current State: {state}")
                print(f"Action Values: {action_values}")
                print(f"AI says to {best_action}")
                self.logged_states.add(state)
            return best_action
        else:
            # Log missing state details only once
            if not hasattr(self, "logged_states"):
                self.logged_states = set()
            if state not in self.logged_states:
                print(f"State not found in Q-table. Defaulting to 'Stand'. Current State: {state}")
                self.logged_states.add(state)
            return "Stand"  # Default action if the state is not in the Q-table

    def is_pair(self, hand):
        """Check if the player's hand contains a pair."""
        if len(hand) != 2:  # A pair is only possible with exactly two cards
            return False
        return hand[0][0] == hand[1][0]  # Compare the ranks of the two cards


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
