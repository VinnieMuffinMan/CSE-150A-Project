from blackjack import Blackjack
from bot import *
from data_bot import action
from state import State


if __name__ == "__main__":
    # seeds = [1, 3, 4, 5, 6]
    seeds = [12]
    for i in seeds:
        game = Blackjack(seed=i)
        game.deal()
        print(game.player)
        print(game.dealer)
        state = State(burn=False)
        state.update_hand(game.player, game.dealer[:1])
        stand_ev = expected_value_stand(state)
        hit_ev = expected_value_hit(state, depth=3)
        double_ev = expected_value_double(state)
        print(f"{i}: ({stand_ev}, {hit_ev}, {double_ev}),")
        rec, evs = action(state)
        print(rec)
        print(evs)
        print("Stand difference:", stand_ev-evs[0])
        print("Hit difference:", hit_ev-evs[1])
        print("Double difference:", double_ev-evs[2])
    # while True:
    #     game.game()
    #     print()
