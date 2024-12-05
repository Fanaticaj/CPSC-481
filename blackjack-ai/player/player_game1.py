import pygame
import logging
from games.game1 import Blackjack
from ai.q_table_manager import load_q_table_json
from ai.basic_strategy import choose_action

class PlayerBlackjack:
    def __init__(self, observer_mode, screen=None, q_table=None):
        self.observer_mode = observer_mode
        self.show_hand = False
        self.ai_wait_interval = 1000
        self.screen = screen
        self.game = Blackjack()

        # Load the Q-table for regular blackjack
        self.q_table = q_table if q_table else {}
            

        if self.screen:
            pygame.font.init()  # Initialize fonts if using graphics
            self.font = pygame.font.Font(None, 36)
        else:
            self.font = None  # No font needed in headless mode
    
    def is_pair(self, hand):
        """Check if the player's hand contains a pair."""
        if len(hand) != 2:  # A pair is only possible with exactly two cards
            return False
        return hand[0][0] == hand[1][0]  # Compare the ranks of the two cards

    
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




    def run(self):
        self.game.new_game()
        print(self.game.player_hand)
        print(f'Dealer: {self.game.dealer_hand}')
        print(f'Observer Mode =', self.observer_mode)
        running = True
        ai_action = None
        if self.screen: self.display_game_state()
        while running:
            action = None
            state = (
                self.game.hand_value(self.game.player_hand),
                str(self.game.dealer_hand[0][0]),  # Dealer's visible card
                self.game.has_usable_ace(self.game.player_hand)
            )
            if ai_action == None:
                ai_action = self.get_ai_action(state)

            if self.screen:
                # Display the current game state and AI suggestion
                self.display_game_state(ai_action)  # Pass AI suggestion to the display method
                pygame.display.flip()
                # Only handle Pygame events if a screen is present
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    elif event.type == pygame.KEYDOWN and not self.observer_mode:
                        action = self.get_key_action(event, state)


            if self.observer_mode:
                action = ai_action

            if self.observer_mode: pygame.time.wait(self.ai_wait_interval)
            if action == "Hit":
                ai_action = None
                print("hit!")
                self.game.deal_card(self.game.player_hand)
                if self.game.hand_value(self.game.player_hand) > 21:
                    running = False  # Player busts, end game
            elif action == "Double":
                ai_action = None
                print("double!")
                self.game.deal_card(self.game.player_hand)
                self.show_hand = True
                running = False  # End player's turn, proceed to dealer
            elif action == "Stand":
                ai_action = None
                print("Stand!")
                self.show_hand = True
                running = False  # End player's turn, proceed to check winner
            elif action == "Split" and self.game.can_split(self.game.player_hand):
                ai_action = None
                print("Split!")
                split_hands = self.game.split_hand(self.game.player_hand)
                self.play_split_hands(split_hands)
                self.display_result()
                running = False

        if self.show_hand: self.game.play_dealer_hand() # Deal the dealer's hand at the end
                
        # Display result if screen is available
        if self.screen:
            self.display_game_state()
            pygame.display.flip()
            if self.observer_mode: pygame.time.wait(self.ai_wait_interval) # Delay for AI before results are displayed
            self.display_result()

    def get_key_action(self, event, state):
        """Return 'Hit', 'Double', or 'Stand' based on player input or policy."""
        if self.screen and not self.observer_mode and event.type == pygame.KEYDOWN:
            # Handle interactive keys if screen is present
            if event.key == pygame.K_h:
                return "Hit"
            elif event.key == pygame.K_s:
                return "Stand"
            elif event.key == pygame.K_d:
                return "Double"
            elif event.key == pygame.K_p and self.game.can_split(self.game.player_hand):
                return "Split"
        
    def play_split_hands(self, split_hands):
        for hand in split_hands:
            hand_running = True
            while hand_running:
                state = (
                self.game.hand_value(hand),
                self.game.dealer_hand[0],  # Dealer's visible card
                self.game.has_usable_ace(hand)
                )
                action = self.get_player_action(state)
                if action == "Hit":
                    self.game.deal_card(hand)
                    if self.game.is_bust(hand):
                        hand_running = False
                elif action == "Stand":
                    hand_running = False
                elif action == "Double":
                    self.game.deal_card(hand)
                    hand_running = False

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


    def display_result(self):
        """Display the game result on screen."""
        result = self.game.check_winner()
        print(result)
        result_text = self.font.render(result, True, (255, 255, 255))
        self.screen.blit(result_text, (50, 300))
        pygame.display.flip()
        pygame.time.wait(3000)
