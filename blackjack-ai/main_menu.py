import pygame, sys, os
from button import Button
from player.player_game1 import PlayerBlackjack
from player.player_game2 import PlayerSpanishBlackjack
from player.player_game3 import PlayerBlackjackSwitch
from player.player_game4 import PlayerEBlackjack

pygame.init()

SCREEN = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Blackjack Main menu")

BG = pygame.image.load("blackjack-ai\images\Background.png" if os.name == "nt" else "blackjack-ai/images/Background.png")

def get_font(size): 
    return pygame.font.Font(None, size)  # Placeholder for font loading

def play():
    while True:
        PLAY_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("black")

        PLAY_TEXT = get_font(45).render("Play Blackjack", True, "White")
        PLAY_RECT = PLAY_TEXT.get_rect(center=(640, 260))
        SCREEN.blit(PLAY_TEXT, PLAY_RECT)

        PLAY_BACK = Button(image=None, pos=(640, 460), 
                            text_input="BACK", font=get_font(75), base_color="White", hovering_color="Green")

        PLAY_BACK.changeColor(PLAY_MOUSE_POS)
        PLAY_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
                    main_menu()

        pygame.display.update()

def options():
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("blue")

        OPTIONS_TEXT = get_font(45).render("Other Blackjack Game", True, "Black")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(640, 260))
        SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)

        OPTIONS_BACK = Button(image=None, pos=(640, 460), 
                            text_input="BACK", font=get_font(75), base_color="Black", hovering_color="Green")

        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu()

        pygame.display.update()

def main_menu():
    while True:
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(100).render("Blackjack Main Menu", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))
        black_Jack1 = Button(image=None, pos=(340, 250), 
                            text_input="Blackjack", font=get_font(35), base_color="#d7fcd4", hovering_color="White")
        black_Jack2 = Button(image=None, pos=(940, 250), 
                            text_input="Spanish Blackjack", font=get_font(35), base_color="#d7fcd4", hovering_color="White")
        black_Jack3 = Button(image=None, pos=(940, 400), 
                            text_input="Blackjack Switch", font=get_font(35), base_color="#d7fcd4", hovering_color="White")
        black_Jack4 = Button(image=None, pos=(340, 400), 
                            text_input="European Blackjack", font=get_font(35), base_color="#d7fcd4", hovering_color="White")

        
        QUIT_BUTTON = Button(image=pygame.image.load( "blackjack-ai\images\Quit Rect.png" if os.name == "nt" else "blackjack-ai/images/Quit Rect.png"), pos=(640, 550), 
                            text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [black_Jack1, black_Jack2, QUIT_BUTTON, black_Jack4, black_Jack3]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if black_Jack1.checkForInput(MENU_MOUSE_POS):
                    if observe_mode() :
                        #print("OBSERVATION MODE")
                        player_blackjack = PlayerBlackjack(True, SCREEN)
                        player_blackjack.run()
                    else :
                        #print("PLAY MODE")
                        player_blackjack = PlayerBlackjack(False, SCREEN)
                        player_blackjack.run() 
                if black_Jack2.checkForInput(MENU_MOUSE_POS):
                    if observe_mode() :
                        player_blackjack_spanish = PlayerSpanishBlackjack(SCREEN)
                        player_blackjack_spanish.run()
                    else :
                        player_blackjack_spanish = PlayerSpanishBlackjack(SCREEN)
                        player_blackjack_spanish.run()
                if black_Jack3.checkForInput(MENU_MOUSE_POS):  # New logic for Blackjack Switch
                    if observe_mode() :
                        player_blackjack_switch = PlayerBlackjackSwitch(SCREEN)
                        player_blackjack_switch.run()
                    else :
                        player_blackjack_switch = PlayerBlackjackSwitch(SCREEN)
                        player_blackjack_switch.run()
                if black_Jack4.checkForInput(MENU_MOUSE_POS):  # New logic for Blackjack Switch
                    if observe_mode() :
                        player_blackjack_european = PlayerEBlackjack(SCREEN)
                        player_blackjack_european.run()
                    else : 
                        player_blackjack_european = PlayerEBlackjack(SCREEN)
                        player_blackjack_european.run()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()


# Function returns true if the player will play in Observer mode, watching the AI play for them.
def observe_mode():
    while True:
        PLAY_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("black")

        WATCH_BACK = Button(image=None, pos=(640, 260), 
                            text_input="WATCH BLACKJACK", font=get_font(75), base_color="White", hovering_color="Green")

        PLAY_BACK = Button(image=None, pos=(640, 460), 
                            text_input="PLAY BLACKJACK", font=get_font(75), base_color="White", hovering_color="Green")

        PLAY_BACK.changeColor(PLAY_MOUSE_POS)
        PLAY_BACK.update(SCREEN)
        WATCH_BACK.changeColor(PLAY_MOUSE_POS)
        WATCH_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
                    return False
                if WATCH_BACK.checkForInput(PLAY_MOUSE_POS):
                    return True


        pygame.display.update()


main_menu()
