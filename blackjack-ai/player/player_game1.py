import pygame
from games.game1 import Blackjack

class PlayerBlackjack:
    def __init__(self, screen):
        self.screen = screen
        self.game = Blackjack()
        self.font = pygame.font.Font(None, 36)

    def run(self):
        self.game.new_game()

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Handle player input for hitting or standing
            keys = pygame.key.get_pressed()
            if keys[pygame.K_h]:  # Player chooses to "Hit"
                self.game.deal_card(self.game.player_hand)
                if self.game.hand_value(self.game.player_hand) > 21:
                    running = False  # Player busts, end game
            elif keys[pygame.K_s]:  # Player chooses to "Stand"
                running = False  # End player's turn, proceed to check winner
            elif keys[pygame.K_d]: # Player chooses to "Double Down"
                if len(self.game.player_hand) == 2:  # Can only double on first two cards
                    self.game.deal_card(self.game.player_hand)
                    running = False  # End player's turn after doubling
                else:
                    # Optionally, display a message that doubling is not allowed
                    pass

            # Display the game state
            self.display_game_state()

            pygame.display.flip()

        # After the loop ends, display the game result
        self.display_result()

    def display_game_state(self):
        player_val = self.game.hand_value(self.game.player_hand)
        dealer_val = self.game.hand_value(self.game.dealer_hand[:1])  # Dealer shows only one card

        player_text = self.font.render(f"Player Hand: {player_val}", True, (255, 255, 255))
        dealer_text = self.font.render(f"Dealer Hand: {dealer_val}", True, (255, 255, 255))

        self.screen.fill((0, 100, 0))  # Green background
        self.screen.blit(player_text, (50, 50))
        self.screen.blit(dealer_text, (50, 150))

    def display_result(self):
        result = self.game.check_winner()
        result_text = self.font.render(result, True, (255, 255, 255))
        self.screen.blit(result_text, (50, 300))
        pygame.display.flip()
        pygame.time.wait(3000)
