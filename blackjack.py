import random


class Blackjack:
    def __init__(self, decks=8, pen=0.8125, burn=False):
        self.deck = Deck(decks=decks)
        self.deck.shuffle()
        self.player = []
        self.dealer = []
        self.player_bal = 0

    def deal(self):
        self.player.append(self.deck.draw())
        self.dealer.append(self.deck.draw())
        self.player.append(self.deck.draw())
        self.dealer.append(self.deck.draw())

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
        score, _ = self.__score(self.player)
        return score

    def dealer_score(self):
        score, _ = self.__score(self.dealer)
        return score

    def player_draw(self):
        self.player.append(self.deck.draw())

    def dealer_draw(self):
        while self.dealer_score() < 17:
            self.dealer.append(self.deck.draw())

    def dealer_soft(self):
        _, ace = self.__score(self.dealer)
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

        self.player = []
        self.dealer = []
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
    def __init__(self, decks=8, pen=0.8125, burn=False):
        self.cards = []
        self.decks = decks
        self.pen = pen
        self.burn = burn
        for i in range(1, 14):
            self.cards.extend([i] * 4 * decks)

    def shuffle(self, burn=False):
        random.shuffle(self.cards)
        if burn:
            self.cards.pop()

    def draw(self):
        return self.cards.pop()

    def __len__(self):
        return len(self.cards)

    def check(self):
        return len(self) < 52 * self.decks * 0.8125
