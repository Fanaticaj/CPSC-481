import pygame
import logging
from games.game1 import Blackjack
import random
from ai.basic_strategy import choose_action
class PlayerBlackjack:
    def __init__(self, screen=None):
        self.screen = screen
        self.game = Blackjack()
        if self.screen:
            pygame.font.init()  # Initialize fonts if using graphics
            self.font = pygame.font.Font(None, 36)
        else:
            self.font = None  # No font needed in headless mode

    def run(self):
        self.game.new_game()
        running = True
        while running:
            state = (
                self.game.hand_value(self.game.player_hand),
                self.game.dealer_hand[0],  # Dealer's visible card
                self.game.has_usable_ace(self.game.player_hand)
            )
            
            action = self.get_player_action(state)  # Now uses policy-based action in headless mode
            
            if action == "Hit":
                self.game.deal_card(self.game.player_hand)
                if self.game.is_bust(self.game.player_hand):
                    running = False
            elif action == "Double":
                self.game.deal_card(self.game.player_hand)
                running = False
            elif action == "Stand":
                running = False
            elif action == "Split" and self.game.can_split(self.game.player_hand):
                split_hands = self.game.split_hand(self.game.player_hand)
                self.play_split_hands(split_hands)
                self.display_result()
                running = False

            if not self.screen:
                logging.info(f"Player Hand: {self.game.player_hand}, Dealer Card: {self.game.dealer_hand[0]}, Action: {action}")
            
            if self.screen:
                self.display_game_state()
                pygame.display.flip()

    def get_player_action(self, state):
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
            return choose_action(state, self.game.player_hand)
    
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
            bottom_right_text_position = (player_x_position + 70, player_y_position + 120)
            self.screen.blit(player_score, top_left_text_position)
            self.screen.blit(player_score, bottom_right_text_position)
            # Move to the next position for the next card
            player_x_position += 110  # Add spacing between cards
            
        # DEALER HAND
        for i in self.game.dealer_hand:
            dealer_score = pygame.font.Font(None, 30).render(str(i[0]), True, "black")
            pygame.draw.rect(self.screen, 'white', [dealer_x_position, dealer_y_position, 100, 150], 0, 5)
            # Draw the text inside the rectangle
            top_left_text_position = (dealer_x_position + 10, dealer_y_position + 10)
            bottom_right_text_position = (dealer_x_position + 70, dealer_y_position + 120)
            self.screen.blit(dealer_score, top_left_text_position)
            self.screen.blit(dealer_score, bottom_right_text_position)
            dealer_x_position += 110  # Add spacing between cards

        # pygame.draw.rect(self.screen, 'white', [400, 300, 100, 150], 0, 5)
        self.screen.blit(player_text, (50, 50))
        self.screen.blit(dealer_text, (50, 150))

    def display_result(self):
        """Display the game result on screen."""
        result = self.game.check_winner()
        result_text = self.font.render(result, True, (255, 255, 255))
        self.screen.blit(result_text, (50, 300))
        pygame.display.flip()
        pygame.time.wait(3000)
