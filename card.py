from constants import values

class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        
    def __str__(self):
        return self.rank + ' of ' + self.suit
    
    def physical_card(self):
        suit_symbol = {'Hearts':'♥', 'Diamonds':'♦', 
                       'Spades':'♠', 'Clubs':'♣'}
        if self.rank in ['Jack', 'Queen', 'King', 'Ace']:
            rank_display = self.rank[0]
        else:
            rank_display = str(values[self.rank])

        red_colour = "\033[1;31m"
        black_colour = "\033[1;30m"
        reset = "\033[0m"

        if self.suit in ["Hearts", "Diamonds"]:
            suit_colour = red_colour
            rank_colour = red_colour
        else:
            suit_colour = black_colour
            rank_colour = black_colour
        
        card_lines = [
            f"|‾‾‾‾‾‾{rank_colour}{rank_display}{reset}|",
            f"| |‾‾‾| |",
            f"|   {suit_colour}{suit_symbol[self.suit]}{reset}   |",
            f"| |___| |",
            f"|{rank_colour}{rank_display}{reset}______|"
        ]
        return card_lines