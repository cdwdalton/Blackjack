import os
from .deck import Deck
from .player import Player
from API.mymongo import initiateMongoDB

def check_blackjack(hand):
    return hand.value == 21

def take_bet(chips):
    while True:
        try:
            bet = input(f'Place bet or save game ({chips.total} Chips): ')
            if bet.lower() == "save":
                return 'save'
            elif bet.lower() == "all":
                chips.bet = chips.total
            else:
                chips.bet = int(bet)
                if chips.bet > chips.total:
                    print("You cannot bet more chips than you have!")
                    continue
        except ValueError:
            print('Bet must be a digit, except for "all" or "save"!') 
        else:
            break

def hit(deck, hand):
    hand.add_card(deck.deal())
    hand.adjust_for_ace()

def hit_or_stand(deck, player, dealer):
    while True:
        x = input(f"{player.name}, would you like to Hit or Stand?: ").strip().lower()
        
        if x[0].lower() == 'h':
            player.hit(deck)
            show_some(player, dealer)

            if player.hand.value == 21:
                show_all(player, dealer) 
                print(f"{player.name} has 21! BLACKJACK!")
                player_wins(player, dealer)  
                return False
            
            if player.hand.value > 21:
                player_busts(player, dealer)
                return False

        elif x[0].lower() == 's':
            print(f"{player.name} stands. Dealer is playing.")
            return False
        
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
    show_all(player, dealer)
    player.increment_losses()
    player.chips.lose_bet()
    print(f"\n{orange_color}{player.name} BUSTS!{reset}")
    display_wins_losses(player)

async def player_wins(player, dealer):
    green_color = "\033[1;32m"
    reset = "\033[0m"
    show_all(player, dealer)
    player.increment_wins()
    player.chips.win_bet()
    await end_game(player)  
    print(f"\n{green_color}{player.name} WINS!{reset}")
    display_wins_losses(player)

def dealer_busts(player, dealer):
    green_color = "\033[1;32m"
    reset = "\033[0m"
    player.chips.win_bet()  
    show_all(player, dealer)
    print(f"\n{green_color}{player.name} WINS!{reset}")
    player.increment_wins()
    display_wins_losses(player)

def dealer_wins(player, dealer):
    orange_color = "\033[1;31m"
    reset = "\033[0m"
    player.chips.lose_bet()   
    show_all(player, dealer)
    print(f"\n{orange_color}{player.name} LOSES!{reset}")
    player.increment_losses()
    display_wins_losses(player)

def push(player, dealer):
    purple_color = "\033[1;35m"
    reset = "\033[0m"
    print(f"\n{purple_color}PUSH!\nYour bet of {player.chips.bet} has been returned.\nNow you have {player.chips.total} chips.{reset}")
    display_wins_losses(player)

def display_wins_losses(player):
    print(f"\nWins: {player.wins}, Losses: {player.losses}\n")

def check_for_blackjack(hand):
    ranks_in_hand = [card.rank for card in hand.cards]
    if ('Ace' in ranks_in_hand and 
       any(rank in ranks_in_hand for rank in ['Ten', 'Jack', 'Queen', 'King'])):
           return True
    return False

async def end_game(player):
    mongo_handler = await initiateMongoDB()
    await mongo_handler.update_user(player.name, player.chips.total, player.wins, player.losses)
    print(f"{player.name}'s game ended. DATA SAVED. Wins: {player.wins}, Losses: {player.losses}")

async def start_game(player):
    global john_player

    mongo_handler = await initiateMongoDB()
    john_data = await mongo_handler.check_and_create_user(player.name)

    john_player = Player(
        name=john_data["name"],
        chips=john_data["chips"] 
    )
    john_player.wins = john_data.get("wins", 0)
    john_player.losses = john_data.get("losses", 0)

    dealer = Player("Dealer", chips=100)

    print('Welcome to BlackJack!')
    print(f"Starting the game for {john_player.name} with {john_player.chips.total} chips.")

    ('\n' * 2)

    while True:   
        deck = Deck()
        deck.shuffle()

        john_player.hand = Player.Hand()
        dealer.hand = Player.Hand()

        playing = True

        if john_player.chips.total <= 0:
            print('You are out of chips! \nWould you like to start a new game?')
            new_game = input().strip().lower()
            if new_game[0] == 'y':
                john_player.chips.total = 100
                continue
            else:
                print("Thanks for playing! \nGOODBYE!!")
                break
    
        john_player.hit(deck)
        john_player.hit(deck)

        dealer.hit(deck)
        dealer.hit(deck)

        john_player.hand.adjust_for_ace()

        if john_player.hand.value > 21:
            player_busts(john_player, dealer)
            await end_game(john_player)
            continue
            
        bet_option = take_bet(john_player.chips)
        if bet_option == 'save':
            await end_game(john_player)
            print(f"{john_player.name}'s game ended. DATA SAVED.")
            return

        if check_blackjack(john_player.hand):
            show_all(john_player, dealer)
            print(f'{john_player.name} has 21! BLACKJACK!')
            await player_wins(john_player, dealer)
            continue

        elif check_blackjack(dealer.hand):
            show_all(john_player, dealer)
            dealer_wins(john_player, dealer)
            continue

        else:
            show_some(john_player, dealer)

            while playing:
                playing = hit_or_stand(deck, john_player, dealer) 

                if john_player.hand.value > 21: 
                    break

        if john_player.hand.value <= 21:
            while dealer.hand.value < 17:
                dealer.hit(deck)

            show_all(john_player, dealer)

            if dealer.hand.value > 21:
                dealer_busts(john_player, dealer)
            elif dealer.hand.value > john_player.hand.value:
                dealer_wins(john_player, dealer)  
            elif dealer.hand.value < john_player.hand.value:
                await player_wins(john_player, dealer)   
            else:
                push(john_player, dealer) 

        if john_player.chips.total <= 0:
            print('You are out of chips! \nWould you like to start a new game?')
            new_game = input().strip().lower()
            if new_game[0] == 'y':
                john_player.chips.total = 100
                continue
            else:
                print("Thanks for playing! \nGOODBYE!!")
                break

        input("Press Enter to play again.")
