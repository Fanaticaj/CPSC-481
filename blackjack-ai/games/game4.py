# -------------------------- European Blackjack --------------------------

import random
import pygame

class EBlackjack:
    def __init__(self):
        self.deck = self.create_deck()
        self.player_hand = []
        self.dealer_hand = []
    
    def create_deck(self):
        # Standard deck of cards: 4 suits, 13 values each
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
            else:
                value += 11
                aces += 1

        # Adjust for aces being either 1 or 11
        while value > 21 and aces:
            value -= 10
            aces -= 1
        return value

    def check_winner(self):
        player_val = self.hand_value(self.player_hand)
        dealer_val = self.hand_value(self.dealer_hand)

        if player_val > 21:
            return "Player Busts! Dealer Wins."
        elif dealer_val > 21:
            return "Dealer Busts! Player Wins."
        elif player_val == dealer_val:
            return "It's a Tie!"
        elif player_val > dealer_val:
            return "Player Wins!"
        else:
            return "Dealer Wins!"

    def new_game(self):
        # Reset game state
        self.player_hand = []
        self.dealer_hand = []
        self.deck = self.create_deck()

        # Initial card dealing
        self.deal_card(self.player_hand)
        #self.deal_card(self.dealer_hand)
        self.deal_card(self.player_hand)
        self.deal_card(self.dealer_hand)

    def play_dealer_hand(self):
        """Play the dealer's hand according to standard Spanish Blackjack rules."""
        while self.hand_value(self.dealer_hand) < 17:
            self.deal_card(self.dealer_hand)
        return self.hand_value(self.dealer_hand)
