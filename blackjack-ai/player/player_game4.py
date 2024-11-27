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

            # Handle Player Input
            keys = pygame.key.get_pressed()
            if keys[pygame.K_h]:  # Player chooses to "Hit"
                pygame.time.wait(100) # Without this it keeps on hitting every single frame, instead of just once
                self.game.deal_card(self.game.player_hand)
                # self.game.deal_card(self.game.dealer_hand)
                if self.game.hand_value(self.game.player_hand) > 21:
                    running = False
            elif keys[pygame.K_s]:  # Player chooses to "Stand"
                self.game.play_dealer_hand()
                running = False
            
            # Render game state
            self.screen.fill((0, 100, 0))  # Green table background
            self.display_game_state()

            pygame.display.flip()

        # After exiting the loop, display result
        self.display_result()

    def display_game_state(self):
        player_x_position = 400
        player_y_position = 100
        dealer_x_position = 400
        dealer_y_position = 400
        # Display player and dealer hands and values
        player_val = self.game.hand_value(self.game.player_hand)
        dealer_val = self.game.hand_value(self.game.dealer_hand)  # Dealer shows only one card

        player_text = self.font.render(f"Player Hand: {player_val}", True, (255, 255, 255))
        dealer_text = self.font.render(f"Dealer Hand: {dealer_val}", True, (255, 255, 255))

        self.screen.blit(player_text, (50, 100))
        self.screen.blit(dealer_text, (50, 400))
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
        
        for i in self.game.dealer_hand:
                dealer_score = pygame.font.Font(None, 30).render(str(i[0]), True, "black")
                pygame.draw.rect(self.screen, 'white', [dealer_x_position, dealer_y_position, 100, 150], 0, 5)
                # Draw the text inside the rectangle
                top_left_text_position = (dealer_x_position + 10, dealer_y_position + 10)
                bottom_right_text_position = (dealer_x_position + 70, dealer_y_position + 120)
                self.screen.blit(dealer_score, top_left_text_position)
                self.screen.blit(dealer_score, bottom_right_text_position)
                dealer_x_position += 110  # Add spacing between cards
                dealer_val = self.game.hand_value(self.game.dealer_hand)
                dealer_text = self.font.render(f"Dealer Hand: {dealer_val}", True, (255, 255, 255))
                self.screen.blit(dealer_text, (50, 400))


    def display_result(self):
        result = self.game.check_winner()
        result_text = self.font.render(result, True, (255, 255, 255))
        self.screen.blit(result_text, (50, 300))
        pygame.display.flip()
        pygame.time.wait(3000)
