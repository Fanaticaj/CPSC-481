import pygame
from StartScreen import *

pygame.display.set_caption("Player Select")

def player_select(selected_game):
    player_cash = get_player_cash()
    bet_amount = ""
    selected_mode = None
    
    input_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 50, 200, 32)
    color_active = pygame.Color('lightskyblue3')
    color_passive = pygame.Color('gray15')
    color = color_passive
    active = False

    def player_select_screen(selected_game, player_cash):
        bet_amount = ""
        selected_mode = None
        
        input_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 50, 200, 32)
        color_active = pygame.Color('lightskyblue3')
        color_passive = pygame.Color('gray15')
        color = color_passive
        active = False

        while True:
            screen.fill(BACKGROUND)
            
            # Draw Back button
            draw_button("Back", 10, 10, 80, 40, RED, WHITE)
            
            # Draw selected game
            game_text = font_large.render(selected_game, True, WHITE)
            game_rect = game_text.get_rect(center=(WIDTH // 2, 30))
            screen.blit(game_text, game_rect)
            
            # Draw Player Cash
            cash_text = f"Player Cash: ${player_cash}"
            cash_surface = font_small.render(cash_text, True, WHITE)
            screen.blit(cash_surface, (WIDTH - 150, 10))
            
            # Draw play options
            draw_button("AI Plays", WIDTH // 2 - 150, HEIGHT // 2 - 50, 140, 60, GREEN, BLACK)
            draw_button("Player Plays", WIDTH // 2 + 10, HEIGHT // 2 - 50, 140, 60, BLUE, BLACK)
            
            # Draw bet input field
            pygame.draw.rect(screen, color, input_rect)
            bet_surface = font_medium.render(bet_amount, True, WHITE)
            screen.blit(bet_surface, (input_rect.x + 5, input_rect.y + 5))
            
            # Draw bet button
            draw_button("Bet", WIDTH // 2 - 50, HEIGHT // 2 + 100, 100, 40, GREEN, BLACK)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if 10 <= mouse_pos[0] <= 90 and 10 <= mouse_pos[1] <= 50:
                        return "back"
                    elif WIDTH // 2 - 150 <= mouse_pos[0] <= WIDTH // 2 - 10 and HEIGHT // 2 - 50 <= mouse_pos[1] <= HEIGHT // 2 + 10:
                        selected_mode = "AI"
                    elif WIDTH // 2 + 10 <= mouse_pos[0] <= WIDTH // 2 + 150 and HEIGHT // 2 - 50 <= mouse_pos[1] <= HEIGHT // 2 + 10:
                        selected_mode = "Player"
                    elif WIDTH // 2 - 50 <= mouse_pos[0] <= WIDTH // 2 + 50 and HEIGHT // 2 + 100 <= mouse_pos[1] <= HEIGHT // 2 + 140:
                        if selected_mode and bet_amount:
                            try:
                                bet = int(bet_amount)
                                if 0 < bet <= player_cash:
                                    return selected_mode, bet
                                else:
                                    print("Invalid bet amount")
                            except ValueError:
                                print("Invalid bet amount")
                    if input_rect.collidepoint(event.pos):
                        active = not active
                    else:
                        active = False
                    color = color_active if active else color_passive
                if event.type == pygame.KEYDOWN:
                    if active:
                        if event.key == pygame.K_BACKSPACE:
                            bet_amount = bet_amount[:-1]
                        else:
                            bet_amount += event.unicode
            
            pygame.display.flip()

if __name__ == "__main__":
    result = player_select("Traditional Blackjack")
    print(f"Result: {result}")
