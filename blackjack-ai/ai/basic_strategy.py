import random
import logging

alpha = 0.05 # Learning Rate
gamma = 0.95 # Discount Factor
epsilon = 0.9  # Start with high exploration
min_epsilon = 0.01  # Minimum exploration rate
decay_rate = 0.995  # Decay factor

# In each training loop iteration
epsilon = max(min_epsilon, epsilon * decay_rate)


actions = ["Hit", "Stand", "Double", "Split"] 
random_actions = ["Hit", "Stand", "Double"]
q_table = {}

basic_strategy_q_table = {
    # Hard Totals
    (4, 2): 'H', (4, 3): 'H', (4, 4): 'H', (4, 5): 'H', (4, 6): 'H',
    (4, 7): 'H', (4, 8): 'H', (4, 9): 'H', (4, 10): 'H', (4, 'A'): 'H',
    (5, 2): 'H', (5, 3): 'H', (5, 4): 'H', (5, 5): 'H', (5, 6): 'H',
    (5, 7): 'H', (5, 8): 'H', (5, 9): 'H', (5, 10): 'H', (5, 'A'): 'H',
    (6, 2): 'H', (6, 3): 'H', (6, 4): 'H', (6, 5): 'H', (6, 6): 'H',
    (6, 7): 'H', (6, 8): 'H', (6, 9): 'H', (6, 10): 'H', (6, 'A'): 'H',
    (7, 2): 'H', (7, 3): 'H', (7, 4): 'H', (7, 5): 'H', (7, 6): 'H',
    (7, 7): 'H', (7, 8): 'H', (7, 9): 'H', (7, 10): 'H', (7, 'A'): 'H',
    (8, 2): 'H', (8, 3): 'H', (8, 4): 'H', (8, 5): 'H', (8, 6): 'H',
    (8, 7): 'H', (8, 8): 'H', (8, 9): 'H', (8, 10): 'H', (8, 'A'): 'H',
    (9, 2): 'H', (9, 3): 'D', (9, 4): 'D', (9, 5): 'D', (9, 6): 'D',
    (9, 7): 'H', (9, 8): 'H', (9, 9): 'H', (9, 10): 'H', (9, 'A'): 'H',
    (10, 2): 'D', (10, 3): 'D', (10, 4): 'D', (10, 5): 'D', (10, 6): 'D',
    (10, 7): 'D', (10, 8): 'D', (10, 9): 'D', (10, 10): 'H', (10, 'A'): 'H',
    (11, 2): 'D', (11, 3): 'D', (11, 4): 'D', (11, 5): 'D', (11, 6): 'D',
    (11, 7): 'D', (11, 8): 'D', (11, 9): 'D', (11, 10): 'D', (11, 'A'): 'D',
    (12, 2): 'H', (12, 3): 'H', (12, 4): 'S', (12, 5): 'S', (12, 6): 'S',
    (12, 7): 'H', (12, 8): 'H', (12, 9): 'H', (12, 10): 'H', (12, 'A'): 'H',
    (13, 2): 'S', (13, 3): 'S', (13, 4): 'S', (13, 5): 'S', (13, 6): 'S',
    (13, 7): 'H', (13, 8): 'H', (13, 9): 'H', (13, 10): 'H', (13, 'A'): 'H',
    (14, 2): 'S', (14, 3): 'S', (14, 4): 'S', (14, 5): 'S', (14, 6): 'S',
    (14, 7): 'H', (14, 8): 'H', (14, 9): 'H', (14, 10): 'H', (14, 'A'): 'H',
    (15, 2): 'S', (15, 3): 'S', (15, 4): 'S', (15, 5): 'S', (15, 6): 'S',
    (15, 7): 'H', (15, 8): 'H', (15, 9): 'H', (15, 10): 'H', (15, 'A'): 'H',
    (16, 2): 'S', (16, 3): 'S', (16, 4): 'S', (16, 5): 'S', (16, 6): 'S',
    (16, 7): 'H', (16, 8): 'H', (16, 9): 'H', (16, 10): 'H', (16, 'A'): 'H',
    (17, 2): 'S', (17, 3): 'S', (17, 4): 'S', (17, 5): 'S', (17, 6): 'S',
    (17, 7): 'S', (17, 8): 'S', (17, 9): 'S', (17, 10): 'S', (17, 'A'): 'S',
    (18, 2): 'S', (18, 3): 'S', (18, 4): 'S', (18, 5): 'S', (18, 6): 'S',
    (18, 7): 'S', (18, 8): 'S', (18, 9): 'S', (18, 10): 'S', (18, 'A'): 'S',
    (19, 2): 'S', (19, 3): 'S', (19, 4): 'S', (19, 5): 'S', (19, 6): 'S',
    (19, 7): 'S', (19, 8): 'S', (19, 9): 'S', (19, 10): 'S', (19, 'A'): 'S',
    (20, 2): 'S', (20, 3): 'S', (20, 4): 'S', (20, 5): 'S', (20, 6): 'S',
    (20, 7): 'S', (20, 8): 'S', (20, 9): 'S', (20, 10): 'S', (20, 'A'): 'S',
    (21, 2): 'S', (21, 3): 'S', (21, 4): 'S', (21, 5): 'S', (21, 6): 'S',
    (21, 7): 'S', (21, 8): 'S', (21, 9): 'S', (21, 10): 'S', (21, 'A'): 'S',


    # Soft Totals
    ('A,2', 2): 'H', ('A,2', 3): 'H', ('A,2', 4): 'H', ('A,2', 5): 'D', ('A,2', 6): 'D',
    ('A,2', 7): 'H', ('A,2', 8): 'H', ('A,2', 9): 'H', ('A,2', 10): 'H', ('A,2', 'A'): 'H',
    ('A,3', 2): 'H', ('A,3', 3): 'H', ('A,3', 4): 'H', ('A,3', 5): 'D', ('A,3', 6): 'D',
    ('A,3', 7): 'H', ('A,3', 8): 'H', ('A,3', 9): 'H', ('A,3', 10): 'H', ('A,3', 'A'): 'H',
    ('A,4', 2): 'H', ('A,4', 3): 'H', ('A,4', 4): 'D', ('A,4', 5): 'D', ('A,4', 6): 'D',
    ('A,4', 7): 'H', ('A,4', 8): 'H', ('A,4', 9): 'H', ('A,4', 10): 'H', ('A,4', 'A'): 'H', 
    ('A,5', 2): 'H', ('A,5', 3): 'H', ('A,5', 4): 'D', ('A,5', 5): 'D', ('A,5', 6): 'D',
    ('A,5', 7): 'H', ('A,5', 8): 'H', ('A,5', 9): 'H', ('A,5', 10): 'H', ('A,5', 'A'): 'H',
    ('A,6', 2): 'H', ('A,6', 3): 'D', ('A,6', 4): 'D', ('A,6', 5): 'D', ('A,6', 6): 'D',
    ('A,6', 7): 'H', ('A,6', 8): 'H', ('A,6', 9): 'H', ('A,6', 10): 'H', ('A,6', 'A'): 'H',
    ('A,7', 2): 'D', ('A,7', 3): 'D', ('A,7', 4): 'D', ('A,7', 5): 'D', ('A,7', 6): 'D',
    ('A,7', 7): 'S', ('A,7', 8): 'S', ('A,7', 9): 'H', ('A,7', 10): 'H', ('A,7', 'A'): 'H',
    ('A,8', 2): 'S', ('A,8', 3): 'S', ('A,8', 4): 'S', ('A,8', 5): 'S', ('A,8', 6): 'D',
    ('A,8', 7): 'S', ('A,8', 8): 'S', ('A,8', 9): 'S', ('A,8', 10): 'S', ('A,8', 'A'): 'S',
    ('A,9', 2): 'S', ('A,9', 3): 'S', ('A,9', 4): 'S', ('A,9', 5): 'S', ('A,9', 6): 'S',
    ('A,9', 7): 'S', ('A,9', 8): 'S', ('A,9', 9): 'S', ('A,9', 10): 'S', ('A,9', 'A'): 'S',
    ('A,10', 2): 'S', ('A,10', 3): 'S', ('A,10', 4): 'S', ('A,10', 5): 'S', ('A,10', 6): 'S',
    ('A,10', 7): 'S', ('A,10', 8): 'S', ('A,10', 9): 'S', ('A,10', 10): 'S', ('A,10', 'A'): 'S',

    # Splitting Totals
    ('A,A', 2): 'Y', ('A,A', 3): 'Y', ('A,A', 4): 'Y', ('A,A', 5): 'Y', ('A,A', 6): 'Y',
    ('A,A', 7): 'Y', ('A,A', 8): 'Y', ('A,A', 9): 'Y', ('A,A', 10): 'Y', ('A,A', 'A'): 'Y',
    ('10,10', 2): 'N', ('10,10', 3): 'N', ('10,10', 4): 'N', ('10,10', 5): 'N', ('10,10', 6): 'N',
    ('10,10', 7): 'N', ('10,10', 8): 'N', ('10,10', 9): 'N', ('10,10', 10): 'N', ('10,10', 'A'): 'N',
    ('9,9', 2): 'Y', ('9,9', 3): 'Y', ('9,9', 4): 'Y', ('9,9', 5): 'Y', ('9,9', 6): 'Y',
    ('9,9', 7): 'N', ('9,9', 8): 'Y', ('9,9', 9): 'Y', ('9,9', 10): 'N', ('9,9', 'A'): 'N',
    ('8,8', 2): 'Y', ('8,8', 3): 'Y', ('8,8', 4): 'Y', ('8,8', 5): 'Y', ('8,8', 6): 'Y',
    ('8,8', 7): 'Y', ('8,8', 8): 'Y', ('8,8', 9): 'Y', ('8,8', 10): 'Y', ('8,8', 'A'): 'Y',
    ('7,7', 2): 'Y', ('7,7', 3): 'Y', ('7,7', 4): 'Y', ('7,7', 5): 'Y', ('7,7', 6): 'Y',
    ('7,7', 7): 'Y', ('7,7', 8): 'N', ('7,7', 9): 'N', ('7,7', 10): 'N', ('7,7', 'A'): 'N',
    ('6,6', 2): 'Y', ('6,6', 3): 'Y', ('6,6', 4): 'Y', ('6,6', 5): 'Y', ('6,6', 6): 'Y',
    ('6,6', 7): 'N', ('6,6', 8): 'N', ('6,6', 9): 'N', ('6,6', 10): 'N', ('6,6', 'A'): 'N',
    ('5,5', 2): 'N', ('5,5', 3): 'N', ('5,5', 4): 'N', ('5,5', 5): 'N', ('5,5', 6): 'N',
    ('5,5', 7): 'N', ('5,5', 8): 'N', ('5,5', 9): 'N', ('5,5', 10): 'N', ('5,5', 'A'): 'N',
    ('4,4', 2): 'N', ('4,4', 3): 'N', ('4,4', 4): 'N', ('4,4', 5): 'Y', ('4,4', 6): 'Y',
    ('4,4', 7): 'N', ('4,4', 8): 'N', ('4,4', 9): 'N', ('4,4', 10): 'N', ('4,4', 'A'): 'N',
    ('3,3', 2): 'Y', ('3,3', 3): 'Y', ('3,3', 4): 'Y', ('3,3', 5): 'Y', ('3,3', 6): 'Y',
    ('3,3', 7): 'Y', ('3,3', 8): 'N', ('3,3', 9): 'N', ('3,3', 10): 'N', ('3,3', 'A'): 'N',
    ('2,2', 2): 'Y', ('2,2', 3): 'Y', ('2,2', 4): 'Y', ('2,2', 5): 'Y', ('2,2', 6): 'Y',
    ('2,2', 7): 'Y', ('2,2', 8): 'N', ('2,2', 9): 'N', ('2,2', 10): 'N', ('2,2', 'A'): 'N',
}

# Initialize Q-values for a given state-action pair
def initialize_state_action(state):
    """
    Initialize Q-values for a given state. Handles pairs and regular states.
    """
    if state not in q_table:
        if isinstance(state[0], str):  # Pair state (e.g., '8,8')
            q_table[state] = {'Split': 0.0, 'Hit': 0.0, 'Stand': 0.0, 'Double': 0.0}
        else:  # Regular state
            q_table[state] = {'Hit': 0.0, 'Stand': 0.0, 'Double': 0.0, 'Split': 0.0}
        logging.info(f"Initialized state in Q-table: {state}")

# Define function to choose an action based on epsilon-greedy policy and basic strategy
def choose_action(state, hand, available_actions):
    """
    Choose an action based on the Q-table or basic strategy, constrained by available actions.

    Args:
        state (tuple): Current state of the game.
        hand (list): The player's current hand.
        available_actions (list): List of actions allowed in the current state.
        epsilon (float): Exploration rate for epsilon-greedy policy.

    Returns:
        str: The chosen action.
    """
    # Exploration: With probability epsilon, choose a random action
    if random.uniform(0, 1) < epsilon:
        return random.choice(available_actions)

    # Exploitation: Choose the best action based on Q-values or basic strategy
    if isinstance(state[0], str):  # Splittable pair
        pair, dealer_card = state
        if state in q_table:
            q_values = q_table[state]
            best_action = max(q_values, key=q_values.get)
        else:
            # Default to basic strategy
            strategy_action = basic_strategy_q_table.get((pair, dealer_card), None)
            best_action = {"H": "Hit", "S": "Stand", "D": "Double", "Y": "Split", "N": "Stand"}.get(strategy_action, "Stand")
    else:
        # Non-pair states
        if state in q_table:
            q_values = q_table[state]
            best_action = max(q_values, key=q_values.get)
        else:
            # Default to basic strategy
            player_total, dealer_card, usable_ace = state
            strategy_action = basic_strategy_q_table.get((player_total, dealer_card), None)
            best_action = {"H": "Hit", "S": "Stand", "D": "Double"}.get(strategy_action, "Stand")

    # Ensure the chosen action is in the list of available actions
    return best_action if best_action in available_actions else "Stand"


# Define function to update Q-value
def update_q_value(state, action, reward, next_state):
    if next_state is None:
        next_max = 0
    else:
        if next_state not in q_table:
            initialize_state_action(next_state)
        next_max = max(q_table[next_state].values())
    
    old_value = q_table[state][action]
    q_table[state][action] = old_value + alpha * (reward + gamma * next_max - old_value)

def get_state(hand, dealer_card, usable_ace):
    """
    Represent the state of the game, considering pairs for splitting and total for other hands.

    Args:
        hand (list): Player's current hand.
        dealer_card (tuple): Dealer's up card (rank, suit).
        usable_ace (bool): Whether the hand has a usable ace.

    Returns:
        tuple: Encoded state of the game.
    """
    if len(hand) == 2 and hand[0][0] == hand[1][0]:  # Splittable pair
        pair = f"{hand[0][0]},{hand[1][0]}"  # Represent as pair (e.g., '8,8')
        return (pair, dealer_card[0])  # Pair state with dealer card rank
    else:
        player_total = sum([card[1] if isinstance(card[1], int) else 10 for card in hand])
        return (player_total, dealer_card[0], usable_ace)




