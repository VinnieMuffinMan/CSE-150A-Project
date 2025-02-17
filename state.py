import numpy as np
from bj_utils import score


class State:
    def __init__(
        self, not_seen=None, player_hand=None, dealer_hand=None, decks=8, burn=True
    ):
        self.decks = decks
        if not not_seen:
            not_seen = np.full(10, self.decks * 4)
            not_seen[-1] = self.decks * 16
        if not player_hand:
            player_hand = []
        if not dealer_hand:
            dealer_hand = []

        self.not_seen = not_seen
        self.player_hand = player_hand
        self.dealer_hand = dealer_hand
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

    def update_hand(self, player, dealer):
        player = [10 if card > 10 else card for card in player]
        dealer = [10 if card > 10 else card for card in dealer]
        for card in player:
            self.not_seen[card - 1] -= 1
        for card in dealer:
            self.not_seen[card - 1] -= 1
        self.player_hand = player
        self.dealer_hand = dealer

    def update_player_hand(self, card):
        card = 10 if card > 10 else card
        self.player_hand.append(card)
        self.not_seen[card - 1] -= 1
        
    def update_dealer_hand(self, cards):
        cards = [10 if card > 10 else card for card in cards]
        self.dealer_hand += cards
        for card in cards:
            self.not_seen[card - 1] -= 1