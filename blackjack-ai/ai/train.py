# train.py for normal blackjack rules.
import logging
import random
from .q_table_manager import save_q_table_json
from player.player_game1 import PlayerBlackjack  
from .basic_strategy import initialize_state_action, choose_action, update_q_value, q_table, get_state
import pygame
logging.basicConfig(level=logging.INFO)

pygame.init()
screen = pygame.Surface((800, 600))  # Dummy screen for headless mode
player_blackjack = PlayerBlackjack(screen)

# Training parameters
episodes = 100000  # Number of episodes to train
print_interval = 1000  # Print progress every 10,000 episodes
wins, losses, draws = 0, 0, 0

# Action-specific statistics
action_stats = {
    "Hit": {"wins": 0, "losses": 0, "draws": 0},
    "Stand": {"wins": 0, "losses": 0, "draws": 0},
    "Double": {"wins": 0, "losses": 0, "draws": 0},
    "Split": {"wins": 0, "losses": 0, "draws": 0},
}

# Dealer and player bust rates
dealer_busts, player_busts = 0, 0

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
            action_stats["Stand"]["draws"] += 1
            logging.info("Both Player and Dealer have Blackjack. It's a Draw!")
        else:
            reward = 1  # Player Wins
            wins += 1
            action_stats["Stand"]["wins"] += 1
            logging.info("Player has a Natural Blackjack! Player Wins.")
        state = (player_total, game.dealer_hand[0], game.has_usable_ace(game.player_hand))
        initialize_state_action(state)  # Fix: Ensure state is in the Q-table
        update_q_value(state, "Stand", reward, None)
        continue  # Move to the next episode


    if dealer_total == 21:
        reward = -1  # Dealer Wins
        losses += 1
        action_stats["Stand"]["losses"] += 1
        logging.info("Dealer has a Natural Blackjack! Dealer Wins.")
        state = (player_total, game.dealer_hand[0], game.has_usable_ace(game.player_hand))
        initialize_state_action(state)  # Fix: Ensure state is in the Q-table
        update_q_value(state, "Stand", reward, None)
        continue  # Move to the next episode
    # Initial state
    player_total = game.hand_value(game.player_hand)
    dealer_card = game.dealer_hand[0]
    usable_ace = game.has_usable_ace(game.player_hand)
    state = get_state(game.player_hand, game.dealer_hand[0], usable_ace)
    
    # Initialize Q-values for the state
    initialize_state_action(state)

    done = False
    while not done:
        
        player_total = game.hand_value(game.player_hand)
        dealer_card = game.dealer_hand[0]
        usable_ace = game.has_usable_ace(game.player_hand)
        state = get_state(game.player_hand, dealer_card, usable_ace)

        # Default available actions
        available_actions = ["Hit", "Stand"]

        # Add "Double" and "Split" if conditions are met
        if len(game.player_hand) == 2:  # Only allow these actions with exactly two cards
            available_actions.append("Double")
            if game.can_split(game.player_hand):
                available_actions.append("Split")

        # Choose an action
        action = choose_action(state, game.player_hand, available_actions)

        # Execute action
        if action == "Hit":
            result = game.hit(game.player_hand)
            player_total = result["total"]
            usable_ace = game.has_usable_ace(game.player_hand)
            next_state = get_state(game.player_hand, game.dealer_hand[0], usable_ace)

            if result["bust"]:
                player_busts += 1
                reward = -1  # Loss
                losses += 1
                action_stats["Hit"]["losses"] += 1
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
                action_stats["Stand"]["wins"] += 1
            elif reward == -1:
                losses += 1
                action_stats["Stand"]["losses"] += 1
            else:
                draws += 1
                action_stats["Stand"]["draws"] += 1
            done = True
            update_q_value(state, action, reward, None)

        elif action == "Double":
            result = game.double(game.player_hand, 10)  # Assuming bet of 10
            player_total = result["total"]
            next_state = (player_total, dealer_card, game.has_usable_ace(game.player_hand))
            
            if player_total in [10, 11]:
                reward = 0.1  # Reward for doubling with a strong total
            else:
                reward = 0  # Neutral reward for other totals

            if result["bust"]:
                reward = -1  # Loss
                losses += 1
                action_stats["Double"]["losses"] += 1
                player_busts += 1
                done = True
            else:
                dealer_total = game.play_dealer_hand()
                if dealer_total > 21:
                    dealer_busts += 1
                    reward = 1
                    wins += 1
                    action_stats["Double"]["wins"] += 1
                elif player_total > dealer_total:
                    reward = 1
                    wins += 1
                    action_stats["Double"]["wins"] += 1
                elif player_total < dealer_total:
                    reward = -1
                    losses += 1
                    action_stats["Double"]["losses"] += 1
                else:
                    reward = 0
                    draws += 1
                    action_stats["Double"]["draws"] += 1
                done = True

            update_q_value(state, action, reward, next_state)
            state = next_state

        elif action == "Split":
            if not game.can_split(game.player_hand):
                logging.warning("Invalid split action. Counting as a loss.")
                reward = -1
                losses += 1
                update_q_value(state, action, reward, None)
                done = True
                continue

            # Perform split
            result = game.split(game.player_hand, 10)  # Assuming bet of 10

            if not result["success"]:
                logging.warning("Split action failed.")
                reward = -1  # Treat failed splits as losses
                losses += 1
                update_q_value(state, action, reward, None)
                done = True
                continue

            hand1, hand2 = result["hand1"], result["hand2"]

            for split_hand in [hand1, hand2]:
                split_done = False
                while not split_done:
                    # Get the state of the current split hand
                    split_total = game.hand_value(split_hand)
                    split_usable_ace = game.has_usable_ace(split_hand)
                    split_state = get_state(split_hand, game.dealer_hand[0], split_usable_ace)
                    initialize_state_action(split_state)

                    # Determine available actions for the split hand
                    split_available_actions = ["Hit", "Stand"]
                    if len(split_hand) == 2:
                        split_available_actions.append("Double")
                        if game.can_split(split_hand):
                            split_available_actions.append("Split")

                    # Choose an action for the split hand
                    split_action = choose_action(split_state, split_hand, split_available_actions)

                    # Execute the chosen action
                    if split_action == "Hit":
                        split_result = game.hit(split_hand)
                        if split_result["bust"]:
                            reward = -1
                            losses += 1
                            action_stats["Split"]["losses"] += 1
                            result["win"] = False  # Update split result
                            split_done = True
                        else:
                            reward = 0
                        update_q_value(split_state, split_action, reward, None)

                    elif split_action == "Stand":
                        dealer_total = game.play_dealer_hand()
                        if dealer_total > 21:
                            reward = 1
                            wins += 1
                            action_stats["Split"]["wins"] += 1
                            result["win"] = True  # Update split result
                        elif split_total > dealer_total:
                            reward = 1
                            wins += 1
                            result["win"] = True  # Update split result
                            action_stats["Split"]["wins"] += 1
                        elif split_total < dealer_total:
                            reward = -1
                            losses += 1
                            action_stats["Split"]["losses"] += 1
                            result["win"] = False
                        else:
                            reward = 0
                            draws += 1
                            action_stats["Split"]["draws"] += 1
                            result["win"] = None  # Draw
                        split_done = True
                        update_q_value(split_state, split_action, reward, None)

                    elif split_action == "Double":
                        split_result = game.double(split_hand, 10)
                        if split_result["bust"]:
                            reward = -1
                            losses += 1
                            action_stats["Double"]["losses"] += 1
                            result["win"] = False
                        else:
                            dealer_total = game.play_dealer_hand()
                            if dealer_total > 21:
                                reward = 1
                                wins += 1
                                action_stats["Double"]["wins"] += 1
                                result["win"] = True
                            elif split_total > dealer_total:
                                reward = 1
                                wins += 1
                                action_stats["Double"]["wins"] += 1
                                result["win"] = True
                            elif split_total < dealer_total:
                                reward = -1
                                losses += 1
                                action_stats["Double"]["losses"] += 1
                                result["win"] = False
                            else:
                                reward = 0
                                draws += 1
                                action_stats["Double"]["draws"] += 1
                                result["win"] = None
                        split_done = True
                        update_q_value(split_state, split_action, reward, None)

    # End the main loop for this episode after processing both hands
    done = True


    
# Final summary
total_games = wins + losses + draws
print("Training completed. Final Results:")
print("-----------------------------------")
print(f"Total Games Played: {total_games}")
print(f"Wins: {wins}, Losses: {losses}, Draws: {draws}")
print(f"Win Rate: {wins / total_games:.2%}")
print("\nAction Statistics:")
for action, stats in action_stats.items():
    print(f"  - {action}: Wins: {stats['wins']}, Losses: {stats['losses']}, Draws: {stats['draws']}")

# Print dealer and player bust rates
print(f"\nDealer Bust Rate: {dealer_busts / total_games:.2%}")
print(f"Player Bust Rate: {player_busts / total_games:.2%}")

# Add Action Success Rates
print("\nAction Success Rates:")
for action, stats in action_stats.items():
    total = stats["wins"] + stats["losses"] + stats["draws"]
    success_rate = stats["wins"] / total if total > 0 else 0
    print(f"  - {action}: Success Rate: {success_rate:.2%}")

# Save Q-table to file
save_q_table_json(q_table)

