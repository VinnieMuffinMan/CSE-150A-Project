from blackjack import Blackjack
from data_bot import action
from state import State


def simulate(seed=None):
    game = Blackjack(seed=seed)
    state = State(burn=False)
    num_games = 6
    for i in range(num_games):
        print("_" * 50)
        print(f"Game {i+1}")
        print("Bal:", game.bal)
        game.deal()
        print(game.player)
        print(game.dealer)
        state.update_hand(game.player, game.dealer[:1])

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
                break
            if act == "split":
                print("GUH") # TODO: implement split
                break
            if act == "surrender":
                break
            print(f"Player: {game.player} ({game.player_score()[0]})")
            print(f"Dealer: {game.dealer[0]}")

        if act == "surrender":
            game.surrender()
            print(f"Dealer: {game.dealer} ({game.dealer_score()[0]})")
            state.update_dealer_hand(game.dealer[1:])
            continue

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
        
    print(f"Won {game.bal} over {num_games} games.")

if __name__ == "__main__":
    simulate(seed=17)
