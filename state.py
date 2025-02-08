import numpy as np
from bj_utils import score


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

    def player_score(self):
        sc, _ = score(self.player_hand)
        return sc

    def dealer_score(self):
        sc, _ = score(self.dealer_hand)
        return sc

    def not_seen(self):
        not_seen = np.full(10, self.decks * 4)
        not_seen[-1] = self.decks * 16
        return not_seen - self.seen

    def update_hand(self, player, dealer):
        player = [10 if card > 10 else card for card in player]
        dealer = [10 if card > 10 else card for card in dealer]
        for card in player:
            self.seen[card - 1] += 1
        for card in dealer:
            self.seen[card - 1] += 1
        self.player_hand = player
        self.dealer_hand = dealer
