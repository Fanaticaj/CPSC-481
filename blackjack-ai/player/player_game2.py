import pygame
from games.game2 import SpanishBlackjack

class PlayerBlackjack:
    def __init__(self, screen):
        self.screen = screen
        self.game = SpanishBlackjack() 
        self.font = pygame.font.Font(None, 36)

    def run(self):
        self.game.new_game()

        running = True
        player_turn = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            if player_turn:
                # Handle player input for hitting or standing
                keys = pygame.key.get_pressed()
                if keys[pygame.K_h]:  # Player chooses to "Hit"
                    self.game.deal_card(self.game.player_hand)
                    if self.game.hand_value(self.game.player_hand) > 21:
                        running = False  # Player busts, end game
                        break
                    # Check for special payouts in Spanish 21
                    special_payout = self.game.check_special_payout(self.game.player_hand)
                    if special_payout:
                        self.display_special_payout(special_payout)
                        running = False
                        break
                elif keys[pygame.K_s]:  # Player chooses to "Stand"
                    player_turn = False  # End player's turn, dealer plays next

            if not player_turn:  # Dealer's turn
                self.dealer_turn()
                running = False  # End the game after dealer's turn

            # Display the game state
            self.display_game_state()

            pygame.display.flip()

        # After the loop ends, display the game result
        self.display_result()

    def dealer_turn(self):
        # Dealer hits until the value of the hand is at least 17
        while self.game.hand_value(self.game.dealer_hand) < 17:
            self.game.deal_card(self.game.dealer_hand)

    def display_game_state(self):
        player_val = self.game.hand_value(self.game.player_hand)
        dealer_val = self.game.hand_value(self.game.dealer_hand[:1])  # Dealer shows only one card

        player_text = self.font.render(f"Player Hand: {player_val}", True, (255, 255, 255))
        dealer_text = self.font.render(f"Dealer Hand: {dealer_val}", True, (255, 255, 255))

        self.screen.fill((0, 100, 0))  # Green background
        self.screen.blit(player_text, (50, 50))
        self.screen.blit(dealer_text, (50, 150))

    def display_special_payout(self, message):
        result_text = self.font.render(message, True, (255, 255, 255))
        self.screen.fill((0, 100, 0))  # Refill the screen before displaying result
        self.screen.blit(result_text, (50, 300))
        pygame.display.flip()
        pygame.time.wait(3000)

    def display_result(self):
        result = self.game.check_winner()  # Check who wins based on final hands
        result_text = self.font.render(result, True, (255, 255, 255))
        self.screen.fill((0, 100, 0))  # Refill the screen before displaying result
        self.screen.blit(result_text, (50, 300))
        pygame.display.flip()
        pygame.time.wait(3000)
