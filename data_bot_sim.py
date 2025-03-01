from blackjack import Blackjack
from data_bot import action
from state import State
import matplotlib.pyplot as plt


def simulate(seed=None,num_games=100):
    """
    Simulates a number of Blackjack games using the model in data_bot.py to play.

    Args:
        seed (int, optional): Seed for deterministic games.
        num_games (int, optional): Number of blackjack games to simulate (default: 100).

    Saves:
        A plot of the player's balance over the number of games played.
    """
    # Initialize the game and its state
    game = Blackjack(seed=seed)
    state = State(burn=False)
    games, bals = range(num_games + 1), []

    for i in range(num_games):
        print("_" * 50)
        print(f"Game {i+1}")
        print("Bal:", game.bal)
        bals.append(game.bal)

        # Check if deck needs to be reshuffled
        if game.check_deck_pen():
            print("Shuffling...")
            state.not_seen_reset()

        game.deal()
        print(game.player)
        print(game.dealer)
        state.update_hand(game.player, game.dealer[:1])

        # Check for immediate blackjacks
        start = game.start_check()
        if start != 0:
            state.update_dealer_hand(game.dealer[1:])
        if start == 1:
            print(f"Dealer: {game.dealer}")
            print("Player blackjack.")
            continue
        if start == 2:
            print(f"Dealer: {game.dealer}")
            print("Dealer blackjack.")
            continue
        if start == 3:
            print(f"Dealer: {game.dealer} ({game.dealer_score()[0]})")
            print("It's a tie.")
            continue

        # Determine best action for the given hand
        while True:
            act, ev = action(state)
            print(ev)
            print(act)
            if act == "hit":
                hit = game.hit()
                state.update_player_hand(hit)
            if act == "stand":
                break
            if act == "double":
                double = game.double()
                state.update_player_hand(double)
                print(f"Player: {game.player} ({game.player_score()[0]})")
                print(f"Dealer: {game.dealer[0]}")
                break
            if act == "split":
                game.split()
                break
            if act == "surrender":
                break
            print(f"Player: {game.player} ({game.player_score()[0]})")
            print(f"Dealer: {game.dealer[0]}")

        # Handle splitting (same loop as above but for both split hands)
        if act == "split":
            i = 0
            while i < len(game.split_hands):
                game.player = game.split_hands[i]
                new = game.hit()
                state.update_player_hand(new)
                state.player_hand = game.player.copy()
                print(f"Hand {i+1}: {game.player} ({game.player_score()[0]})")
                print(f"Dealer: {game.dealer[0]}")
                if game.player[0] == 1:
                    print("Stand on ace")
                    game.split_acts[i] = 1
                    i += 1
                    continue
                while True:
                    act, ev = action(state, can_split=i != game.split_limit)
                    print(ev)
                    print(act)
                    if act == "hit":
                        hit = game.hit()
                        state.update_player_hand(hit)
                    if act == "stand":
                        break
                    if act == "double":
                        double = game.double()
                        state.update_player_hand(double)
                        print(f"Hand {i+1}: {game.player} ({game.player_score()[0]})")
                        print(f"Dealer: {game.dealer[0]}")
                        break
                    if act == "split":
                        game.split()
                        break
                    if act == "surrender":
                        break
                    print(f"Hand {i+1}: {game.player} ({game.player_score()[0]})")
                    print(f"Dealer: {game.dealer[0]}")
                i += 1

            # Evaluate outcome for both split hands
            dealer_drawn = False
            for i in range(len(game.split_hands)):
                game.player = game.split_hands[i]
                print(f"Hand {i+1}: {game.player} ({game.player_score()[0]})")

                end = game.end_check(game.split_acts[i], dealer_drawn=dealer_drawn)
                dealer_drawn = True
                print(f"Dealer: {game.dealer} ({game.dealer_score()[0]})")

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
            state.update_dealer_hand(game.dealer[1:])
            continue

        if act == "surrender":
            game.surrender()
            print(f"Dealer: {game.dealer} ({game.dealer_score()[0]})")
            state.update_dealer_hand(game.dealer[1:])
            continue

        # Determines winner of the game
        act = 2 if act == "double" else 1
        end = game.end_check(act)
        print(f"Dealer: {game.dealer} ({game.dealer_score()[0]})")

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
        state.update_dealer_hand(game.dealer[1:])

    # Saves the player's balance over the number of games played to a plot
    print(f"Won {game.bal} over {num_games} games.")
    bals.append(game.bal)
    plt.plot(games, bals)
    plt.xlabel("Games")
    plt.ylabel("Balance")
    plt.title(f"Blackjack Balance (Seed {seed}, Games {num_games})")
    plt.savefig(f"balance_seed_{seed}_games_{num_games}.png")


if __name__ == "__main__":
    simulate(seed=0, num_games=500)
