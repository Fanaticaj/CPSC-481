import pygame
from games.game1 import Blackjack

class AIBlackjack:
    def __init__(self, screen):
        self.screen = screen
        self.game = Blackjack()
        self.font = pygame.font.Font(None, 36)

    def run(self):
        # Start a new game
        self.game.new_game()

        # AI plays as Dealer
        while self.game.hand_value(self.game.dealer_hand) < 17:
            self.game.deal_card(self.game.dealer_hand)

        # Render result
        self.display_result()

    def display_result(self):
        result = self.game.check_winner()
        result_text = self.font.render(result, True, (255, 255, 255))
        self.screen.fill((0, 100, 0))
        self.screen.blit(result_text, (50, 300))
        pygame.display.flip()
        pygame.time.wait(3000)
