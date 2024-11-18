import random
import logging

class BlackjackSwitch:
    def __init__(self):
        self.deck = self.create_deck()
        self.player_hand1 = []
        self.player_hand2 = []
        self.dealer_hand = []

    def create_deck(self):
        suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
        values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
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

    def switch_cards(self):
        """
        Switch the top cards of the two player hands.
        """
        if self.player_hand1 and self.player_hand2:
            self.player_hand1[-1], self.player_hand2[-1] = self.player_hand2[-1], self.player_hand1[-1]
            logging.info("Switched top cards of the two hands.")

    def check_winner(self):
        dealer_val = self.hand_value(self.dealer_hand)
        player_val1 = self.hand_value(self.player_hand1)
        player_val2 = self.hand_value(self.player_hand2)

        results = []
        for player_val in [player_val1, player_val2]:
            if player_val > 21:
                results.append("Player Busts! Dealer Wins.")
            elif dealer_val > 21:
                results.append("Dealer Busts! Player Wins.")
            elif dealer_val == 22:
                results.append("Dealer Pushes on 22.")
            elif player_val > dealer_val:
                results.append("Player Wins!")
            elif player_val < dealer_val:
                results.append("Dealer Wins.")
            else:
                results.append("It's a Tie!")

        return results

    def new_game(self):
        self.player_hand1 = []
        self.player_hand2 = []
        self.dealer_hand = []
        self.deck = self.create_deck()

        # Deal two hands for the player and two cards for the dealer
        for _ in range(2):
            self.deal_card(self.player_hand1)
            self.deal_card(self.player_hand2)
        self.deal_card(self.dealer_hand)
        self.deal_card(self.dealer_hand)