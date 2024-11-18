import pygame
from games.game3 import BlackjackSwitch
import random

class PlayerBlackjackSwitch:
    def __init__(self, screen=None):
        self.screen = screen
        self.game = BlackjackSwitch()
        self.switch_pressed = False  # To prevent continuous switching
        self.double_done_hand1 = False  # Track if Hand 1 has doubled
        self.double_done_hand2 = False  # Track if Hand 2 has doubled
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
                # Only handle Pygame events if a screen is present
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    elif event.type == pygame.KEYUP:
                        # Reset switch_pressed when 'S' is released
                        if event.key == pygame.K_s:
                            self.switch_pressed = False

            # Display game state
            if self.screen:
                self.display_game_state()

            # Handle player actions
            action = self.get_player_action()
            if action == "Switch" and not self.switch_pressed:
                self.game.switch_cards()
                self.switch_pressed = True  # Prevent continuous switching
            elif action == "Hit Hand 1":
                self.game.deal_card(self.game.player_hand1)
                if self.game.hand_value(self.game.player_hand1) > 21:
                    running = False  # Player busts, end game
            elif action == "Hit Hand 2":
                self.game.deal_card(self.game.player_hand2)
                if self.game.hand_value(self.game.player_hand2) > 21:
                    running = False  # Player busts, end game
            elif action == "Double Hand 1" and not self.double_done_hand1:
                self.game.deal_card(self.game.player_hand1)
                self.double_done_hand1 = True
                running = False  # End player's turn for this hand
            elif action == "Double Hand 2" and not self.double_done_hand2:
                self.game.deal_card(self.game.player_hand2)
                self.double_done_hand2 = True
                running = False  # End player's turn for this hand
            elif action == "Stand":
                running = False  # End player's turn, proceed to check winner

            if self.screen:
                pygame.display.flip()

        # Display result
        if self.screen:
            self.display_full_result()

    def get_player_action(self):
        """Return 'Switch', 'Hit Hand 1', 'Hit Hand 2', 'Double Hand 1', 'Double Hand 2', or 'Stand' based on player input or policy."""
        if self.screen:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_s]:
                return "Switch"
            elif keys[pygame.K_1]:
                return "Hit Hand 1"
            elif keys[pygame.K_2]:
                return "Hit Hand 2"
            elif keys[pygame.K_q]:
                return "Double Hand 1"
            elif keys[pygame.K_w]:
                return "Double Hand 2"
            elif keys[pygame.K_t]:
                return "Stand"
        else:
            # In headless mode, return random or policy-based actions
            return random.choice(["Switch", "Hit Hand 1", "Hit Hand 2", "Double Hand 1", "Double Hand 2", "Stand"])

    def display_game_state(self):
        """Display the game state for both hands and the dealer's visible card."""
        player_val1 = self.game.hand_value(self.game.player_hand1)
        player_val2 = self.game.hand_value(self.game.player_hand2)
        dealer_val = self.game.hand_value(self.game.dealer_hand[:1])  # Dealer shows only one card

        player_hand1_str = ', '.join([f'{card[0]}{card[1][0]}' for card in self.game.player_hand1])
        player_hand2_str = ', '.join([f'{card[0]}{card[1][0]}' for card in self.game.player_hand2])
        dealer_hand_str = ', '.join([f'{card[0]}{card[1][0]}' for card in self.game.dealer_hand[:1]])

        self.screen.fill((0, 100, 0))  # Green background
        player_text1 = self.font.render(f"Player Hand 1: {player_val1} ({player_hand1_str})", True, (255, 255, 255))
        player_text2 = self.font.render(f"Player Hand 2: {player_val2} ({player_hand2_str})", True, (255, 255, 255))
        dealer_text = self.font.render(f"Dealer Hand: {dealer_val} ({dealer_hand_str})", True, (255, 255, 255))

        self.screen.blit(player_text1, (50, 50))
        self.screen.blit(player_text2, (50, 100))
        self.screen.blit(dealer_text, (50, 150))

    def display_full_result(self):
        """Display the full dealer hand and the game results."""
        dealer_val = self.game.hand_value(self.game.dealer_hand)
        dealer_hand_str = ', '.join([f'{card[0]}{card[1][0]}' for card in self.game.dealer_hand])

        player_val1 = self.game.hand_value(self.game.player_hand1)
        player_hand1_str = ', '.join([f'{card[0]}{card[1][0]}' for card in self.game.player_hand1])

        player_val2 = self.game.hand_value(self.game.player_hand2)
        player_hand2_str = ', '.join([f'{card[0]}{card[1][0]}' for card in self.game.player_hand2])

        results = self.game.check_winner()

        self.screen.fill((0, 100, 0))  # Green background
        dealer_text = self.font.render(f"Dealer Hand: {dealer_val} ({dealer_hand_str})", True, (255, 255, 255))
        player_text1 = self.font.render(f"Player Hand 1: {player_val1} ({player_hand1_str})", True, (255, 255, 255))
        player_text2 = self.font.render(f"Player Hand 2: {player_val2} ({player_hand2_str})", True, (255, 255, 255))

        self.screen.blit(dealer_text, (50, 50))
        self.screen.blit(player_text1, (50, 100))
        self.screen.blit(player_text2, (50, 150))

        # Display results for both hands
        y_offset = 200
        for result in results:
            result_text = self.font.render(result, True, (255, 255, 255))
            self.screen.blit(result_text, (50, y_offset))
            y_offset += 50

        pygame.display.flip()
        pygame.time.wait(5000)