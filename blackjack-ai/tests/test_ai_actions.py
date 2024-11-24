import unittest
from ai.basic_strategy import choose_action, q_table

class TestAIActionSelection(unittest.TestCase):

    def setUp(self):
        """Set up a predefined Q-table for testing."""
        self.test_q_table = {
            "(11, ('7', 'Hearts'), False)": {
                "Hit": -0.5695327900000001,
                "Stand": -0.5441260067656166,
                "Double": 0.5298059764986435,
                "Split": -0.39053002391
            },
            "(12, ('7', 'Hearts'), True)": {
                "Hit": -0.19,
                "Stand": -0.1,
                "Double": 0.272835973410667,
                "Split": -0.13095099999999998
            },
            "(12, ('J', 'Clubs'), False)": {
                "Hit": -0.8018471233943343,
                "Stand": -0.610704374778322,
                "Double": -0.8384065230806766,
                "Split": 0.7944566104284118
            },
            "(15, ('J', 'Clubs'), False)": {
                "Hit": -0.6946666961671001,
                "Stand": -0.7129434958736738,
                "Double": -0.6964709483012227,
                "Split": -0.6650534228384363
            },
            "(5, ('4', 'Hearts'), False)": {
                "Hit": -0.1,
                "Stand": 0.4497711391237559,
                "Double": -0.25693080012135394,
                "Split": 0.0
            },
            "(12, ('4', 'Hearts'), False)": {
                "Hit": -0.6513215599000001,
                "Stand": -0.7179381026509464,
                "Double": -0.5736593601938111,
                "Split": -0.5070017572743274
            },
            "(22, ('4', 'Hearts'), False)": {
                "Hit": -0.46855900000000006,
                "Stand": -0.46809963722209774,
                "Double": -0.49743475169116314,
                "Split": -0.46855900000000006
            },
        }
        q_table.update(self.test_q_table)  # Inject test Q-table into the AI logic

    def test_action_selection(self):
        """Test if AI selects the maximum action for each scenario."""
        for state, actions in self.test_q_table.items():
            max_action = max(actions, key=actions.get)  # Get the action with the highest value
            selected_action = choose_action(eval(state))  # Convert state string back to a tuple for the test
            self.assertEqual(selected_action, max_action, f"Expected action '{max_action}' but got '{selected_action}' for state {state}")

if __name__ == "__main__":
    unittest.main()
