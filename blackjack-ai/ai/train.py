# train.py for normal blackjack rules.
import logging
import random
from .q_table_manager import save_q_table_json
from player.player_game1 import PlayerBlackjack  
from .basic_strategy import initialize_state_action, choose_action, update_q_value, q_table
import pygame

logging.basicConfig(level=logging.INFO)

pygame.init()
screen = pygame.Surface((800, 600))  # Dummy screen for headless mode
player_blackjack = PlayerBlackjack(screen)
# Training parameters
episodes = 100000  # Number of episodes to train
print_interval = 10000  # Print progress every 10,000 episodes
wins, losses, draws = 0, 0, 0
# Training loop
for episode in range(episodes):
    # Create a new instance of the blackjack game in non-graphical mode
    player_blackjack = PlayerBlackjack()  

    # Initialize the game state
    player_blackjack.game.deal_card(player_blackjack.game.player_hand)  # Deal first card to player
    player_blackjack.game.deal_card(player_blackjack.game.player_hand)  # Deal second card to player
    player_hand = player_blackjack.game.player_hand  # Retrieve the player's hand after dealing
    player_blackjack.game.deal_card(player_blackjack.game.dealer_hand)  # Deal first card to dealer
    dealer_card = player_blackjack.game.dealer_hand[0]  # Retrieve dealer’s visible card
  # Check if player has a usable Ace
    player_total = player_blackjack.game.hand_value(player_hand)
    usable_ace = player_blackjack.game.has_usable_ace(player_hand)  
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
            if player_blackjack.game.is_bust(player_hand):
                reward = -1
                losses += 1
                done = True
                update_q_value(state, action, reward, None)  # Terminal update
                continue
            else:
                reward = 0

        elif action == "Stand":
            # Dealer's turn and determine game outcome
            dealer_total = player_blackjack.game.play_dealer_hand()  # Play dealer's hand to completion

            # Determine the game outcome
            if dealer_total > 21 or player_total > dealer_total:
                reward = 1  # Win
                wins += 1
            elif player_total < dealer_total:
                reward = -1  # Loss
                losses += 1
            else:
                reward = 0  # Draw
                draws += 1
            done = True  # Game ends on Stand

            next_state = None  # Terminal state for the purpose of Q-learning
        
        elif action == "Double":
            # Player doubles down: hits once and then stands
            player_blackjack.game.double_down(player_hand)
            player_total = player_blackjack.game.hand_value(player_hand)
            next_state = (player_total, dealer_card, player_blackjack.game.has_usable_ace(player_hand))

            # Check if player busts after doubling down
            if player_blackjack.game.is_bust(player_hand):
                reward = -1  # Immediate loss
            else:
                # Dealer plays their hand
                dealer_total = player_blackjack.game.play_dealer_hand()
                if dealer_total > 21 or player_total > dealer_total:
                    reward = 1  # Player wins
                    wins += 1
                elif player_total < dealer_total:
                    reward = -1  # Player loses
                    losses += 1
                else:
                    reward = 0  # Draw
                    draws += 1

            done = True  # Player must stand after doubling down

            # Update Q-value for "Double"
            update_q_value(state, action, reward, next_state)
            continue

        elif action == "Split":
            # Player splits their hand into two separate hands
            logging.info(f"Splitting hand: {player_hand}")
            hand1, hand2 = player_blackjack.game.split_hand(player_hand)
            for i, hand in enumerate([hand1, hand2], start=1):
                logging.info(f"Processing split hand {i}: {hand}")

            for hand in [hand1, hand2]:
                player_total = player_blackjack.game.hand_value(hand)
                usable_ace = player_blackjack.game.has_usable_ace(hand)
                split_state = (player_total, dealer_card, usable_ace)
                if split_state is not None:
                    initialize_state_action(split_state)

                split_done = False
                while not split_done:
                    if split_state is None:
                        break
                    split_action = choose_action(split_state)

                    if split_action == "Hit":
                        player_blackjack.game.deal_card(hand)
                        player_total = player_blackjack.game.hand_value(hand)
                        usable_ace = player_blackjack.game.has_usable_ace(hand)
                        next_split_state = (player_total, dealer_card, usable_ace)

                        if player_blackjack.game.is_bust(hand):
                            reward = -1  # Immediate loss
                            losses += 1
                            split_done = True
                            update_q_value(split_state, split_action, reward, None)
                            continue
                        else:
                            reward = 0
                    elif split_action == "Stand":
                        dealer_total = player_blackjack.game.play_dealer_hand()
                        if dealer_total > 21 or player_total > dealer_total:
                            reward = 1  # Player wins
                            wins += 1
                        elif player_total < dealer_total:
                            reward = -1  # Player loses
                            losses += 1
                        else:
                            reward = 0  # Draw
                            draws += 1
                        split_done = True
                        next_split_state = None
                    
                    update_q_value(split_state, split_action, reward, next_split_state)
                    split_state = next_split_state
            break

        # Update Q-value for the (state, action) pair
        update_q_value(state, action, reward, next_state if action != "Split" else None)

        # Move to the next state
        state = next_state

    if (episode + 1) % print_interval == 0:
        total_games = wins + losses + draws
        print(f"Episode {episode + 1}/{episodes} completed")
        win_rate = wins / (wins + losses + draws)
        loss_rate = losses / (wins + losses + draws)
        draw_rate = draws / (wins + losses + draws)
        print(f"Episode {episode + 1}/{episodes} completed")
        print(f"Win Rate: {win_rate:.2%}, Loss Rate: {loss_rate:.2%}, Draw Rate: {draw_rate:.2%}")


print("Training completed. Q-table has been updated.")
save_q_table_json(q_table)
