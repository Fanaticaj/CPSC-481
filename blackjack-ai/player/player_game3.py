import pygame
from games.game3 import BlackjackSwitch
import random

class PlayerBlackjackSwitch:
    def __init__(self, screen=None):
        self.screen = screen
        self.game = BlackjackSwitch()
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

            # Display game state
            if self.screen:
                self.display_game_state()

            # Handle player actions
            action = self.get_player_action()
            if action == "Switch":
                self.game.switch_cards()
            elif action == "Hit Hand 1":
                self.game.deal_card(self.game.player_hand1)
                if self.game.hand_value(self.game.player_hand1) > 21:
                    running = False  # Player busts, end game
            elif action == "Hit Hand 2":
                self.game.deal_card(self.game.player_hand2)
                if self.game.hand_value(self.game.player_hand2) > 21:
                    running = False  # Player busts, end game
            elif action == "Stand":
                running = False  # End player's turn, proceed to check winner

            if self.screen:
                pygame.display.flip()

        # Display result
        if self.screen:
            self.display_result()

    def get_player_action(self):
        """Return 'Switch', 'Hit Hand 1', 'Hit Hand 2', or 'Stand' based on player input or policy."""
        if self.screen:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_s]:
                return "Switch"
            elif keys[pygame.K_h]:
                # Determine which hand to hit based on additional input
                return "Hit Hand 1" if keys[pygame.K_1] else "Hit Hand 2"
            elif keys[pygame.K_t]:
                return "Stand"
        else:
            # In headless mode, return random or policy-based actions
            return random.choice(["Switch", "Hit Hand 1", "Hit Hand 2", "Stand"])

    def display_game_state(self):
        """Display the game state for both hands and the dealer's visible card."""
        player_val1 = self.game.hand_value(self.game.player_hand1)
        player_val2 = self.game.hand_value(self.game.player_hand2)
        dealer_val = self.game.hand_value(self.game.dealer_hand[:1])  # Dealer shows only one card

        self.screen.fill((0, 100, 0))  # Green background
        player_text1 = self.font.render(f"Player Hand 1: {player_val1}", True, (255, 255, 255))
        player_text2 = self.font.render(f"Player Hand 2: {player_val2}", True, (255, 255, 255))
        dealer_text = self.font.render(f"Dealer Hand: {dealer_val}", True, (255, 255, 255))

        self.screen.blit(player_text1, (50, 50))
        self.screen.blit(player_text2, (50, 100))
        self.screen.blit(dealer_text, (50, 150))

    def display_result(self):
        """Display the game results for both hands."""
        results = self.game.check_winner()
        y_offset = 200
        for result in results:
            result_text = self.font.render(result, True, (255, 255, 255))
            self.screen.blit(result_text, (50, y_offset))
            y_offset += 50

        pygame.display.flip()
        pygame.time.wait(3000)