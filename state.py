import numpy as np


class State:
    def __init__(
        self, seen=None, player_hand=None, dealer_hand=None, decks=8, burn=True
    ):
        if not seen:
            seen = np.zeros(10)
        if not player_hand:
            player_hand = []
        if not dealer_hand:
            dealer_hand = []

        self.seen = seen
        self.player_hand = player_hand
        self.dealer_hand = dealer_hand
        self.decks = decks
        self.burn = burn

    def get_cards_left(self):
        seen_count = 0
        for k in self.seen.keys():
            seen_count += self.seen[k]
        return 52 * self.decks - self.burn - seen_count

    def __score(self, hand):
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

    def player_score(self):
        score, _ = self.__score(self.player_hand)
        return score

    def dealer_score(self):
        score, _ = self.__score(self.dealer_hand)
        return score

    def not_seen(self):
        not_seen = np.full(10, self.decks * 4)
        return not_seen - self.seen

    def update_hand(self, player, dealer):
        for card in player:
            self.seen[card - 1] += 1
        for card in dealer:
            self.seen[card - 1] += 1
        self.player_hand = player
        self.dealer_hand = dealer
