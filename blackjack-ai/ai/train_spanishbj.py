# train_spanishbj.py for Spanish Blackjack rules.
import logging
import random
from .q_table_spanish_manager import save_q_table_spanish_json
from player.player_game2 import PlayerSpanishBlackjack 
from .basic_strategy_spanishbj import initialize_state_action, choose_action, update_q_value, q_table
import pygame

logging.basicConfig(level=logging.INFO)

pygame.init()
screen = pygame.Surface((800, 600))  # Dummy screen for headless mode
player_spanish_blackjack = PlayerSpanishBlackjack(screen)

# Training parameters
episodes = 100000  # Number of episodes to train
print_interval = 10000  # Print progress every 10,000 episodes

# Training loop
for episode in range(episodes):
    # Create a new instance of the Spanish Blackjack game in non-graphical mode
    player_spanish_blackjack = PlayerSpanishBlackjack()

    # Initialize the game state
    player_spanish_blackjack.game.deal_card(player_spanish_blackjack.game.player_hand)  # Deal first card to player
    player_spanish_blackjack.game.deal_card(player_spanish_blackjack.game.player_hand)  # Deal second card to player
    player_hand = player_spanish_blackjack.game.player_hand  # Retrieve the player's hand after dealing
    player_spanish_blackjack.game.deal_card(player_spanish_blackjack.game.dealer_hand)  # Deal first card to dealer
    dealer_card = player_spanish_blackjack.game.dealer_hand[0]  # Retrieve dealer’s visible card
    # Check if player has a usable Ace
    player_total = player_spanish_blackjack.game.hand_value(player_hand)
    usable_ace = player_spanish_blackjack.game.has_usable_ace(player_hand)
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
            player_spanish_blackjack.game.deal_card(player_hand)
            player_total = player_spanish_blackjack.game.hand_value(player_hand)
            usable_ace = player_spanish_blackjack.game.has_usable_ace(player_hand)
            next_state = (player_total, dealer_card, usable_ace)

            # Check if player busts
            if player_spanish_blackjack.game.is_bust(player_hand):
                reward = -1
                done = True
                update_q_value(state, action, reward, None)  # Terminal update
                continue
            else:
                reward = 0

        elif action == "Stand":
            # Dealer's turn and determine game outcome
            dealer_total = player_spanish_blackjack.game.play_dealer_hand()  # Play dealer's hand to completion

            # Determine the game outcome
            if dealer_total > 21 or player_total > dealer_total:
                reward = 1  # Win
            elif player_total < dealer_total:
                reward = -1  # Loss
            else:
                reward = 0  # Draw
            done = True  # Game ends on Stand

            next_state = None  # Terminal state for the purpose of Q-learning

        # Update Q-value for the (state, action) pair
        update_q_value(state, action, reward, next_state)

        # Move to the next state
        state = next_state

    if (episode + 1) % print_interval == 0:
        print(f"Episode {episode + 1}/{episodes} completed")

print("Training completed. Q-table has been updated.")
save_q_table_spanish_json(q_table)
