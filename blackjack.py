import numpy as np
from bj_utils import score


class Blackjack:
    def __init__(self, decks=8, pen=0.8125, burn=False, seed=None, bal=0):
        self.deck = Deck(decks=decks, seed=seed)
        self.deck.shuffle()
        self.player = []
        self.dealer = []
        self.bal = bal

    def deal(self):
        self.player = []
        self.dealer = []
        self.player.append(self.deck.draw())
        self.dealer.append(self.deck.draw())
        self.player.append(self.deck.draw())
        self.dealer.append(self.deck.draw())
        self.bal -= 1

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

    def player_hit(self):
        return self.player_draw()

    def player_double(self):
        self.bal -= 1
        return self.player_draw()

    def cards_left(self):
        return len(self.deck)

    def player_action(self, action):
        match action:
            case "hit":
                self.player_hit()
                return 1 if self.player_score()[0] >= 21 else 0
            case "stand":
                return 1
            case "double":
                self.player_double()
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
        if self.deck.check():
            self.deck = Deck(decks=self.deck.decks, pen=self.deck.pen, burn=True)
            print("Shuffling...")
            self.deck.shuffle()

        self.deal()
        print(
            f"Player: {self.player} ({self.player_score()[0]}) Bal: {self.bal}"
        )
        if self.player_score()[0] == 21:
            if self.dealer_score()[0] == 21:
                print(f"Dealer: {self.dealer} ({self.dealer_score()[0]})")
                print("It's a tie.")
                self.bal += 1
            else:
                print(f"Dealer: {self.dealer[0]}")
                print("Player wins.")
                self.bal += 2.5
            return
        if self.dealer_score()[0] == 21:
            print(f"Dealer: {self.dealer} ({self.dealer_score()[0]})")
            print("Dealer wins.")
            return
        print(f"Dealer: {self.dealer[0]}")

        while True:
            action = input("Action (hit, stand, double, split, surrender): ")
            act = self.player_action(action)
            if act != 0:
                break
            print(f"Player: {self.player} ({self.player_score()[0]})")
            print(f"Dealer: {self.dealer[0]}")

        if self.player_score()[0] > 21:
            print("Player busts! Dealer wins.")
            return

        self.dealer_action()

        print(f"Dealer: {self.dealer} ({self.dealer_score()[0]})")
        if self.dealer_score()[0] > 21:
            print("Dealer busts! Player wins.")
            self.bal += 4 if act == 2 else 2
            return

        if self.player_score()[0] > self.dealer_score()[0]:
            self.bal += 4 if act == 2 else 2
            print("Player wins.")
        elif self.player_score()[0] < self.dealer_score()[0]:
            print("Dealer wins.")
        else:
            print("It's a tie.")
            self.bal += 2 if act == 2 else 1


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
