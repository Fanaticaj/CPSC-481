import pygame
import logging
from games.game1 import Blackjack
import random
from ai.basic_strategy import choose_action
class PlayerBlackjack:
    def __init__(self, observer_mode, screen=None):
        self.observer_mode = observer_mode
    def __init__(self, observer_mode, screen=None):
        self.observer_mode = observer_mode
        self.show_hand = False
        self.ai_wait_interval = 1000
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
        print(f'Observer Mode =', self.observer_mode)
        running = True
        print("displaying game")
        self.display_game_state()
        while running:
            action = None
            state = (
                self.game.hand_value(self.game.player_hand),
                self.game.dealer_hand[0],  # Dealer's visible card
                self.game.has_usable_ace(self.game.player_hand)
            )

            if self.screen:
                # Only handle Pygame events if a screen is present
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        x, y = event.pos
                        action = self.get_button_action(x, y, state)  # Now uses policy-based action in headless mode
                    elif event.type == pygame.KEYDOWN and not self.observer_mode:
                        print(event.key)
                        action = self.get_key_action(event, state)

            if self.observer_mode:
                action = self.get_ai_action(state)

            if action == "Hit":
                print("hit!")
                self.game.deal_card(self.game.player_hand)
                pygame.time.wait(100) # Without this it keeps on hitting every single frame, instead of just once
                if self.game.hand_value(self.game.player_hand) > 21:
                    running = False  # Player busts, end game
            elif action == "Double":
                print("double!")
                self.game.deal_card(self.game.player_hand)
                self.show_hand = True
                self.game.play_dealer_hand() # Deal the dealer's hand at the end
                running = False  # End player's turn, proceed to dealer
            elif action == "Stand":
                print("Stand!")
                self.show_hand = True
                self.game.play_dealer_hand() # Deal the dealer's hand at the end
                running = False  # End player's turn, proceed to check winner
            elif action == "Split" and self.game.can_split(self.game.player_hand):
                print("Split!")
                split_hands = self.game.split_hand(self.game.player_hand)
                self.play_split_hands(split_hands)
                self.display_result()
                running = False

            
            # Display game state if screen is available
            if self.screen:
                self.display_game_state()
                pygame.display.flip()
        if self.observer_mode: pygame.time.wait(self.ai_wait_interval) # Delay for AI before results are displayed
        # Display result if screen is available
        if self.screen:
            if self.observer_mode: pygame.time.wait(self.ai_wait_interval) # Wait for a predetermined time if observer mode is active.
            self.display_result()

    def get_key_action(self, event, state):
        """Return 'Hit', 'Double', or 'Stand' based on player input or policy."""
        print(not self.observer_mode, event.type == pygame.KEYDOWN)
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
        
    def get_ai_action(self, state):
        if self.observer_mode: pygame.time.wait(self.ai_wait_interval)
        return choose_action(state, self.game.player_hand, ["Hit", "Stand", "Double", "Split"] )
    
    def get_button_action(self, x, y, state):
        print("hi")
    
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
        print(result)
        result_text = self.font.render(result, True, (255, 255, 255))
        self.screen.blit(result_text, (50, 300))
        pygame.display.flip()
        pygame.time.wait(3000)
