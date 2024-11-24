# train.py for normal blackjack rules.
import logging
import random
from .q_table_manager import save_q_table_json
from player.player_game1 import PlayerBlackjack  
from .basic_strategy import initialize_state_action, choose_action, update_q_value, q_table, min_epsilon, epsilon_decay
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
    # Initialize a new game instance
    player_blackjack = PlayerBlackjack()  
    game = player_blackjack.game

    # Deal initial cards to player and dealer
    game.deal_card(game.player_hand)
    game.deal_card(game.dealer_hand)
    game.deal_card(game.player_hand)
    game.deal_card(game.dealer_hand)
    logging.info(f"Player's initial hand: {game.player_hand}, Total: {game.hand_value(game.player_hand)}")

    # Initial state
    player_total = game.hand_value(game.player_hand)
    dealer_total = game.hand_value(game.dealer_hand)

    if player_total == 21:
        if dealer_total == 21:
            reward = 0  # Draw
            draws += 1
            logging.info("Both Player and Dealer have Blackjack. It's a Draw!")
        else:
            reward = 1  # Player Wins
            wins += 1
            logging.info("Player has a Natural Blackjack! Player Wins.")
        state = (player_total, game.dealer_hand[0], game.has_usable_ace(game.player_hand))
        initialize_state_action(state)  # Fix: Ensure state is in the Q-table
        update_q_value(state, "Stand", reward, None)
        continue  # Move to the next episode


    if dealer_total == 21:
        reward = -1  # Dealer Wins
        losses += 1
        logging.info("Dealer has a Natural Blackjack! Dealer Wins.")
        state = (player_total, game.dealer_hand[0], game.has_usable_ace(game.player_hand))
        initialize_state_action(state)  # Fix: Ensure state is in the Q-table
        update_q_value(state, "Stand", reward, None)
        continue  # Move to the next episode
    # Initial state
    player_total = game.hand_value(game.player_hand)
    dealer_card = game.dealer_hand[0]
    usable_ace = game.has_usable_ace(game.player_hand)
    state = (player_total, dealer_card, usable_ace)

    # Initialize Q-values for the state
    initialize_state_action(state)

    done = False
    while not done:
        # Choose an action
        action = choose_action(state, game.player_hand)

        # Execute action
        if action == "Hit":
            result = game.hit(game.player_hand)
            player_total = result["total"]
            usable_ace = game.has_usable_ace(game.player_hand)
            next_state = (player_total, dealer_card, usable_ace)

            if result["bust"]:
                reward = -1  # Loss
                losses += 1
                done = True
                update_q_value(state, action, reward, None)
                break
            else:
                reward = 0
                update_q_value(state, action, reward, next_state)
            state = next_state

        elif action == "Stand":
            result = game.stand(game.player_hand)
            reward = 1 if "Player Wins" in result else -1 if "Dealer Wins" in result else 0
            if reward == 1:
                wins += 1
            elif reward == -1:
                losses += 1
            else:
                draws += 1
            done = True
            update_q_value(state, action, reward, None)

        elif action == "Double":
            result = game.double(game.player_hand, 10)  # Assuming bet of 10
            player_total = result["total"]
            next_state = (player_total, dealer_card, game.has_usable_ace(game.player_hand))

            if result["bust"]:
                reward = -1  # Loss
                losses += 1
                done = True
            else:
                dealer_total = game.play_dealer_hand()
                if dealer_total > 21 or player_total > dealer_total:
                    reward = 1
                    wins += 1
                elif player_total < dealer_total:
                    reward = -1
                    losses += 1
                else:
                    reward = 0
                    draws += 1
                done = True

            update_q_value(state, action, reward, next_state)
            state = next_state

        elif action == "Split":
            if not game.can_split(game.player_hand):
                logging.warning("Invalid split action. Skipping turn.")
                done = True
                continue

            result = game.split(game.player_hand, 10)  # Assuming bet of 10
            if not result["success"]:
                logging.warning("Split failed.")
                done = True
                continue

            hand1, hand2 = result["hand1"], result["hand2"]
            for split_hand in [hand1, hand2]:
                split_done = False
                while not split_done:
                    split_total = game.hand_value(split_hand)
                    split_usable_ace = game.has_usable_ace(split_hand)
                    split_state = (split_total, dealer_card, split_usable_ace)
                    initialize_state_action(split_state)

                    split_action = choose_action(split_state, split_hand)
                    if split_action == "Hit":
                        split_result = game.hit(split_hand)
                        if split_result["bust"]:
                            reward = -1
                            losses += 1
                            split_done = True
                        else:
                            reward = 0
                        update_q_value(split_state, split_action, reward, None)

                    elif split_action == "Stand":
                        dealer_total = game.play_dealer_hand()
                        if dealer_total > 21 or split_total > dealer_total:
                            reward = 1
                            wins += 1
                        elif split_total < dealer_total:
                            reward = -1
                            losses += 1
                        else:
                            reward = 0
                            draws += 1
                        split_done = True
                        update_q_value(split_state, split_action, reward, None)

                    elif split_action == "Double":
                        split_result = game.double(split_hand, 10)
                        if split_result["bust"]:
                            reward = -1
                            losses += 1
                        else:
                            dealer_total = game.play_dealer_hand()
                            if dealer_total > 21 or split_total > dealer_total:
                                reward = 1
                                wins += 1
                            elif split_total < dealer_total:
                                reward = -1
                                losses += 1
                            else:
                                reward = 0
                                draws += 1
                        split_done = True
                        update_q_value(split_state, split_action, reward, None)

    if (episode + 1) % print_interval == 0:
        total_games = wins + losses + draws
        print(f"Episode {episode + 1}/{episodes} completed")
        print(f"Wins: {wins}, Losses: {losses}, Draws: {draws}")
        print(f"Total Games: {total_games}, Win Rate: {wins / total_games}")

print("Training completed. Saving Q-table...")
save_q_table_json(q_table)

