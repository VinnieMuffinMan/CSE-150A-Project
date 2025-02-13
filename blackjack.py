import random
from bj_utils import score


class Blackjack:
    def __init__(self, decks=8, pen=0.8125, burn=False, seed=0):
        random.seed(seed)
        self.deck = Deck(decks=decks)
        self.deck.shuffle()
        self.player = []
        self.dealer = []
        self.player_bal = 0

    def deal(self):
        self.player = []
        self.dealer = []
        self.player.append(self.deck.draw())
        self.dealer.append(self.deck.draw())
        self.player.append(self.deck.draw())
        self.dealer.append(self.deck.draw())

    def player_score(self):
        sc, _ = score(self.player)
        return sc

    def dealer_score(self):
        sc, _ = score(self.dealer)
        return sc

    def player_draw(self):
        self.player.append(self.deck.draw())

    def dealer_draw(self):
        while self.dealer_score() < 17:
            self.dealer.append(self.deck.draw())

    def dealer_soft(self):
        _, ace = score(self.dealer)
        return ace > 0

    def cards_left(self):
        return len(self.deck)

    def player_action(self, action):
        match action:
            case "hit":
                self.player_draw()
                return 1 if self.player_score() >= 21 else 0
            case "stand":
                return 1
            case "double":
                self.player_draw()
                return 1
            case "split":
                return 2
            case "surrender":
                return -1
            case _:
                raise ValueError("Invalid action")

    def dealer_action(self):
        while self.dealer_score() < 17 or self.dealer_soft():
            self.dealer.append(self.deck.draw())

    def game(self):
        if self.deck.check():
            self.deck = Deck(decks=self.deck.decks, pen=self.deck.pen, burn=True)
            print("Shuffling...")
            self.deck.shuffle()

        self.deal()
        print(f"Player: {self.player} ({self.player_score()})")
        if self.player_score() == 21:
            if self.dealer_score() == 21:
                print(f"Dealer: {self.dealer} ({self.dealer_score()})")
                print("It's a tie.")
            else:
                print(f"Dealer: {self.dealer[0]}")
                print("Player wins.")
            return
        if self.dealer_score() == 21:
            print(f"Dealer: {self.dealer} ({self.dealer_score()})")
            print("Dealer wins.")
            return
        print(f"Dealer: {self.dealer[0]}")

        action = input("Action (hit, stand, double, split, surrender): ")
        while self.player_action(action) == 0:
            print(f"Player: {self.player} ({self.player_score()})")
            print(f"Dealer: {self.dealer[0]}")
            action = input("Action (hit, stand, double, split, surrender): ")

        if self.player_score() > 21:
            print("Player busts! Dealer wins.")
            return

        self.dealer_action()

        print(f"Dealer: {self.dealer} ({self.dealer_score()})")
        if self.dealer_score() > 21:
            print("Dealer busts! Player wins.")
            return
        if self.player_score() > self.dealer_score():
            print("Player wins.")
        elif self.player_score() < self.dealer_score():
            print("Dealer wins.")
        else:
            print("It's a tie.")


class Deck:
    def __init__(self, cards=None, decks=8, pen=0.8125, burn=False):
        if not cards:
            cards = []
        self.cards = cards
        self.decks = decks
        self.pen = pen
        self.burn = burn
        for i in range(1, 14):
            self.cards.extend([i] * 4 * decks)
        self.pos = 52 * self.decks - 1

    def shuffle(self, burn=False):
        random.shuffle(self.cards)
        if burn:
            self.draw()

    def draw(self):
        self.pos -= 1
        return self.cards[self.pos + 1]

    def peek(self):
        return self.cards[self.pos]

    def __len__(self):
        return self.pos + 1

    def check(self):
        return len(self) < 52 * self.decks * 0.8125
