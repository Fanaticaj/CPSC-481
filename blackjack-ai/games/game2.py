import random

class Blackjack:
    def __init__(self, spanish=False):
        self.spanish = spanish
        self.deck = self.create_deck()
        self.player_hand = []
        self.dealer_hand = []

    def create_deck(self):
        deck = []
        values = [2, 3, 4, 5, 6, 7, 8, 9, 11] if self.spanish else [2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
        suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
        for value in values:
            for suit in suits:
                deck.append((value, suit))
        return deck * 4  # Multiply by 4 for four suits

    def new_game(self):
        self.deck = self.create_deck()
        random.shuffle(self.deck)
        self.player_hand = [self.deal_card(), self.deal_card()]
        self.dealer_hand = [self.deal_card(), self.deal_card()]

    def deal_card(self, hand=None):
        card = self.deck.pop()
        if hand is not None:
            hand.append(card)
        return card

    def hand_value(self, hand):
        value = 0
        ace_count = 0
        for card in hand:
            card_value = card[0]
            if card_value == 11:  # Ace
                ace_count += 1
            value += min(card_value, 10)
        while ace_count > 0 and value + 10 <= 21:
            value += 10
            ace_count -= 1
        return value

    def check_winner(self):
        player_val = self.hand_value(self.player_hand)
        dealer_val = self.hand_value(self.dealer_hand)

        if player_val > 21:
            return "Player Busts! Dealer Wins!"
        elif dealer_val > 21:
            return "Dealer Busts! Player Wins!"
        elif player_val > dealer_val:
            return "Player Wins!"
        elif dealer_val > player_val:
            return "Dealer Wins!"
        else:
            return "It's a Draw!"


class SpanishBlackjack(Blackjack):
    def __init__(self):
        super().__init__(spanish=True)
    
    def check_special_payout(self, hand):
        hand_value = self.hand_value(hand)
        if hand_value == 21:
            if len(hand) >= 7:
                return "7+ Card 21! Pays 3-1"
            elif len(hand) == 6:
                return "6 Card 21! Pays 2-1"
            elif len(hand) == 5:
                return "5 Card 21! Pays 3-2"
        
        # Check for special 6-7-8 and 7-7-7 combinations
        if self.check_678(hand):
            return self.check_678(hand)
        if self.check_777(hand):
            return self.check_777(hand)
        
        return None
    
    def check_678(self, hand):
        values = [card[0] for card in hand]
        if sorted(values) == [6, 7, 8]:
            suits = [card[1] for card in hand]
            if len(set(suits)) == 1:  # All cards have the same suit
                if suits[0] == 'Spades':
                    return "6-7-8 Spaded! Pays 3-1"
                else:
                    return "6-7-8 Suited! Pays 2-1"
            else:
                return "6-7-8 Mixed! Pays 3-2"
        return False

    def check_777(self, hand):
        values = [card[0] for card in hand]
        if values.count(7) == 3:
            suits = [card[1] for card in hand]
            if len(set(suits)) == 1:  # All cards have the same suit
                if suits[0] == 'Spades':
                    return "7-7-7 Spaded! Pays 3-1"
                else:
                    return "7-7-7 Suited! Pays 2-1"
            else:
                return "7-7-7 Mixed! Pays 3-2"
        return False
