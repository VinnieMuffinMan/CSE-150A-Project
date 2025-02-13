import unittest
from blackjack import Blackjack
from bot import *
from state import State


class TestBlackjackEV(unittest.TestCase):
    def test_expected_values(self):
        test_cases = {
            0: (-0.5368065088280378, -0.4080431269704462),
            1: (-0.5402939136195947, -0.34279455713803053),
            3: (-0.5398232925468964, -0.3431091660924308),
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

                self.assertAlmostEqual(stand_ev, expected_stand_ev, places=6)
                self.assertAlmostEqual(hit_ev, expected_hit_ev, places=6)


if __name__ == "__main__":
    unittest.main()
