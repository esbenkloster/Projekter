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
chips = 100

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
    global chips

    if chips <= 0:
        print("Du har ikke flere chips! Spillet er slut.")
        quit_game()

    # Bet (tjek 'q' først)
    bet = input(f"Placér dit bet (maks {chips}): ")
    while True:
        if bet.lower() == 'q':
            quit_game()
        if bet.isdigit():
            b = int(bet)
            if b > 0 and b <= chips:
                bet = b
                break
        bet = input(f"Ugyldigt beløb. Placér dit bet (maks {chips}): ")

    print(f"Du har satset {bet} chips.\n")
    shuffle_deck()

    player_hand = [deal_card(), deal_card()]
    dealer_hand = [deal_card(), deal_card()]

    print("\nDin hånd:", display_hand(player_hand), "(Værdi:", calculate_hand_value(player_hand), ")")
    print("Dealerens hånd:", display_hand(dealer_hand, hide_first_card=True))

    did_split = False
    player_hands = []
    bets = []

    # Tjek om par
    if player_hand[0][0] == player_hand[1][0]:
        action = input("Du har et par! Vil du (d)ele, (h)it eller (s)tand? ").lower()

        if action == 'd':
            if chips - bet < 0:
                print("Ikke nok chips til split. Fortsætter uden split.")
                # Spil EN hånd færdig
                while True:
                    pv = calculate_hand_value(player_hand)
                    print("\nDin hånd:", display_hand(player_hand), "(Værdi:", pv, ")")
                    if pv >= 21:
                        break
                    a = input("Vil du (h)it eller (s)tand? ").lower()
                    if a == 'h':
                        player_hand.append(deal_card())
                    elif a == 's':
                        break
                    elif a == 'q':
                        quit_game()
                player_hands = [player_hand]
                bets = [bet]
            else:
                chips -= bet
                did_split = True

                # Lav to hænder og giv ét kort til hver
                hand1 = [player_hand[0], deal_card()]
                hand2 = [player_hand[1], deal_card()]

                # Spil hånd 1
                print("\nFørste hånd:", display_hand(hand1), "(Værdi:", calculate_hand_value(hand1), ")")
                while True:
                    v1 = calculate_hand_value(hand1)
                    print("Første hånd nu:", display_hand(hand1), "(Værdi:", v1, ")")
                    if v1 >= 21:
                        break
                    a1 = input("Hånd 1 - (h)it eller (s)tand? ").lower()
                    if a1 == 'h':
                        hand1.append(deal_card())
                    elif a1 == 's':
                        break
                    elif a1 == 'q':
                        quit_game()

                # Spil hånd 2
                print("\nAnden hånd:", display_hand(hand2), "(Værdi:", calculate_hand_value(hand2), ")")
                while True:
                    v2 = calculate_hand_value(hand2)
                    print("Anden hånd nu:", display_hand(hand2), "(Værdi:", v2, ")")
                    if v2 >= 21:
                        break
                    a2 = input("Hånd 2 - (h)it eller (s)tand? ").lower()
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
            player_hand.append(deal_card())
            while True:
                pv = calculate_hand_value(player_hand)
                print("\nDin hånd:", display_hand(player_hand), "(Værdi:", pv, ")")
                if pv >= 21:
                    break
                a = input("Vil du (h)it eller (s)tand? ").lower()
                if a == 'h':
                    player_hand.append(deal_card())
                elif a == 's':
                    break
                elif a == 'q':
                    quit_game()
            player_hands = [player_hand]
            bets = [bet]

        elif action == 's':
            player_hands = [player_hand]
            bets = [bet]

        elif action == 'q':
            quit_game()
        else:
            print("Ugyldigt valg. Fortsætter uden split.")
            while True:
                pv = calculate_hand_value(player_hand)
                print("\nDin hånd:", display_hand(player_hand), "(Værdi:", pv, ")")
                if pv >= 21:
                    break
                a = input("Vil du (h)it eller (s)tand? ").lower()
                if a == 'h':
                    player_hand.append(deal_card())
                elif a == 's':
                    break
                elif a == 'q':
                    quit_game()
            player_hands = [player_hand]
            bets = [bet]
    else:
        # Ikke par
        a = input("Vil du (h)it eller (s)tand? ").lower()
        if a == 'h':
            player_hand.append(deal_card())
            while True:
                pv = calculate_hand_value(player_hand)
                print("\nDin hånd:", display_hand(player_hand), "(Værdi:", pv, ")")
                if pv >= 21:
                    break
                a = input("Vil du (h)it eller (s)tand? ").lower()
                if a == 'h':
                    player_hand.append(deal_card())
                elif a == 's':
                    break
                elif a == 'q':
                    quit_game()
        elif a == 'q':
            quit_game()
        player_hands = [player_hand]
        bets = [bet]

    # Hvis alle hænder går over
    alle_over = True
    i = 0
    while i < len(player_hands):
        if calculate_hand_value(player_hands[i]) <= 21:
            alle_over = False
            break
        i += 1

    if alle_over:
        time.sleep(1)
        if did_split:
            print("\nBegge dine hænder gik over! Dealer vinder.")
        else:
            print("\nDu gik over! Dealer vinder.")
        i = 0
        while i < len(bets):
            chips -= bets[i]
            i += 1
        return

    # Dealer spiller
    print("\nDealerens tur...")
    time.sleep(2)
    dealer_value = calculate_hand_value(dealer_hand)
    print("\nDealerens hånd (afslører kort):", display_hand(dealer_hand), "(Værdi:", dealer_value, ")")

    while dealer_value < 17:
        print("Dealer trækker et kort...")
        time.sleep(2)
        dealer_hand.append(deal_card())
        dealer_value = calculate_hand_value(dealer_hand)
        print("Dealerens hånd:", display_hand(dealer_hand), "(Værdi:", dealer_value, ")")

    # Find vinder for hver hånd
    time.sleep(1)
    idx = 0
    while idx < len(player_hands):
        hand = player_hands[idx]
        b = bets[idx]
        pv = calculate_hand_value(hand)

        if pv > 21:
            print(f"Hånd {idx+1 if did_split else 1}: {display_hand(hand)} ({pv}) -> går over! Du taber {b}.")
            chips -= b
        elif dealer_value > 21:
            print(f"Dealer går over. Du vinder {b}!")
            chips += b
        elif pv > dealer_value:
            print(f"Hånd {idx+1 if did_split else 1}: {display_hand(hand)} ({pv}) > Dealer ({dealer_value}). Du vinder {b}!")
            chips += b
        elif pv < dealer_value:
            print(f"Hånd {idx+1 if did_split else 1}: {display_hand(hand)} ({pv}) < Dealer ({dealer_value}). Du taber {b}.")
            chips -= b
        else:
            print(f"Hånd {idx+1 if did_split else 1}: {display_hand(hand)} ({pv}) = Dealer ({dealer_value}). Uafgjort (push).")
        idx += 1

if __name__ == "__main__":
    print("Velkommen til Blackjack!\n")
    print("For at afslutte spillet når som helst, skriv 'q'. God fornøjelse!\n")
    print(f"Du starter med {chips} chips.\n")
    while True:
        play_blackjack()
        print(f"Du har nu {chips} chips.")
        if chips <= 0:
            print("Du har ikke flere chips! Spillet er slut.")
            break
        again = input("Vil du spille igen? (j/n): ").lower()
        if again != 'j':
            print("Tak for spillet! Farvel!")
            break