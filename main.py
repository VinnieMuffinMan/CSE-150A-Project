from blackjack import Blackjack
from bot import *
from state import State


if __name__ == "__main__":
    game = Blackjack(seed=6)
    game.deal()
    print(game.player)
    print(game.dealer)
    state = State(burn=False)
    state.update_hand(game.player, game.dealer[:1])
    stand_ev = expected_value_stand(state)
    print(stand_ev)
    hit_ev = expected_value_hit(state)
    print(hit_ev)
    # while True:
    #     game.game()
    #     print()
