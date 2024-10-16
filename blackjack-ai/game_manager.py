from games import game1, game2, game3, game4
from ai import ai_game1, ai_game2, ai_game3, ai_game4
from player import player_game1, player_game2, player_game3, player_game4

class GameManager:
    def __init__(self):
        # Store available games and modes (AI or Player)
        self.games = {
            1: game1, 
            2: game2,
            3: game3,
            4: game4
        }

    def show_start_screen(self, screen):
        # Code to display and manage game selection on the start screen
        pass

    def start_game(self, game_choice, mode):
        # Load the selected game and mode (Player or AI)
        if mode == 'player':
            self.load_player_game(game_choice)
        elif mode == 'ai':
            self.load_ai_game(game_choice)

    def load_player_game(self, game_choice):
        # Load player-controlled version of the selected game
        if game_choice == 1:
            player_game1.run()
        elif game_choice == 2:
            player_game2.run()
        # Continue for other games...

    def load_ai_game(self, game_choice):
        # Load AI-controlled version of the selected game
        if game_choice == 1:
            ai_game1.run()
        elif game_choice == 2:
            ai_game2.run()
        # Continue for other games...
