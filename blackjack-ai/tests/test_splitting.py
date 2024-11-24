import unittest
from games.game1 import Blackjack  # Replace with the correct module path if different

class TestCanSplit(unittest.TestCase):
    def setUp(self):
        self.blackjack = Blackjack()

    def test_can_split(self):
        test_cases = [
            ([('8', 'Hearts'), ('8', 'Diamonds')], True),  # Valid split
            ([('10', 'Hearts'), ('8', 'Diamonds')], False),  # Different ranks
            ([('A', 'Hearts'), ('A', 'Diamonds')], True),  # Valid split
            ([('8', 'Hearts')], False),  # Only one card
            ([('K', 'Clubs'), ('K', 'Diamonds')], True),  # Valid split
            ([('2', 'Spades'), ('3', 'Hearts')], False),  # Different ranks
        ]

        for hand, expected in test_cases:
            with self.subTest(hand=hand):
                self.assertEqual(
                    self.blackjack.can_split(hand), expected, 
                    f"Failed for hand: {hand}"
                )

if __name__ == '__main__':
    unittest.main()
