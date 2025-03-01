import numpy as np
from bj_utils import score


class Blackjack:
    def __init__(self, decks=8, pen=0.8125, burn=False, seed=None, bal=0):
        """
        Initializes the Blackjack game.

        Args:
            decks (int, optional): Number of decks used (default: 8).
            pen (float, optional): Penetration percentage before reshuffling (default: 0.8125).
            burn (bool, optional): Whether to burn a card after shuffling (default: False).
            seed (int, optional): Random seed for deck shuffling.
            bal (float, optional): Player's starting balance (default: 0).
        """
        self.deck = Deck(decks=decks, seed=seed)
        self.deck.shuffle()
        self.player = []
        self.split_limit = 3
        self.split_hands = []
        self.split_acts = [0] * (self.split_limit + 1)
        self.dealer = []
        self.bal = bal
        self.bet = 1

    def deal(self):
        """
        Deals two cards to both player and dealer and adjusts the balance by the bet.
        """
        self.player = []
        self.dealer = []
        self.split_hands = []
        self.player.append(self.deck.draw())
        self.dealer.append(self.deck.draw())
        self.player.append(self.deck.draw())
        self.dealer.append(self.deck.draw())
        self.bal -= self.bet

    def player_score(self):
        """
        Calculates the player's hand score.

        Returns:
            tuple: The player's score and the number of aces in hand.
        """
        sc, ace = score(self.player)
        return sc, ace

    def dealer_score(self):
        """
        Calculates the dealer's hand score.

        Returns:
            tuple: The dealer's score and the number of aces in hand.
        """
        sc, ace = score(self.dealer)
        return sc, ace

    def player_draw(self):
        """
        Draws a card for the player.

        Returns:
            int: The drawn card.
        """
        card = self.deck.draw()
        self.player.append(card)
        return card

    def hit(self):
        """
        Allows player to hit by drawing a card.

        Returns:
            int: The drawn card.
        """
        return self.player_draw()

    def double(self):
        """
        Doubles the bet and draws a card for the player.

        Returns:
            int: The drawn card.
        """
        self.bal -= self.bet
        return self.player_draw()

    def split(self):
        """
        Splits the player's hand into two hands.
        """
        self.bal -= self.bet
        self.split_hands.append([self.player[0]])
        self.split_hands.append([self.player[0]])

    def surrender(self):
        """
        Allows player to surrender this game.
        """
        self.bal += 0.5 * self.bet

    def cards_left(self):
        """
        Returns the number of cards left in the deck.

        Returns:
            int: The number of cards left in the deck.
        """
        return len(self.deck)

    def player_action(self, action):
        """
        Maps the given action to an integer.

        Returns:
            int: 0 for hit, 1 for stand, 2 for double, 3 for split, -1 for surrender.
        """
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
                self.split()
                return 3
            case "surrender":
                return -1
            case _:
                raise ValueError("Invalid action")

    def dealer_action(self):
        """
        Draws cards for the dealer until they score at least 17.
        """
        dealer_score, ace = self.dealer_score()
        while dealer_score < 17 or (dealer_score == 17 and ace):
            self.dealer.append(self.deck.draw())
            dealer_score, ace = self.dealer_score()

    def game(self):
        """
        Allows user to play a game of blackjack (our model plays this in data_bot_sim.py).
        """
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

        if act == 3:
            i = 0
            while i < len(self.split_hands):
                self.player = self.split_hands[i]
                self.hit()
                print(f"Hand {i+1}: {self.player} ({self.player_score()[0]})")
                if self.player[0] == 1:
                    print("Stand on ace")
                    self.split_acts[i] = 1
                    i += 1
                    continue
                while True:
                    if i < self.split_limit:
                        action = input("Action (hit, stand, double, split): ")
                    else:
                        action = input("Action (hit, stand, double): ")
                    act = self.player_action(action)
                    if act != 0:
                        break
                    print(f"Hand {i+1}: {self.player} ({self.player_score()[0]})")
                    print(f"Dealer: {self.dealer}")
                self.split_acts[i] = act
                i += 1

            dealer_drawn = False
            for i in range(len(self.split_hands)):
                self.player = self.split_hands[i]
                print(f"Hand {i+1}: {self.player} ({self.player_score()[0]})")

                end = self.end_check(self.split_acts[i], dealer_drawn=dealer_drawn)
                dealer_drawn = True
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
            return

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

    def end_check(self, act, dealer_drawn=False):
        """
        Checks winner of the game.

        Returns:
            int: 0 if player wins, 1 if dealer wins, 2 if tie, 3 if player busts, 4 if dealer busts.
        """
        player_score, _ = self.player_score()
        if player_score > 21:
            print("Player busts! Dealer wins.")
            return 3
        if not dealer_drawn:
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
        """
        Initializes a deck of cards.

        Args:
            cards (np.ndarray, optional): List of cards (index 0 = A, index 1 = 2, ..., index 9 = 10 + face cards).
            decks (int, optional): Number of decks used.
            pen (float, optional): Penetration percentage before reshuffling.
            burn (bool, optional): Whether to burn a card after shuffling.
            seed (int, optional): Random seed for shuffling.
        """
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
        """
        Shuffles the deck and optionally burns a card.

        Args:
            burn (bool, optional): Whether to burn a card after shuffling.
        """
        np.random.shuffle(self.cards)
        self.pos = len(self.cards) - 1
        if burn:
            self.draw()

    def draw(self):
        """
        Draws a card from the deck.

        Returns:
            int: The drawn card.
        """
        if self.pos < 0:
            raise IndexError("No cards left in the deck.")
        card = self.cards[self.pos]
        self.pos -= 1
        return card

    def peek(self):
        """
        Returns the top card of the deck without drawing it.

        Returns:
            int: The top card.
        """
        if self.pos < 0:
            raise IndexError("No cards left in the deck.")
        return self.cards[self.pos]

    def __len__(self):
        """
        Returns the number of remaining cards in the deck.

        Returns:
            int: The number of remaining cards in the deck.
        """
        return self.pos + 1

    def check(self):
        """
        Checks if the deck has reached the reshuffle penetration point.

        Returns:
            bool: True if reshuffling is needed, False otherwise.
        """
        return len(self) < len(self.cards) * (1 - self.pen)
