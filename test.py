import unittest
from blackjack import Blackjack
from bot import *
from state import State


class TestBlackjackEV(unittest.TestCase):
    def test_expected_values(self):
        test_cases = {
            1: (-0.5113538599846008, -0.19648142835425353),
            3: (0.19538824630840795, -0.612792945312413),
            4: (-0.119351548497642, 0.35304316118886636),
            5: (-0.47619322088841776, -0.40702352260419256),
            6: (0.39819612589651554, -0.5882976232377854),
        }

        for seed, (expected_stand_ev, expected_hit_ev) in test_cases.items():
            with self.subTest(seed=seed):
                game = Blackjack(seed=seed)
                game.deal()

                player_hand = game.player
                dealer_hand = game.dealer[:1]

                state = State(burn=False)
                state.update_hand(player_hand, dealer_hand)

                stand_ev = expected_value_stand(state)
                hit_ev = expected_value_hit(state, depth=6)

                print(f"Seed: {seed}")
                print("Player Hand:", player_hand)
                print("Dealer Hand:", dealer_hand)
                print("Stand EV:", stand_ev)
                print("Hit EV:", hit_ev)
                print("__________________________________________")

                self.assertAlmostEqual(stand_ev, expected_stand_ev, places=6)
                self.assertAlmostEqual(hit_ev, expected_hit_ev, places=6)


if __name__ == "__main__":
    unittest.main()
