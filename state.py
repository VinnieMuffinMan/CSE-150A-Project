import numpy as np
from bj_utils import score


class State:
    def __init__(
        self, not_seen=None, player_hand=None, dealer_hand=None, decks=8, burn=True
    ):
        """
        Initializes the game state.

        Args:
            not_seen (np.ndarray, optional): Array representing unseen cards (index 0 = A, index 1 = 2, ..., index 9 = 10 + face cards).
            player_hand (list[int], optional): The player's hand.
            dealer_hand (list[int], optional): The dealer's hand.
            decks (int, optional): Number of decks used in the game (default: 8).
            burn (bool, optional): Indicates if a burn card was used (default: True).
        """
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
        """
        Calculates the number of remaining cards in the deck.

        Returns:
            int: The number of remaining cards in the deck.
        """
        seen_count = 0
        for k in self.seen.keys():
            seen_count += self.seen[k]
        return 52 * self.decks - self.burn - seen_count

    def player_score(self):
        """
        Calculates the player's hand score.

        Returns:
            int: The player's score.
        """
        sc, _ = score(self.player_hand)
        return sc

    def dealer_score(self):
        """
        Calculates the dealer's hand score.

        Returns:
            int: The dealer's score.
        """
        sc, _ = score(self.dealer_hand)
        return sc

    def update_hand(self, player, dealer):
        """
        Updates the state with a new player and dealer hand and updates unseen cards.

        Args:
            player (list[int]): The player's new hand.
            dealer (list[int]): The dealer's new hand.
        """
        player = [10 if card > 10 else card for card in player]
        dealer = [10 if card > 10 else card for card in dealer]
        for card in player:
            self.not_seen[card - 1] -= 1
        for card in dealer:
            self.not_seen[card - 1] -= 1
        self.player_hand = player
        self.dealer_hand = dealer

    def update_player_hand(self, card):
        """
        Updates the player's hand when they draw a card.

        Args:
            card (int): The drawn card.
        """
        card = 10 if card > 10 else card
        self.player_hand.append(card)
        self.not_seen[card - 1] -= 1

    def update_dealer_hand(self, cards):
        """
        Updates the dealer's hand when they draw cards.

        Args:
            card (int): The drawn cards.
        """
        cards = [10 if card > 10 else card for card in cards]
        self.dealer_hand += cards
        for card in cards:
            self.not_seen[card - 1] -= 1

    def not_seen_reset(self):
        """
        Resets the unseen cards when the deck is shuffled.
        """
        self.not_seen = np.full(10, self.decks * 4)
        self.not_seen[-1] = self.decks * 16
