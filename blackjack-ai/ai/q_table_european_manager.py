import pickle
import json

def save_eblackjack_q_table(q_table, filename="e_blackjack_q_table.pkl"):
    """
    Save the Q-table to a file using pickle.
    Args:
        q_table (dict): The Q-table to be saved.
        filename (str): The file name where the Q-table will be saved.
    """
    with open(filename, "wb") as file:
        pickle.dump(q_table, file)
    print(f"European Blackjack Q-table saved to {filename}")

def load_eblackjack_q_table(filename="e_blackjack_q_table.pkl"):
    """
    Load the Q-table from a pickle file.
    Args:
        filename (str): The file name to load the Q-table from.
    Returns:
        dict: The loaded Q-table.
    """
    try:
        with open(filename, "rb") as file:
            q_table = pickle.load(file)
        print(f"European Blackjack Q-table loaded from {filename}")
        return q_table
    except FileNotFoundError:
        print(f"No Q-table found at {filename}. Starting with an empty table.")
        return {}

def save_eblackjack_q_table_json(q_table, filename="e_blackjack_q_table.json"):
    """
    Save the Q-table to a file in JSON format.
    Args:
        q_table (dict): The Q-table to be saved.
        filename (str): The file name where the Q-table will be saved.
    """
    # Convert tuple keys to strings for JSON serialization
    q_table_serializable = {str(key): value for key, value in q_table.items()}
    with open(filename, "w") as file:
        json.dump(q_table_serializable, file, indent=4)
    print(f"European Blackjack Q-table saved to {filename} as JSON")

def load_eblackjack_q_table_json(filename="e_blackjack_q_table.json"):
    """
    Load the Q-table from a JSON file.
    Args:
        filename (str): The file name to load the Q-table from.
    Returns:
        dict: The loaded Q-table.
    """
    try:
        with open(filename, "r") as file:
            q_table_serializable = json.load(file)
        # Convert string keys back to tuples
        q_table = {eval(key): value for key, value in q_table_serializable.items()}
        print(f"European Blackjack Q-table loaded from {filename}")
        return q_table
    except FileNotFoundError:
        print(f"No Q-table found at {filename}. Starting with an empty table.")
        return {}