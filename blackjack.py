import os
from deck import Deck
from player import Player

def check_blackjack(hand):
    return hand.value == 21

def take_bet(chips):
    while True:
        try:
            bet = input(f'Place bet ({chips.total} Chips Left): ')
            if bet.lower() == "all":
                chips.bet = chips.total
            else:
                chips.bet = int(bet)
                if chips.bet > chips.total:
                    print("You cannot bet more chips than you have!")
                    continue
        except ValueError:
            print('Bet must be a digit, except for "all"!')
        else:
            chips.total -= chips.bet
            break

def hit(deck, hand):
    hand.add_card(deck.deal())
    hand.adjust_for_ace()

def hit_or_stand(deck, player, dealer):
    global playing  
    while True:
        x = input(f"{player.name}, would you like to Hit or Stand? ")
        
        if x[0].lower() == 'h':
            player.hit(deck)
            show_some(player, dealer)

            if player.hand.value == 21:
                show_all(player, dealer) 
                print(f"{player.name} has 21! BLACKJACK!")
                player_wins(player, dealer)  
                playing = False
                return 
            
            if player.hand.value > 21:
                player_busts(player, dealer)
                playing = False
                return

        elif x[0].lower() == 's':
            print(f"{player.name} stands. Dealer is playing.")
            playing = False
            return
        
        else:
            print("Sorry, please try again.")
            continue

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def show_some(player, dealer):
    clear_screen()
    yellow_color = "\033[1;33m"
    reset = "\033[0m"
    
    print(f"\n{yellow_color}Dealer's Hand (?):{reset}")
    hidden_card = [
        "|‾‾‾‾‾‾‾|",
        "|       |",
        "|       |",
        "|       |",
        "|_______|"
    ]
    
    dealer_card = dealer.hand.cards[1].physical_card()

    for line_hidden, line_visible in zip(hidden_card, dealer_card):
        print(line_hidden + ' ' + line_visible)

    print(f"\n{yellow_color}{player.name}'s Hand: ({player.hand.value}) \n\033[1;36mChips: {player.chips.total}{reset}")
    
    player_cards = [card.physical_card() for card in player.hand.cards]
    
    for i in range(len(player_cards[0])):
        print(' '.join(card[i] for card in player_cards))

def show_all(player, dealer):
    clear_screen()
    yellow_color = "\033[1;33m"
    reset = "\033[0m"

    print(f"\n{yellow_color}Dealer's Hand: ({dealer.hand.value}){reset}")
    
    dealer_cards = [card.physical_card() for card in dealer.hand.cards]
    
    for i in range(len(dealer_cards[0])):
        print(' '.join(card[i] for card in dealer_cards))

    print(f"\n{yellow_color}{player.name}'s Hand: ({player.hand.value}) \n\033[1;36mChips: {player.chips.total}{reset}")
    
    player_cards = [card.physical_card() for card in player.hand.cards]
    
    for i in range(len(player_cards[0])):
        print(' '.join(card[i] for card in player_cards))

def player_busts(player, dealer):
    orange_color = "\033[1;31m"
    reset = "\033[0m"
    
    player.chips.lose_bet()  
    show_all(player, dealer)
    
    print(f"\n{orange_color}{player.name} BUSTS!{reset}")

def player_wins(player, dealer):
    green_color = "\033[1;32m"
    reset = "\033[0m"
    
    player.chips.win_bet()   
    show_all(player, dealer)
    
    print(f"\n{green_color}{player.name} WINS!{reset}")

def dealer_busts(player, dealer):
    orange_color = "\033[1;31m"
    green_color = "\033[1;32m"
    reset = "\033[0m"
    
    player.chips.win_bet()  
    show_all(player, dealer)
    
    print(f"\n{orange_color}DEALER BUSTS!{reset}")
    print(f"\n{green_color}{player.name} WINS!{reset}")

def dealer_wins(player, dealer):
    orange_color = "\033[1;31m"
    reset = "\033[0m"
    
    player.chips.lose_bet()   
    show_all(player, dealer)
    
    print(f"\n{orange_color}{player.name} LOSES!{reset}")


def push(player,dealer):
    purple_color = "\033[1;35m"
    reset = "\033[0m"

    player.chips.total += player.chips.bet
    print(f"\n{purple_color}PUSH!\nYour bet of {player.chips.bet} has been returned.\nNow you have {player.chips.total} chips.{reset}")

def check_for_blackjack(hand):
    ranks_in_hand = [card.rank for card in hand.cards]
    
    if ('Ace' in ranks_in_hand and 
       any(rank in ranks_in_hand for rank in ['Ten', 'Jack', 'Queen', 'King'])):
           return True
           
    return False
print('Welcome to BlackJack!')

('\n' * 2)

name_input= input("Enter player's name: ")
player= Player(name_input)
dealer= Player("Dealer")

while True:   
    deck= Deck()
    deck.shuffle()

    player.hand = Player.Hand()
    dealer.hand = Player.Hand()

    playing = True

    if player.chips.total <= 0:
        print('You are out of chips! \nWould you like to start a new game?')
        new_game = input().strip().lower()
        if new_game[0] == 'y':
            player.chips.total = 100
            continue
        else:
            print("Thanks for playing! \nGOODBYE!!")
            break
   
    player.hit(deck)
    player.hit(deck)

    dealer.hit(deck)
    dealer.hit(deck)

    player.hand.adjust_for_ace()

    if player.hand.value > 21:
        player_busts(player, dealer)
        continue
        
    take_bet(player.chips)

    if check_blackjack(player.hand):
        show_all(player,dealer)
        print(f'{player.name} has 21! BLACKJACK!')
        player_wins(player, dealer)
        continue

    elif check_blackjack(dealer.hand):
        show_all(player,dealer)
        dealer_wins(player, dealer)
        continue

    else:
        show_some(player,dealer)

        while playing:
            hit_or_stand(deck, player, dealer)

            show_some(player,dealer)

            if player.hand.value > 21:
                player_busts(player,dealer)
                break

        if player.hand.value <= 21:
            while dealer.hand.value < 17:
                dealer.hit(deck)

            show_all(player,dealer)

            if dealer.hand.value > 21:
                dealer_busts(player, dealer)
            elif dealer.hand.value > player.hand.value:
                dealer_wins(player, dealer)  
            elif dealer.hand.value < player.hand.value:
                player_wins(player, dealer)   
            else:
                push(player, dealer)   

    if player.chips.total <= 0:
        print('You are out of chips! \nWould you like to start a new game?')
        new_game = input().strip().lower()
        if new_game[0] == 'y':
            player.chips.total = 100
            continue
        else:
            print("\033[1;34mThanks for playing! \nGOODBYE!!\033[0m")
            break

    playing = True