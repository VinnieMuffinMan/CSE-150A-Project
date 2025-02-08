def score(hand):
    ace = 0
    sc = 0
    for card in hand:
        if card == 1:
            ace += 1
        sc += 11 if card == 1 else min(card, 10)
    while ace > 0 and sc > 21:
        sc -= 10
        ace -= 1
    return sc, ace

