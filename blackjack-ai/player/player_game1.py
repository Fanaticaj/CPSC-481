import pygame
from games.game1 import Blackjack
import random

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
            if self.screen:
                # Only handle Pygame events if a screen is present
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False

            # Handle player actions for hitting or standing
            action = self.get_player_action()
            if action == "Hit":
                self.game.deal_card(self.game.player_hand)
                if self.game.hand_value(self.game.player_hand) > 21:
                    running = False  # Player busts, end game
            elif action == "Double":
                self.game.deal_card(self.game.player_hand)
                running = False  # End player's turn, proceed to dealer
            elif action == "Stand":
                running = False  # End player's turn, proceed to check winner
            # elif keys[pygame.K_d]: # Player chooses to "Double Down"
            #     if len(self.game.player_hand) == 2:  # Can only double on first two cards
            #         self.game.deal_card(self.game.player_hand)
            #         running = False  # End player's turn after doubling
            #     else:
            #         # Optionally, display a message that doubling is not allowed
            #         pass

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
        else:
            # In headless mode, return random or policy-based actions
            return "Hit" if random.random() < 0.5 else "Stand"  # Example: random action for testing

    def display_game_state(self):
        """Display the player's and dealer's hand values on screen."""
        player_val = self.game.hand_value(self.game.player_hand)
        dealer_val = self.game.hand_value(self.game.dealer_hand[:1])  # Dealer shows only one card

        player_text = self.font.render(f"Player Hand: {player_val}", True, (255, 255, 255))
        dealer_text = self.font.render(f"Dealer Hand: {dealer_val}", True, (255, 255, 255))

        self.screen.fill((0, 100, 0))  # Green background
        pygame.draw.rect(self.screen, 'white', [400, 100, 100, 150], 0, 5)
        player_score = pygame.font.Font(None, 22).render(str(player_val), True, "black")
        self.screen.blit(player_score, (400,100))
        self.screen.blit(player_text, (50, 50))
        self.screen.blit(dealer_text, (50, 150))

    def display_result(self):
        """Display the game result on screen."""
        result = self.game.check_winner()
        result_text = self.font.render(result, True, (255, 255, 255))
        self.screen.blit(result_text, (50, 300))
        pygame.display.flip()
        pygame.time.wait(3000)
