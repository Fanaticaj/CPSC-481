import unittest
from player.player_game1 import PlayerBlackjack

class TestBlackjackSplitting(unittest.TestCase):
    def setUp(self):
        """Initialize PlayerBlackjack instance before each test."""
        self.player_blackjack = PlayerBlackjack()

    def test_split_action(self):
        # Test scenario for 8,8 split
        self.player_blackjack.game.player_hand = [('8', 'Hearts'), ('8', 'Spades')]
        self.assertTrue(self.player_blackjack.game.can_split(self.player_blackjack.game.player_hand), "Should allow split for 8,8")

        # Test scenario for A,A split
        self.player_blackjack.game.player_hand = [('A', 'Hearts'), ('A', 'Clubs')]
        self.assertTrue(self.player_blackjack.game.can_split(self.player_blackjack.game.player_hand), "Should allow split for A,A")

    def test_no_split_action(self):
        # Test scenario for mixed card values
        self.player_blackjack.game.player_hand = [('10', 'Hearts'), ('8', 'Clubs')]
        self.assertFalse(self.player_blackjack.game.can_split(self.player_blackjack.game.player_hand), "Should not allow split for mixed cards")

    def test_split_hand(self):
        # Set up a scenario for 8,8 split
        self.player_blackjack.game.player_hand = [('8', 'Hearts'), ('8', 'Spades')]
        self.player_blackjack.game.dealer_hand = [('10', 'Diamonds')]

        # Check if splitting is allowed
        self.assertTrue(self.player_blackjack.game.can_split(self.player_blackjack.game.player_hand), "Should allow split for 8,8")

        # Perform the split
        split_hands = self.player_blackjack.game.split_hand(self.player_blackjack.game.player_hand)

        # Validate the result of the split
        self.assertEqual(len(split_hands), 2, "Should result in two split hands")
        self.assertEqual(len(split_hands[0]), 2, "First split hand should have two cards")
        self.assertEqual(len(split_hands[1]), 2, "Second split hand should have two cards")

        # Validate that one original card and one new card exist in each hand
        self.assertEqual(split_hands[0][0][0], '8', "First hand should start with '8'")
        self.assertEqual(split_hands[1][0][0], '8', "Second hand should start with '8'")

        # Ensure new cards were added to split hands
        self.assertNotEqual(split_hands[0][1][0], '8', "First hand should have a new card added")
        self.assertNotEqual(split_hands[1][1][0], '8', "Second hand should have a new card added")


if __name__ == "__main__":
    unittest.main()

