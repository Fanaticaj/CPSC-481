# -------------------------- European Blackjack --------------------------
import random
import logging

class EBlackjack:
    def __init__(self):
        self.deck = self.create_deck()
        self.player_hand = []
        self.dealer_hand = []
        self.split_hands = []
    
    def create_deck(self):
        """Create a shuffled deck with 6 standard decks."""
        suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
        values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        single_deck = [(v, s) for v in values for s in suits]
        full_deck = single_deck * 2  # Multiply by 2 to create a 2-deck shoe
        random.shuffle(full_deck)
        return full_deck

    def deal_card(self, hand):
        if not self.deck:
            logging.warning("Deck is empty. Replenishing deck.")
            self.deck = self.create_deck()  # Reset the deck
        hand.append(self.deck.pop())


    def hand_value(self, hand):
        value = 0
        aces = 0
        for card, suit in hand:
            if card.isdigit():
                value += int(card)
            elif card in ['J', 'Q', 'K']:
                value += 10
            elif card == 'A':
                value += 11
                aces += 1

    # Adjust for aces being 1 or 11
        while value > 21 and aces > 0:
            value -= 10
            aces -= 1

        return value


    def check_winner(self):
        player_val = self.hand_value(self.player_hand)
        dealer_val = self.hand_value(self.dealer_hand)

        if player_val > 21:
            result = "Player Busts! Dealer Wins."
        elif player_val == 21:
            result = "Player Wins! Blackjack!"
        elif dealer_val > 21:
            result = "Dealer Busts! Player Wins."
        elif player_val == dealer_val:
            result = "It's a Tie!"
        elif player_val > dealer_val:
            result = "Player Wins!"
        else:
            result = "Dealer Wins!"
        
        logging.info(f"Final Results -> Player: {player_val}, Dealer: {dealer_val}, Outcome: {result}")
        return result
    
    def has_usable_ace(self, hand):
        """Check if the hand has a usable Ace (counts as 11 without busting)."""
        total_value = self.hand_value(hand)
        # Check for an Ace in the hand and if total <= 21 with Ace counted as 11
        return any(card == 'A' for card, suit in hand) and total_value <= 21

    def new_game(self):
        self.player_hand = []
        self.dealer_hand = []
        self.deck = self.create_deck()

        self.deal_card(self.player_hand)
        self.deal_card(self.dealer_hand) # Dealer gets one card, and gets second after player chooses action
        self.deal_card(self.player_hand)

        logging.info(f"Player's initial hand: {self.player_hand}, Total: {self.hand_value(self.player_hand)}")
    
    def is_bust(self, hand):
        if self.hand_value(hand) > 21:
            return True
        return False
    
    def double_down(self, hand):
        """Double down: Hit once, then stand with the new total."""
        if self.hand_value(hand) == 9 or 10 or 11:
            self.deal_card(hand)
            logging.info(f"Player's hand after doubling down: {hand}, Total: {self.hand}")
        else:
            logging.info(f"Invalid double down. Player's hand: {hand}, Total: {self.hand}")
        return self.hand_value(hand)  # The hand must stand immediately after this.

    
    def play_dealer_hand(self):
        """
        Play the dealer's hand according to standard Blackjack rules:
        - Dealer hits until their hand value is at least 17.
        - Dealer stands on soft 17 or higher.
        """
        logging.info(f"Dealer's initial hand: {self.dealer_hand}, Total: {self.hand_value(self.dealer_hand)}")

        while self.hand_value(self.dealer_hand) < 17 or (
            self.hand_value(self.dealer_hand) == 17 and self.has_soft_ace(self.dealer_hand)
        ):
            # Dealer hits
            self.deal_card(self.dealer_hand)
            logging.info(f"Dealer hits and receives: {self.dealer_hand[-1]}")
            logging.info(f"Dealer's updated hand: {self.dealer_hand}, Total: {self.hand_value(self.dealer_hand)}")

            if self.hand_value(self.dealer_hand) >= 17:
                break
        
            # Check if dealer busts
            if self.hand_value(self.dealer_hand) > 21:
                logging.warning(f"Dealer busts with hand: {self.dealer_hand}, Total: {self.hand_value(self.dealer_hand)}")
                return self.hand_value(self.dealer_hand)  # Return bust total

        # Dealer stands
        total = self.hand_value(self.dealer_hand)
        if self.hand_value(self.dealer_hand) == 17 and self.has_soft_ace(self.dealer_hand):
            logging.info(f"Dealer stands on soft 17 with hand: {self.dealer_hand}, Total: {total}")
        else:
            logging.info(f"Dealer stands with hand: {self.dealer_hand}, Total: {total}")

        return total
    
    def can_split(self, hand):
        """Check if the hand can be split."""
        if len(hand) != 2:  # Ensure the hand contains exactly two cards
            return False

        rank1 = hand[0][0]
        rank2 = hand[1][0]

        # Ensure the cards have the same rank
        if rank1 != rank2:
            return False

        # Prevent splitting restricted pairs (4, 5, and 10-value cards)
        restricted_ranks = {'4', '5', '10'}  # 10-value cards are represented by '10', 'J', 'Q', 'K'
        if rank1 in restricted_ranks or rank2 in restricted_ranks:
            return False

        return True
    
    
    def split_hand(self, hand):
        """Split the hand into two separate hands."""
        logging.info(f"Player chooses to split the hand. Current Hand: {hand}")
        if not self.can_split(hand):
            logging.warning("Hand cannot be split.")
            return None, None  # Return an empty list if splitting isn't allowed

        # Create two hands and deal a new card to each
        hand1 = [hand[0]]
        hand2 = [hand[1]]
        self.deal_card(hand1)
        self.deal_card(hand2)

        # Log the result of the split
        logging.info(f"Split Hand 1: {hand1}")
        logging.info(f"Split Hand 2: {hand2}")

        return hand1, hand2
    
    def can_double_down(self, hand, is_split=False):
        if is_split:  # Check if the hand is a split hand
            return False
        if len(hand) != 2:
            return False
        total = self.hand_value(hand)
        has_usable_ace = self.has_usable_ace(hand)
        return not has_usable_ace and total in {9, 10, 11}
    
    def has_soft_ace(self, hand):
        """
        Returns True if the hand contains a soft Ace (Ace valued at 11).
        """
        total = sum(10 if card[0] in "JQK" else 11 if card[0] == "A" else int(card[0]) for card in hand)
        return total <= 21 and any(card[0] == "A" for card in hand)

    
    def stand(self, hand):
        """Stand with the current hand."""
        logging.info("Player chooses to stand.")
        dealer_total = self.play_dealer_hand()

        player_total = self.hand_value(hand)
        dealer_total = self.hand_value(self.dealer_hand)

        if dealer_total > 21:
            result = "Player Wins"
        elif player_total > dealer_total:
            result = "Player Wins"
        elif player_total < dealer_total:
            result = "Dealer Wins"
        else:
            result = "Push"
        
        logging.info(f"Final Results -> Player: {player_total}, Dealer: {dealer_total}, Outcome: {result}")
        return result
    
    def hit(self, hand):
        """
        Player chooses to hit. A card is dealt to their hand.
        """
        logging.info("Player chooses to hit.")
        self.deal_card(hand)
        hand_total = self.hand_value(hand)

        if self.is_bust(hand):
            result = "Player Busts! Dealer Wins."
            logging.info(f"Final Results -> Player: {hand_total}, Dealer: {self.hand_value(self.dealer_hand)}, Outcome: {result}")
            return {
                "hand": hand,
                "total": hand_total,
                "bust": True,
                "result": result
            }
        else:
            logging.info(f"Player hits successfully. Current hand: {hand}, Total: {hand_total}")
            return {
                "hand": hand,
                "total": hand_total,
                "bust": False
            }
    
    def double(self, hand, bet):
        """
        Player chooses to double down. Their initial bet is doubled, and they receive one additional card.
        The turn ends immediately after the card is dealt.
    
        Args:
        hand (list): The player's current hand.
        bet (float): The player's current bet.

        Returns:
        dict: Updated hand, total value, new bet, and game state (bust or not).
        """
        logging.info("Player chooses to double down.")

        # Double the player's bet
        new_bet = bet * 2

        # Deal one card to the player's hand
        self.deal_card(hand)
        hand_total = self.hand_value(hand)

        # Check if the player busts
        if self.is_bust(hand):
            logging.info(f"Player busts after doubling down. Hand: {hand}, Total: {hand_total}")
            return {
                "hand": hand,
                "total": hand_total,
                "new_bet": new_bet,
                "bust": True,
                "result": "Player Busts! Dealer Wins."
            }
        else:
            logging.info(f"Player completes double down successfully. Hand: {hand}, Total: {hand_total}")
            return {
                "hand": hand,
                "total": hand_total,
                "new_bet": new_bet,
                "bust": False
            }

    def split(self, hand, bet):
        """
        Player chooses to split their hand into two separate hands if the first two cards are of the same rank.
        Each split hand gets one additional card, and the bet is doubled for the second hand.

        Args:
        hand (list): The player's current hand.
        bet (float): The player's current bet.

        Returns:
        dict: Contains the two split hands, their total values, the updated bets for each hand, 
              and whether the action was successful.
        """
        logging.info("Player chooses to split their hand.")

        # Check if the hand can be split
        if not self.can_split(hand):
            logging.warning("Hand cannot be split. Splitting is only allowed if the first two cards are the same rank.")
            return {
                "success": False,
                "message": "Hand cannot be split",
                "hand1": None,
                "hand2": None,
                "bet1": bet,
                "bet2": None,
                "win": None,
            }

        # Create two separate hands
        hand1 = [hand[0]]  # First card goes to the first hand
        hand2 = [hand[1]]  # Second card goes to the second hand

        # Deal one card to each new hand
        self.deal_card(hand1)
        self.deal_card(hand2)

        # Update the bet for the second hand (same as the original bet)
        bet2 = bet

        # Calculate hand values
        hand1_total = self.hand_value(hand1)
        hand2_total = self.hand_value(hand2)

        logging.info(f"Hand 1 after split: {hand1}, Total: {hand1_total}")
        logging.info(f"Hand 2 after split: {hand2}, Total: {hand2_total}")

        return {
            "success": True,
            "hand1": hand1,
            "hand2": hand2,
            "bet1": bet,
            "bet2": bet2,
            "hand1_total": hand1_total,
            "hand2_total": hand2_total,
            "win": None,
    }

        


