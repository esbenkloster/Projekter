import random
import time

suits = ('Hjerter', 'Ruder', 'Spar', 'Klør')
ranks = ('To', 'Tre', 'Fire', 'Fem', 'Seks', 'Syv', 'Otte', 'Ni', 'Ti', 'Knægt', 'Dame', 'Konge', 'Es')
values = {
    'To': 2, 'Tre': 3, 'Fire': 4, 'Fem': 5, 'Seks': 6,
    'Syv': 7, 'Otte': 8, 'Ni': 9, 'Ti': 10,
    'Knægt': 10, 'Dame': 10, 'Konge': 10, 'Es': 11

}

deck = []
print("\nVelkommen til Blackjack!\n")
print("For at afslutte spillet når som helst, skriv 'q'. God fornøjelse!\n")
while True:
    num_players = input("Hvor mange spillere? ")
    if num_players.isdigit() and int(num_players) > 0:
        num_players = int(num_players)
        break
    else:
        print("Ugyldigt antal spillere. Prøv igen.")

chips = [100 for _ in range(num_players)]
for suit in suits:
    for rank in ranks:
        deck.append((rank, suit))

def shuffle_deck():
    print("Blander kortene...")
    time.sleep(2)
    random.shuffle(deck)

def quit_game():
    print("Tak for spillet! Farvel!")
    exit()

def deal_card():
    #Hivs bunken er tom
    if len(deck) == 0:
        print("Blander kortene...")
        time.sleep(2)
        for suit in suits:
            for rank in ranks:
                deck.append((rank, suit))
        shuffle_deck()
    return deck.pop()

def calculate_hand_value(hand):
    total = 0
    aces = 0
    for card in hand:
        rank = card[0]
        total += values[rank]
        if rank == 'Es':
            aces += 1
    # Es skal tælles som 1 hvis total > 21
    while total > 21 and aces > 0:
        total -= 10
        aces -= 1
    return total

def display_hand(hand, hide_first_card=False):
    if hide_first_card:
        cards = "[Skjult]"
        i = 1
        while i < len(hand):
            cards += ", " + hand[i][1] + " " + hand[i][0]
            i += 1
        return cards
    else:
        cards = ""
        i = 0
        while i < len(hand):
            if i > 0:
                cards += ", "
            cards += hand[i][1] + " " + hand[i][0]
            i += 1
        return cards
    
def play_blackjack():
    shuffle_deck()
    dealer_hand = [deal_card(), deal_card()]

    all_player_hands = []
    all_player_bets = []

    for i in range(num_players):
        print(f"\nSpiller {i+1}'s tur")
        print(f"Du har {chips[i]} chips.")

        if chips[i] <= 0:
            print("Du har ikke flere chips! Spillet er slut.")
            quit_game()

        bet = input(f"Placér dit bet (maks {chips[i]}): ")
        while True:
            if bet.lower() == 'q':
                quit_game()
            if bet.isdigit():
                b = int(bet)
                if b > 0 and b <= chips[i]:
                    bet = b
                    break
            bet = input(f"Ugyldigt beløb. Placér dit bet (maks {chips[i]}): ")

        time.sleep(1)
        print(f"\nDu har satset {bet} chips.")
        hand = [deal_card(), deal_card()]
        #hand = [('Syv', 'Spar'), ('Syv', 'Hjerter')]
        print(f"Din hånd: {display_hand(hand)} (Værdi: {calculate_hand_value(hand)})")
        time.sleep(1)
        all_player_hands.append(hand)
        all_player_bets.append(bet)

    print("\n\nDealerens hånd:", display_hand(dealer_hand, hide_first_card=True))
    time.sleep(2)

    # Spillerens tur
    all_final_hands = []
    all_final_bets = []
    for i in range(num_players):
        print(f"\nSpiller {i+1}'s tur ")
        print("Din hånd:", display_hand(all_player_hands[i]), "(Værdi:", calculate_hand_value(all_player_hands[i]), ")")
        bet = all_player_bets[i]
        did_split = False
        player_hands = []
        bets = []

        # Tjek om par
        if all_player_hands[i][0][0] == all_player_hands[i][1][0]:
            action = input("Du har et par! Vil du (d)ele, (h)it eller (s)tand? ").lower()
            time.sleep(1)

            if action == 'd':
                if chips[i] < bet:
                    print("Ikke nok chips til split. Fortsætter uden split.")

                    # Spil EN hånd færdig
                    while True:
                        hand_value = calculate_hand_value(all_player_hands[i])
                        print("\nDin hånd:", display_hand(all_player_hands[i]), "(Værdi:", hand_value, ")")
                        if hand_value >= 21:
                            break
                        action = input("Vil du (h)it eller (s)tand? ").lower()
                        time.sleep(1)

                        if action == 'h':
                            all_player_hands[i].append(deal_card())
                        elif action == 's':
                            break
                        elif action == 'q':
                            quit_game()
                    player_hands = [all_player_hands[i]]
                    bets = [bet]
                else:
                    chips[i] -= bet
                    did_split = True

                    # Lav to hænder og giv ét kort til hver
                    hand1 = [all_player_hands[i][0], deal_card()]
                    hand2 = [all_player_hands[i][1], deal_card()]

                    # Spil hånd 1 færdig
                    while True:
                        v1 = calculate_hand_value(hand1)
                        print("Første hånd:", display_hand(hand1), "(Værdi:", v1, ")")
                        if v1 >= 21:
                            break
                        a1 = input(" - (h)it eller (s)tand? ").lower()
                        if a1 == 'h':
                            hand1.append(deal_card())
                        elif a1 == 's':
                            break
                        elif a1 == 'q':
                            quit_game()

                    # Spil hånd 2 færdig
                    while True:
                        v2 = calculate_hand_value(hand2)
                        print("Anden hånd:", display_hand(hand2), "(Værdi:", v2, ")")
                        if v2 >= 21:
                            break
                        a2 = input(" - (h)it eller (s)tand? ").lower()
                        if a2 == 'h':
                            hand2.append(deal_card())
                        elif a2 == 's':
                            break
                        elif a2 == 'q':
                            quit_game()

                    player_hands = [hand1, hand2]
                    bets = [bet, bet]

            elif action == 'h':
                # Almindelig runde
                all_player_hands[i].append(deal_card())
                while True:
                    hand_value = calculate_hand_value(all_player_hands[i])
                    print("\nDin hånd:", display_hand(all_player_hands[i]), "(Værdi:", hand_value, ")")
                    if hand_value >= 21:
                        break
                    action = input("Vil du (h)it eller (s)tand? ").lower()
                    time.sleep(1)

                    if action == 'h':
                        all_player_hands[i].append(deal_card())
                    elif action == 's':
                        break
                    elif action == 'q':
                        quit_game()
                player_hands = [all_player_hands[i]]
                bets = [bet]

            elif action == 's':
                player_hands = [all_player_hands[i]]
                bets = [bet]

            elif action == 'q':
                quit_game()
            else:
                print("Ugyldigt valg. Prøv igen.")
                while True:
                    hand_value = calculate_hand_value(all_player_hands[i])
                    print("\nDin hånd:", display_hand(all_player_hands[i]), "(Værdi:", hand_value, ")")
                    if hand_value >= 21:
                        break
                    action = input("Vil du (h)it eller (s)tand? ").lower()
                    time.sleep(1)

                    if action == 'h':
                        all_player_hands[i].append(deal_card())
                    elif action == 's':
                        break
                    elif action == 'q':
                        quit_game()

                player_hands = [all_player_hands[i]]
                bets = [bet]
        else:
            # Ikke par
            if calculate_hand_value(all_player_hands[i]) == 21:
                print("Blackjack!")
                player_hands = [all_player_hands[i]]
                bets = [bet]
            else:
                action = input("Vil du (h)it eller (s)tand? ").lower()
                time.sleep(1)
                if action == 'h':
                    all_player_hands[i].append(deal_card())
                    while True:
                        hand_value = calculate_hand_value(all_player_hands[i])
                        print("\nDin hånd:", display_hand(all_player_hands[i]), "(Værdi:", hand_value, ")")
                        if hand_value > 21:
                            print("Du går over.")
                            break
                        if hand_value == 21:
                            print("Du har 21!")
                            break
                        action = input("Vil du (h)it eller (s)tand? ").lower()
                        time.sleep(1)
                        if action == 'h':
                            all_player_hands[i].append(deal_card())
                        elif action == 's':
                            break
                        elif action == 'q':
                            quit_game()
                elif action == 's':
                    player_hands = [all_player_hands[i]]
                    bets = [bet]

                elif action == 'q':
                    quit_game()
                else:
                    print("Ugyldigt valg. Prøv igen.")
                    while True:
                        hand_value = calculate_hand_value(all_player_hands[i])
                        print("\nDin hånd:", display_hand(all_player_hands[i]), "(Værdi:", hand_value, ")")
                        if hand_value >= 21:
                            break
                        action = input("Vil du (h)it eller (s)tand? ").lower()
                        time.sleep(1)
                        if action == 'h':
                            all_player_hands[i].append(deal_card())
                        elif action == 's':
                            break
                        elif action == 'q':
                            quit_game()
                player_hands = [all_player_hands[i]]
                bets = [bet]
        all_final_hands.append(player_hands)
        all_final_bets.append(bets)
    # Dealer spiller
    print("\nDealerens tur...")
    time.sleep(2)
    dealer_value = calculate_hand_value(dealer_hand)
    print("\nDealerens hånd (afslører kort):", display_hand(dealer_hand), "(Værdi:", dealer_value, ")")
    time.sleep(1)
    while dealer_value < 17:
        print("Dealer trækker et kort...")
        time.sleep(1)
        dealer_hand.append(deal_card())
        dealer_value = calculate_hand_value(dealer_hand)
        print("Dealerens hånd:", display_hand(dealer_hand), "(Værdi:", dealer_value, ")")

    print()
    time.sleep(1)

   # Resultater for hver spiller
    for i in range(num_players):
        print(f"\nResultater for Spiller {i+1}:")
        for hand_index, (hand, bet) in enumerate(zip(all_final_hands[i], all_final_bets[i]), start=1):
            hand_value = calculate_hand_value(hand)
            if hand_value > 21:
                print(f"Hånd {hand_index}: {display_hand(hand)} ({hand_value}) -> går over! Du taber {bet}.")
                chips[i] -= bet
            elif dealer_value > 21:
                print(f"Dealer går over. Du vinder {bet}!")
                chips[i] += bet
            elif hand_value > dealer_value:
                print(f"Hånd {hand_index}: {display_hand(hand)} ({hand_value}) > Dealer ({dealer_value}). Du vinder {bet}!")
                chips[i] += bet
            elif hand_value < dealer_value:
                print(f"Hånd {hand_index}: {display_hand(hand)} ({hand_value}) < Dealer ({dealer_value}). Du taber {bet}.")
                chips[i] -= bet
            else:
                print(f"Hånd {hand_index}: {display_hand(hand)} ({hand_value}) = Dealer ({dealer_value}). Uafgjort.")
        print(f"Du har nu {chips[i]} chips.")


if __name__ == "__main__":
    while True:
        play_blackjack()
        if all(c <= 0 for c in chips):
            print("Alle spillere har ikke flere chips! Spillet er slut.")
            break
        again = input("\nVil du/I spille igen? (j/n): ").lower()
        if again != 'j':
            print("Tak for spillet! Farvel!")
            break