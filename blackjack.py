import numpy as np
from bj_utils import score


class Blackjack:
    def __init__(self, decks=8, pen=0.8125, burn=False, seed=None, bal=0):
        self.deck = Deck(decks=decks, seed=seed)
        self.deck.shuffle()
        self.player = []
        self.dealer = []
        self.bal = bal
        self.bet = 1

    def deal(self):
        self.player = []
        self.dealer = []
        self.player.append(self.deck.draw())
        self.dealer.append(self.deck.draw())
        self.player.append(self.deck.draw())
        self.dealer.append(self.deck.draw())
        self.bal -= self.bet

    def player_score(self):
        sc, ace = score(self.player)
        return sc, ace

    def dealer_score(self):
        sc, ace = score(self.dealer)
        return sc, ace

    def player_draw(self):
        card = self.deck.draw()
        self.player.append(card)
        return card

    def hit(self):
        return self.player_draw()

    def double(self):
        self.bal -= self.bet
        return self.player_draw()

    def surrender(self):
        self.bal += 0.5 * self.bet

    def cards_left(self):
        return len(self.deck)

    def player_action(self, action):
        match action:
            case "hit":
                self.hit()
                return 1 if self.player_score()[0] >= 21 else 0
            case "stand":
                return 1
            case "double":
                self.double()
                return 2
            case "split":
                return 3
            case "surrender":
                return -1
            case _:
                raise ValueError("Invalid action")

    def dealer_action(self):
        dealer_score, ace = self.dealer_score()
        while dealer_score < 17 or (dealer_score == 17 and ace):
            self.dealer.append(self.deck.draw())
            dealer_score, ace = self.dealer_score()

    def game(self):
        if self.check_deck_pen():
            print("Shuffling...")
        self.deal()
        print(f"Player: {self.player} ({self.player_score()[0]}) Bal: {self.bal}")

        start_check = self.start_check()
        if start_check == 1:
            print(f"Dealer: {self.dealer}")
            print("Player blackjack.")
            return
        if start_check == 2:
            print(f"Dealer: {self.dealer}")
            print("Dealer blackjack.")
            return
        if start_check == 3:
            print(f"Dealer: {self.dealer} ({self.dealer_score()[0]})")
            print("It's a tie.")
            return

        print(f"Dealer: {self.dealer[0]}")

        while True:
            action = input("Action (hit, stand, double, split, surrender): ")
            act = self.player_action(action)
            if act != 0:
                break
            print(f"Player: {self.player} ({self.player_score()[0]})")
            print(f"Dealer: {self.dealer[0]}")

        if act == -1:
            print("Surrender.")
            self.surrender()
            print(f"Dealer: {self.dealer} ({self.dealer_score()[0]})")
            return

        end = self.end_check(act)
        print(f"Dealer: {self.dealer} ({self.dealer_score()[0]})")

        match end:
            case 0:
                print("Player wins.")
            case 1:
                print("Dealer wins.")
            case 2:
                print("It's a tie.")
            case 3:
                print("Player busts! Dealer wins.")
            case 4:
                print("Dealer busts! Player wins.")

    def check_deck_pen(self):
        """
        Checks if the deck is sufficiently depleted.

        Returns:
            bool: True if shuffling, False otherwise.
        """
        if self.deck.check():
            self.deck = Deck(decks=self.deck.decks, pen=self.deck.pen, burn=True)
            self.deck.shuffle()
            return True
        return False

    def start_check(self):
        """
        Checks for blackjacks at start of game.

        Returns:
            int: 1 if player blackjack, 2 if dealer blackjack, 3 if tie, 0 otherwise.
        """
        if self.player_score()[0] == 21:
            if self.dealer_score()[0] == 21:
                self.bal += self.bet
                return 3
            else:
                self.bal += 2.5 * self.bet
                return 1
        if self.dealer_score()[0] == 21:
            return 2
        return 0

    def end_check(self, act):
        """
        Checks winner of the game.

        Returns:
            int: 0 if player wins, 1 if dealer wins, 2 if tie, 3 if player busts, 4 if dealer busts.
        """
        player_score, _ = self.player_score()
        if player_score > 21:
            print("Player busts! Dealer wins.")
            return 3

        self.dealer_action()
        dealer_score, _ = self.dealer_score()

        if dealer_score > 21:
            self.bal += (4 if act == 2 else 2) * self.bet
            return 4
        if player_score > dealer_score:
            self.bal += (4 if act == 2 else 2) * self.bet
            return 0
        if player_score < dealer_score:
            return 1
        self.bal += (2 if act == 2 else 1) * self.bet
        return 2


class Deck:
    def __init__(self, cards=None, decks=8, pen=0.8125, burn=False, seed=None):
        if cards is None:
            cards = np.array([i for i in range(1, 14) for _ in range(4 * decks)])
        else:
            cards = np.array(cards)
        if seed is not None:
            np.random.seed(seed)
        self.cards = cards
        self.decks = decks
        self.pen = pen
        self.burn = burn
        self.pos = 52 * self.decks - 1

    def shuffle(self, burn=False):
        np.random.shuffle(self.cards)
        self.pos = len(self.cards) - 1
        if burn:
            self.draw()

    def draw(self):
        if self.pos < 0:
            raise IndexError("No cards left in the deck.")
        card = self.cards[self.pos]
        self.pos -= 1
        return card

    def peek(self):
        if self.pos < 0:
            raise IndexError("No cards left in the deck.")
        return self.cards[self.pos]

    def __len__(self):
        return self.pos + 1

    def check(self):
        return len(self) < len(self.cards) * (1 - self.pen)
