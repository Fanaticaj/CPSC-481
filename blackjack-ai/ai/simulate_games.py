import logging
from player.player_game1 import PlayerBlackjack
from .basic_strategy import initialize_state_action, choose_action, update_q_value
from .train import simulate_split_hand  # Assuming simulate_split_hand is defined in train.py

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def simulate_debug_games(num_games=10):
    """Simulate a small number of games with detailed logging to debug behavior."""
    for game_num in range(1, num_games + 1):
        print(f"\n--- Starting Game {game_num} ---")
        player_blackjack = PlayerBlackjack()
        
        # Initialize player and dealer hands
        player_blackjack.game.deal_card(player_blackjack.game.player_hand)
        player_blackjack.game.deal_card(player_blackjack.game.player_hand)
        player_hand = player_blackjack.game.player_hand
        player_blackjack.game.deal_card(player_blackjack.game.dealer_hand)
        player_blackjack.game.deal_card(player_blackjack.game.dealer_hand)
        dealer_hand = player_blackjack.game.dealer_hand
        dealer_card = player_blackjack.game.dealer_hand[0]

        # Calculate initial state
        player_total = player_blackjack.game.hand_value(player_hand)
        dealer_hand = player_blackjack.game.hand_value(dealer_hand)
        usable_ace = player_blackjack.game.has_usable_ace(player_hand)
        state = (player_total, dealer_card, usable_ace)
        initialize_state_action(state)  # Initialize Q-table for this state
        done = False

        while not done:
            print(f"Player Hand: {player_hand} | Dealer Card: {dealer_card}")
            action = choose_action(state, player_hand)  # Use Q-learning policy to choose action
            print(f"Action Chosen: {action}")
            
            next_state = None  # Placeholder for next state
            reward = 0  # Initialize reward

            if action == "Hit":
                player_blackjack.game.deal_card(player_hand)
                player_total = player_blackjack.game.hand_value(player_hand)
                usable_ace = player_blackjack.game.has_usable_ace(player_hand)
                next_state = (player_total, dealer_card, usable_ace)

                if player_blackjack.game.is_bust(player_hand):
                    print("Player Busts!")
                    reward = -1
                    done = True
            
            elif action == "Stand":
                print("Player Stands. Dealer's turn.")
                player_total = player_blackjack.game.hand_value(player_hand)
                dealer_total = player_blackjack.game.play_dealer_hand()
                print(f"Dealer Hand: {dealer_hand} | Dealer Total: {dealer_total}")
                
                if player_blackjack.game.is_bust(dealer_hand):
                    print("Dealer Busts! Player Wins!")
                    reward = 1
                elif player_total > dealer_total:
                    print("Player Wins!")
                    reward = 1
                elif player_total < dealer_total:
                    print("Dealer Wins!")
                    reward = -1
                else:
                    print("It's a Draw!")
                    reward = 0
                done = True

            elif action == "Double":
                print("Player Doubles Down.")
                player_blackjack.game.double_down(player_hand)
                next_state = None  # No further actions after doubling
                reward = 1 if player_blackjack.game.hand_value(player_hand) > dealer_total else -1
                done = True
            
            elif action == "Split":
                try:
        # Pre-check before attempting to split
                    if len(player_hand) == 2 and player_hand[0][0] == player_hand[1][0]:
                        print(f"Splitting Hand: {player_hand}")
                        hand1, hand2 = player_blackjack.game.split_hand(player_hand)
                        for split_hand in [hand1, hand2]:
                            print(f"Processing split hand: {split_hand}")
                            player_total = player_blackjack.game.hand_value(split_hand)
                            split_state = (player_total, dealer_card, player_blackjack.game.has_usable_ace(split_hand))
                            simulate_split_hand(split_state, split_hand, dealer_card, player_blackjack)
                    else:
                        logging.warning(f"Cannot split invalid hand: {player_hand}")
                        raise ValueError(f"Invalid hand attempted for split: {player_hand}")
                except ValueError as e:
                    print(f"Error during split: {e}")
                done = True

            # Update Q-table after each action
            update_q_value(state, action, reward, next_state)
            
            if next_state:
                state = next_state

        print(f"Game {game_num} Result: Player Hand: {player_hand}, Dealer Hand: {dealer_hand}")
        print(f"Final Outcome: {player_blackjack.game.check_winner()}")

if __name__ == "__main__":
    simulate_debug_games(10)