from deck import Deck
from constants import values

class Player:
    class Hand:
        def __init__(self):
            self.cards = [] 
            self.value = 0  
            self.aces = 0  

        def add_card(self, card):
            self.cards.append(card)
            self.value += values[card.rank]
            if card.rank == 'Ace':
                self.aces += 1  

        def adjust_for_ace(self):
            while self.value > 21 and self.aces:
                self.value -= 10
                self.aces -= 1 

    class Chips:
        def __init__(self):
            self.total = 100 
            self.bet = 0

        def win_bet(self):
            self.total += self.bet * 2 
        
        def lose_bet(self):
            pass

    def __init__(self, name):
        self.name = name
        self.chips = Player.Chips()
        self.hand = Player.Hand()

    def hit(self, deck):
        card = deck.deal()
        self.hand.add_card(card)