import random

alpha = 0.1 # Learning Rate
gamma = 0.9 # Discount Factor
epsilon = 0.1 # Exploration rate

actions = ["Hit", "Stand"] 

q_table = {}

basic_strategy_q_table = {
    # Hard Totals
    (8, 2): 'H', (8, 3): 'H', (8, 4): 'H', (8, 5): 'H', (8, 6): 'H',
    (8, 7): 'H', (8, 8): 'H', (8, 9): 'H', (8, 10): 'H', (8, 'A'): 'H',
    (9, 2): 'D/H', (9, 3): 'D/H', (9, 4): 'D/H', (9, 5): 'D/H', (9, 6): 'D/H',
    (9, 7): 'H', (9, 8): 'H', (9, 9): 'H', (9, 10): 'H', (9, 'A'): 'H',
    (10, 2): 'D/H', (10, 3): 'D/H', (10, 4): 'D/H', (10, 5): 'D/H', (10, 6): 'D/H',
    (10, 7): 'D/H', (10, 8): 'D/H', (10, 9): 'D/H', (10, 10): 'H', (10, 'A'): 'H',
    (11, 2): 'D/H', (11, 3): 'D/H', (11, 4): 'D/H', (11, 5): 'D/H', (11, 6): 'D/H',
    (11, 7): 'D/H', (11, 8): 'D/H', (11, 9): 'D/H', (11, 10): 'D/H', (11, 'A'): 'H',
    (12, 2): 'H', (12, 3): 'H', (12, 4): 'S', (12, 5): 'S', (12, 6): 'S',
    (12, 7): 'H', (12, 8): 'H', (12, 9): 'H', (12, 10): 'H', (12, 'A'): 'H',
    (13, 2): 'S', (13, 3): 'S', (13, 4): 'S', (13, 5): 'S', (13, 6): 'S',
    (13, 7): 'H', (13, 8): 'H', (13, 9): 'H', (13, 10): 'H', (13, 'A'): 'H',
    (14, 2): 'S', (14, 3): 'S', (14, 4): 'S', (14, 5): 'S', (14, 6): 'S',
    (14, 7): 'H', (14, 8): 'H', (14, 9): 'H', (14, 10): 'R/H', (14, 'A'): 'R/H',
    (15, 2): 'S', (15, 3): 'S', (15, 4): 'S', (15, 5): 'S', (15, 6): 'S',
    (15, 7): 'H', (15, 8): 'H', (15, 9): 'R/H', (15, 10): 'R/H', (15, 'A'): 'R/H',
    (16, 2): 'S', (16, 3): 'S', (16, 4): 'S', (16, 5): 'S', (16, 6): 'S',
    (16, 7): 'R/H', (16, 8): 'R/H', (16, 9): 'R/H', (16, 10): 'R/H', (16, 'A'): 'R/H',
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
    ('A,2', 2): 'H', ('A,2', 3): 'H', ('A,2', 4): 'H', ('A,2', 5): 'D/H', ('A,2', 6): 'D/H',
    ('A,3', 2): 'H', ('A,3', 3): 'H', ('A,3', 4): 'H', ('A,3', 5): 'D/H', ('A,3', 6): 'D/H',
    ('A,4', 2): 'H', ('A,4', 3): 'H', ('A,4', 4): 'D/H', ('A,4', 5): 'D/H', ('A,4', 6): 'D/H',
    ('A,4', 7): 'H', ('A,4', 8): 'H', ('A,4', 9): 'H', ('A,4', 10): 'H', ('A,4', 'A'): 'H', ('A,5', 2): 'H', ('A,5', 3): 'H', ('A,5', 4): 'D/H', ('A,5', 5): 'D/H', ('A,5', 6): 'D/H',
    ('A,5', 7): 'H', ('A,5', 8): 'H', ('A,5', 9): 'H', ('A,5', 10): 'H', ('A,5', 'A'): 'H',
    ('A,6', 2): 'H', ('A,6', 3): 'D/H', ('A,6', 4): 'D/H', ('A,6', 5): 'D/H', ('A,6', 6): 'D/H',
    ('A,6', 7): 'H', ('A,6', 8): 'H', ('A,6', 9): 'H', ('A,6', 10): 'H', ('A,6', 'A'): 'H',
    ('A,7', 2): 'S', ('A,7', 3): 'D/S', ('A,7', 4): 'D/S', ('A,7', 5): 'D/S', ('A,7', 6): 'D/S',
    ('A,7', 7): 'S', ('A,7', 8): 'S', ('A,7', 9): 'H', ('A,7', 10): 'H', ('A,7', 'A'): 'H',
    ('A,8', 2): 'S', ('A,8', 3): 'S', ('A,8', 4): 'S', ('A,8', 5): 'S', ('A,8', 6): 'S',
    ('A,8', 7): 'S', ('A,8', 8): 'S', ('A,8', 9): 'S', ('A,8', 10): 'S', ('A,8', 'A'): 'S',

    # Pair Splitting
    (2, 2): 'P/H', (2, 3): 'P/H', (2, 4): 'P/H', (2, 5): 'P/H', (2, 6): 'P/H',
    (2, 7): 'P', (2, 8): 'P', (2, 9): 'H', (2, 10): 'H', (2, 'A'): 'H',
    (3, 2): 'P/H', (3, 3): 'P/H', (3, 4): 'P/H', (3, 5): 'P/H', (3, 6): 'P/H',
    (3, 7): 'P', (3, 8): 'P', (3, 9): 'H', (3, 10): 'H', (3, 'A'): 'H',
    (4, 2): 'H', (4, 3): 'H', (4, 4): 'H', (4, 5): 'P/H', (4, 6): 'P/H',
    (4, 7): 'H', (4, 8): 'H', (4, 9): 'H', (4, 10): 'H', (4, 'A'): 'H',
    (5, 2): 'D/H', (5, 3): 'D/H', (5, 4): 'D/H', (5, 5): 'D/H', (5, 6): 'D/H',
    (5, 7): 'H', (5, 8): 'H', (5, 9): 'H', (5, 10): 'H', (5, 'A'): 'H',
    (6, 2): 'P/H', (6, 3): 'P/H', (6, 4): 'P', (6, 5): 'P', (6, 6): 'P',
    (6, 7): 'H', (6, 8): 'H', (6, 9): 'H', (6, 10): 'H', (6, 'A'): 'H',
    (7, 2): 'P', (7, 3): 'P', (7, 4): 'P', (7, 5): 'P', (7, 6): 'P',
    (7, 7): 'P', (7, 8): 'H', (7, 9): 'H', (7, 10): 'H', (7, 'A'): 'H',
    (8, 2): 'P', (8, 3): 'P', (8, 4): 'P', (8, 5): 'P', (8, 6): 'P',
    (8, 7): 'P', (8, 8): 'P', (8, 9): 'P', (8, 10): 'S', (8, 'A'): 'S',
    (9, 2): 'P', (9, 3): 'P', (9, 4): 'P', (9, 5): 'P', (9, 6): 'P',
    (9, 7): 'S', (9, 8): 'P', (9, 9): 'P', (9, 10): 'S', (9, 'A'): 'S',
    (10, 2): 'S', (10, 3): 'S', (10, 4): 'S', (10, 5): 'S', (10, 6): 'S',
    (10, 7): 'S', (10, 8): 'S', (10, 9): 'S', (10, 10): 'S', (10, 'A'): 'S',
    ('A,A', 2): 'P', ('A,A', 3): 'P', ('A,A', 4): 'P', ('A,A', 5): 'P', ('A,A', 6): 'P',
    ('A,A', 7): 'P', ('A,A', 8): 'P', ('A,A', 9): 'P', ('A,A', 10): 'P', ('A,A', 'A'): 'P',
}

# Initialize Q-values for a given state-action pair
def initialize_state_action(state):
    if state not in q_table:
        q_table[state] = {action: 0 for action in actions}

# Define function to choose an action based on epsilon-greedy policy and basic strategy
def choose_action(state):
    player_total, dealer_card, usable_ace = state

    # Convert 'H', 'S', etc., to actual action strings for Q-learning
    strategy_action = basic_strategy_q_table.get((player_total, dealer_card), None)
    if strategy_action:
        if strategy_action == 'H' or strategy_action == 'D/H':
            basic_action = "Hit"
        elif strategy_action == 'S' or strategy_action == 'D/S':
            basic_action = "Stand"
        elif strategy_action == 'P' or strategy_action == 'P/H':
            basic_action = "Hit"  # Pair splits handled separately; assume "Hit" here 
        elif strategy_action == 'R/H':
            basic_action = "Hit"  # Surrender if possible; otherwise, "Hit"

        # Follow basic strategy action with 90% probability
        if random.uniform(0, 1) < 0.9:
            return basic_action

    # Use epsilon-greedy policy if no basic strategy recommendation or for exploration
    if random.uniform(0, 1) < epsilon:  # Exploration
        return random.choice(actions)
    else:  # Exploitation
        return max(q_table[state], key=q_table[state].get)

# Define function to update Q-value
def update_q_value(state, action, reward, next_state):
    # Initialize next state in the Q-table if it’s not already there
    initialize_state_action(next_state)
    
    # Q-learning update rule
    old_value = q_table[state][action]
    next_max = max(q_table[next_state].values())  # Highest Q-value for the next state
    q_table[state][action] = old_value + alpha * (reward + gamma * next_max - old_value)

# Example state representation
# (player_total, dealer_card, usable_ace)
current_state = (15, 10, False)  # Example: player has 15, dealer shows 10, no usable Ace

# Initialize state-action pairs for the current state
initialize_state_action(current_state)
