import pygame
from games.game4 import EBlackjack

class PlayerEBlackjack:
    def __init__(self, screen):
        self.screen = screen
        self.game = EBlackjack()
        self.font = pygame.font.Font(None, 36)

    def run(self):
        # Start a new game
        self.game.new_game()

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Render game state
            self.screen.fill((0, 100, 0))  # Green table background
            self.display_game_state()

            # Handle Player Input
            keys = pygame.key.get_pressed()
            if keys[pygame.K_h]:  # Player chooses to "Hit"
                self.game.deal_card(self.game.player_hand)
                self.game.deal_card(self.game.dealer_hand)
                if self.game.hand_value(self.game.player_hand) > 21:
                    running = False
            elif keys[pygame.K_s]:  # Player chooses to "Stand"
                self.game.deal_card(self.game.dealer_hand)
                running = False

            pygame.display.flip()

        # After exiting the loop, display result
        self.display_result()

    def display_game_state(self):
        # Display player and dealer hands and values
        player_val = self.game.hand_value(self.game.player_hand)
        dealer_val = self.game.hand_value(self.game.dealer_hand[:1])  # Dealer shows only one card

        player_text = self.font.render(f"Player Hand: {player_val}", True, (255, 255, 255))
        dealer_text = self.font.render(f"Dealer Hand: {dealer_val}", True, (255, 255, 255))

        self.screen.blit(player_text, (50, 50))
        self.screen.blit(dealer_text, (50, 150))

    def display_result(self):
        result = self.game.check_winner()
        result_text = self.font.render(result, True, (255, 255, 255))
        self.screen.blit(result_text, (50, 300))
        pygame.display.flip()
        pygame.time.wait(3000)
