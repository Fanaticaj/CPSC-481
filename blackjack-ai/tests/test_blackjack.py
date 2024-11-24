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
        self.assertNotEqual(id(split_hands[0][1]), id(self.player_blackjack.game.player_hand[0]), "First hand should have a new card added")
        self.assertNotEqual(id(split_hands[1][1]), id(self.player_blackjack.game.player_hand[1]), "Second hand should have a new card added")


    def test_soft_12_with_two_aces(self):
        # Set up a scenario for two aces
        self.player_blackjack.game.player_hand = [('A', 'Hearts'), ('A', 'Spades')]
        value = self.player_blackjack.game.hand_value(self.player_blackjack.game.player_hand)
        self.assertEqual(value, 12, "Two aces should result in a soft 12")
    
    def test_hard_20_with_two_kings(self):
        # Test scenario for two kings
        self.player_blackjack.game.player_hand = [('K', 'Hearts'), ('K', 'Clubs')]
        value = self.player_blackjack.game.hand_value(self.player_blackjack.game.player_hand)
        self.assertEqual(value, 20, "Two kings should result in a value of 20")

    def test_hard_20_with_two_queens(self):
        # Test scenario for two queens
        self.player_blackjack.game.player_hand = [('Q', 'Diamonds'), ('Q', 'Spades')]
        value = self.player_blackjack.game.hand_value(self.player_blackjack.game.player_hand)
        self.assertEqual(value, 20, "Two queens should result in a value of 20")

    def test_hard_20_with_two_jacks(self):
        # Test scenario for two jacks
        self.player_blackjack.game.player_hand = [('J', 'Clubs'), ('J', 'Diamonds')]
        value = self.player_blackjack.game.hand_value(self.player_blackjack.game.player_hand)
        self.assertEqual(value, 20, "Two jacks should result in a value of 20")

    def test_hard_20_with_two_tens(self):
        # Test scenario for two tens
        self.player_blackjack.game.player_hand = [('10', 'Hearts'), ('10', 'Spades')]
        value = self.player_blackjack.game.hand_value(self.player_blackjack.game.player_hand)
        self.assertEqual(value, 20, "Two tens should result in a value of 20")
    
    def test_split_after_hit_invalid(self):
        # Set up a scenario where splitting is not allowed after hitting
        self.player_blackjack.game.player_hand = [('8', 'Hearts'), ('4', 'Spades')]
        self.assertFalse(self.player_blackjack.game.can_split(self.player_blackjack.game.player_hand),  "Should not allow split for 8 and 4")

        # Player hits and gets another 4
        self.player_blackjack.game.deal_card(self.player_blackjack.game.player_hand)
        self.player_blackjack.game.player_hand.append(('4', 'Clubs'))  # Adding a second 4 manually

        # Check again for split eligibility
        self.assertFalse(self.player_blackjack.game.can_split(self.player_blackjack.game.player_hand), "Should not allow split for a hand formed after hitting (8, 4, 4)")
    
    def test_double_down_valid(self):
        # Player starts with two cards
        self.player_blackjack.game.player_hand = [('5', 'Hearts'), ('6', 'Spades')]
        self.assertTrue(self.player_blackjack.game.can_double_down(self.player_blackjack.game.player_hand),
                    "Player should be able to double down on the initial hand")

    def test_double_down_invalid_after_hit(self):
        # Player starts with two cards, then hits
        self.player_blackjack.game.player_hand = [('5', 'Hearts'), ('6', 'Spades')]
        self.player_blackjack.game.deal_card(self.player_blackjack.game.player_hand)
        self.assertFalse(self.player_blackjack.game.can_double_down(self.player_blackjack.game.player_hand),"Player should not be able to double down after hitting")

    def test_double_down_invalid_with_more_than_two_cards(self):
        # Player starts with more than two cards (e.g., after splitting)
        self.player_blackjack.game.player_hand = [('5', 'Hearts'), ('6', 'Spades'), ('4', 'Clubs')]
        self.assertFalse(self.player_blackjack.game.can_double_down(self.player_blackjack.game.player_hand), "Player should not be able to double down with more than two cards")
    
    def test_dealer_stands_on_17(self):
        self.player_blackjack.game.dealer_hand = [('10', 'Hearts'), ('7', 'Clubs')]
        self.assertEqual(self.player_blackjack.game.play_dealer_hand(), 17, "Dealer should stand on 17")

    def test_dealer_stands_on_soft_17(self):
        self.player_blackjack.game.dealer_hand = [('A', 'Hearts'), ('6', 'Clubs')]
        self.assertEqual(self.player_blackjack.game.play_dealer_hand(), 17, "Dealer should stand on soft 17")
    
    def test_dealer_stands_on_17(self):
        # Dealer hand: 10 + 7
        self.player_blackjack.game.dealer_hand = [('10', 'Hearts'), ('7', 'Clubs')]
        result = self.player_blackjack.game.play_dealer_hand()
        self.assertEqual(result, 17, "Dealer should stand on 17")

    def test_dealer_stands_on_soft_17(self):
        # Dealer hand: A + 6
        self.player_blackjack.game.dealer_hand = [('A', 'Hearts'), ('6', 'Clubs')]
        result = self.player_blackjack.game.play_dealer_hand()
        self.assertEqual(result, 17, "Dealer should stand on soft 17")





if __name__ == "__main__":
    unittest.main()

