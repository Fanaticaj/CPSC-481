# -------------------------- Spanish 21 --------------------------

import random
import logging

class SpanishBlackjack:
    def __init__(self):
        self.deck = self.create_deck()
        self.player_hand = []
        self.dealer_hand = []
    
    def create_deck(self):
        suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
        values = ['2', '3', '4', '5', '6', '7', '8', '9', 'J', 'Q', 'K', 'A']
        # Remove 10s for Spanish Blackjack
        deck = [(v, s) for v in values for s in suits]
        random.shuffle(deck)
        return deck

    def deal_card(self, hand):
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
            return "Player Busts! Dealer Wins."
        elif player_val == 21:
            return "Player Wins! Blackjack!"
        elif dealer_val > 21:
            return "Dealer Busts! Player Wins."
        elif player_val == dealer_val:
            return "It's a Tie!"
        elif player_val > dealer_val:
            return "Player Wins!"
        else:
            return "Dealer Wins!"
    
    def has_usable_ace(self, hand):
        """Check if the hand has a usable Ace (counts as 11 without busting)."""
        total_value = self.hand_value(hand)
        return any(card == 'A' for card, suit in hand) and total_value <= 21

    def new_game(self):
        self.player_hand = []
        self.dealer_hand = []
        self.deck = self.create_deck()

        self.deal_card(self.player_hand)
        self.deal_card(self.dealer_hand)
        self.deal_card(self.player_hand)
        self.deal_card(self.dealer_hand)
    
    def is_bust(self, hand):
        if self.hand_value(hand) > 21:
            logging.warning(f"Bust detected: Hand={hand}, Value={self.hand_value(hand)}")
            return True
        return False
    
    def play_dealer_hand(self):
        """Play the dealer's hand according to standard Spanish Blackjack rules."""
        while self.hand_value(self.dealer_hand) < 17:
            self.deal_card(self.dealer_hand)
        return self.hand_value(self.dealer_hand)
