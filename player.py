from .deck import Deck
from .constants import values
from API.mymongo import initiateMongoDB

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
        def __init__(self, total = 100):
            self.total = total
            self.bet = 0

        def win_bet(self):
            self.total += self.bet
        
        def lose_bet(self):
            self.total -= self.bet
            self.bet = 0

    def __init__(self, name, chips, wins=0, losses=0):
        self.name = name
        self.chips = Player.Chips(chips)
        self.wins = wins
        self.losses = losses
        self.hand = Player.Hand()

    def increment_wins(self):
        self.wins += 1

    def increment_losses(self):
        self.losses += 1
        
    def hit(self, deck):
        card = deck.deal()
        self.hand.add_card(card)

    async def end_game(self):
        mongo_handler = await initiateMongoDB()
        await mongo_handler.update_user(
            self.name,
            self.chips.total,
            self.wins,
            self.losses
        )