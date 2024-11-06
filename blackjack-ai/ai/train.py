# train.py

import random
from .q_table_manager import save_q_table_json
from player.player_game1 import PlayerBlackjack  # Import the PlayerBlackjack class
from .basic_strategy import initialize_state_action, choose_action, update_q_value, q_table
import pygame
pygame.init()
screen = pygame.Surface((800, 600))  # Dummy screen for headless mode
player_blackjack = PlayerBlackjack(screen)
# Training parameters
episodes = 100000  # Number of episodes to train
print_interval = 10000  # Print progress every 10,000 episodes

# Training loop
for episode in range(episodes):
    # Create a new instance of the blackjack game in non-graphical mode
    player_blackjack = PlayerBlackjack()  # Assuming this instance can run headlessly for training

    # Initialize the game state
    player_blackjack.game.deal_card(player_blackjack.game.player_hand)  # Deal first card to player
    player_blackjack.game.deal_card(player_blackjack.game.player_hand)  # Deal second card to player
    player_hand = player_blackjack.game.player_hand  # Retrieve the player's hand after dealing
    player_blackjack.game.deal_card(player_blackjack.game.dealer_hand)  # Deal first card to dealer
    dealer_card = player_blackjack.game.dealer_hand[0]  # Retrieve dealer’s visible card
  # Check if player has a usable Ace
    player_total = player_blackjack.game.hand_value(player_hand)
    usable_ace = player_blackjack.game.has_usable_ace(player_hand)  # Assuming `has_usable_ace` exists in `Blackjack`
    state = (player_total, dealer_card, usable_ace)

    # Initialize Q-values for the state if not already present
    initialize_state_action(state)

    done = False  # To track if the game is over
    while not done:
        # Choose an action (Hit or Stand) based on epsilon-greedy policy and basic strategy
        action = choose_action(state)

        # Execute the chosen action
        if action == "Hit":
            # Player takes a hit
            player_blackjack.game.deal_card(player_hand)
            player_total = player_blackjack.game.hand_value(player_hand)
            usable_ace = player_blackjack.game.has_usable_ace(player_hand)
            next_state = (player_total, dealer_card, usable_ace)

            # Check if player busts
            if player_blackjack.game.is_bust(player_hand):  # Assuming this method checks for bust
                reward = -1  # Loss
                done = True
            else:
                reward = 0  # Game continues

        elif action == "Stand":
            # Dealer's turn and determine game outcome
            dealer_total = player_blackjack.game.play_dealer_hand()  # Play dealer's hand to completion

            # Determine the game outcome
            if dealer_total > 21 or player_total > dealer_total:
                reward = 1  # Win
            elif player_total < dealer_total:
                reward = -1  # Loss
            else:
                reward = 0  # Draw
            done = True  # Game ends on Stand

            next_state = state  # Terminal state for the purpose of Q-learning

        # Update Q-value for the (state, action) pair
        update_q_value(state, action, reward, next_state)

        # Move to the next state
        state = next_state

    # Optional: Print progress every few episodes
    if (episode + 1) % print_interval == 0:
        print(f"Episode {episode + 1}/{episodes} completed")

# Training complete
print("Training completed. Q-table has been updated.")
save_q_table_json(q_table)
