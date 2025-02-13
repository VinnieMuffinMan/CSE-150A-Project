import numpy as np
from bj_utils import score


def action(state):
    return "hit" if expected_value_hit(state) > expected_value_stand(state) else "stand"


def __dealer_sim(hand, not_seen):
    """
    Returns an array of probabilities of the dealer's score
    [17, 18, 19, 20, 21, bust]
    """

    dist = np.zeros(6)
    sc, ace = score(hand)
    left = not_seen.sum()

    if sc > 21:
        dist[5] = 1
        return dist

    if sc > 17:
        dist[sc - 17] = 1
        return dist

    if sc == 17 and ace == 0:
        dist[0] = 1
        return dist

    for r, c in enumerate(not_seen):
        if c == 0:
            continue
        not_seen[r] -= 1
        dist += __dealer_sim(hand + [r + 1], not_seen) * c / left
        not_seen[r] += 1

    return dist


def expected_value_stand(state):  # assume no blackjack
    player_score = state.player_score()

    not_seen = state.not_seen()

    card_dist = not_seen / not_seen.sum()
    if state.dealer_hand[0] == 10:
        card_dist[0] = 0
        card_dist = card_dist / card_dist.sum()
    if state.dealer_hand[0] == 1:
        card_dist[9] = 0
        card_dist = card_dist / card_dist.sum()

    ev = 0
    for c, p in enumerate(card_dist):
        if p == 0:
            continue
        not_seen[c] -= 1

        ev += p * __ev_stand(state.dealer_hand + [c + 1], not_seen, player_score)

        not_seen[c] += 1

    return ev


def __ev_hit_stand(player, dealer, not_seen, depth, hit=False, stand=False):
    player_score, _ = score(player)
    if depth == 0:
        stand = True
    if player_score > 21:
        return -1

    if hit:
        return __ev_hit(player, dealer, not_seen, depth)

    if stand:
        return __ev_stand(dealer, not_seen, player_score)

    return max(
        __ev_hit(player, dealer, not_seen, depth),
        __ev_stand(dealer, not_seen, player_score),
    )


def __ev_stand(dealer, not_seen, player_score):
    dealer_dist = __dealer_sim(dealer, not_seen)

    stand_ev = 0
    for dealer_score, prob in enumerate(dealer_dist):
        dealer_score += 17
        if dealer_score > 21:
            stand_ev += prob
        elif dealer_score > player_score:
            stand_ev -= prob
        elif dealer_score < player_score:
            stand_ev += prob
    return stand_ev


def __ev_hit(player, dealer, not_seen, depth):
    hit_ev = 0
    left = not_seen.sum()
    for r, c in enumerate(not_seen):
        if c == 0:
            continue
        not_seen[r] -= 1
        hit_ev += (
            __ev_hit_stand(player + [r + 1], dealer, not_seen, depth - 1) * c / left
        )
        not_seen[r] += 1
    return hit_ev


def expected_value_hit(state, depth = 5):
    not_seen = state.not_seen()

    card_dist = not_seen / not_seen.sum()
    if state.dealer_hand[0] >= 10:
        card_dist[0] = 0
        card_dist = card_dist / card_dist.sum()
    if state.dealer_hand[0] == 1:
        card_dist[9] = 0
        card_dist = card_dist / card_dist.sum()

    ev = 0
    for c, p in enumerate(card_dist):
        if p == 0:
            continue
        not_seen[c] -= 1
        ev += (
            __ev_hit_stand(
                state.player_hand, state.dealer_hand + [c + 1], not_seen, depth, hit=True
            )
            * p
        )
        not_seen[c] += 1

    return ev
