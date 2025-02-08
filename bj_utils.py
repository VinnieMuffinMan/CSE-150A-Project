def score(hand):
    ace = 0
    score = 0
    for card in hand:
        if card == 1:
            ace += 1
        score += 11 if card == 1 else min(card, 10)
    while ace > 0 and score > 21:
        score -= 10
        ace -= 1
    return score, ace

