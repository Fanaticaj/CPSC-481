import pickle
import json

def save_q_table_spanish(q_table, filename="q_table_spanish.pkl"):
    """Save the Q-table for Spanish Blackjack to a file."""
    with open(filename, "wb") as file:
        pickle.dump(q_table, file)
    print(f"Spanish Blackjack Q-table saved to {filename}")

def load_q_table_spanish(filename="q_table_spanish.pkl"):
    """Load the Q-table for Spanish Blackjack from a file."""
    try:
        with open(filename, "rb") as file:
            q_table = pickle.load(file)
        print(f"Spanish Blackjack Q-table loaded from {filename}")
        return q_table
    except FileNotFoundError:
        print(f"No Q-table found at {filename}. Starting with an empty table.")
        return {}


def save_q_table_spanish_json(q_table, filename="q_table_spanish.json"):
    """Save the Q-table for Spanish Blackjack to a JSON file."""
    # Convert tuple keys to strings for JSON serialization
    q_table_serializable = {str(key): value for key, value in q_table.items()}
    with open(filename, "w") as file:
        json.dump(q_table_serializable, file, indent=4)
    print(f"Spanish Blackjack Q-table saved to {filename} as JSON")

def load_q_table_spanish_json(filename="q_table_spanish.json"):
    """Load the Q-table for Spanish Blackjack from a JSON file."""
    try:
        with open(filename, "r") as file:
            q_table_serializable = json.load(file)
        # Convert string keys back to tuples
        q_table = {eval(key): value for key, value in q_table_serializable.items()}
        print(f"Spanish Blackjack Q-table loaded from {filename}")
        return q_table
    except FileNotFoundError:
        print(f"No Q-table found at {filename}. Starting with an empty table.")
        return {}
