import numpy as np
from bj_utils import score
from blackjack import Deck
from state import State
from tqdm import tqdm
import multiprocessing
from concurrent.futures import ProcessPoolExecutor
import time


def create_and_shuffle_decks(cards, count):
    decks = [Deck(cards=cards.copy()) for _ in range(count)]
    for deck in decks:
        deck.shuffle()
    return decks


def __generate_decks(not_seen, count=1000000, num_workers=None):
    start_time = time.time()

    if num_workers is None:
        num_workers = multiprocessing.cpu_count()

    cards = np.repeat(np.arange(1, len(not_seen) + 1), not_seen)

    chunk_size = max(1, count // num_workers)
    chunk_sizes = [chunk_size] * (count // chunk_size) + (
        [count % chunk_size] if count % chunk_size else []
    )

    with ProcessPoolExecutor(max_workers=num_workers) as executor:
        shuffled_chunks = list(
            executor.map(
                create_and_shuffle_decks, [cards] * len(chunk_sizes), chunk_sizes
            )
        )

    decks = [deck for chunk in shuffled_chunks for deck in chunk]

    end_time = time.time()
    print(
        f"Execution time: {end_time - start_time:.2f} seconds using {num_workers} cores"
    )

    return decks


def action(state: State):
    player_hand = state.player_hand
    can_split = player_hand[0] == player_hand[1]
    dealer_hand = state.dealer_hand
    decks = __generate_decks(state.not_seen)
    num_decks = len(decks)
    total_value = [0, 0, 0, 0]
    deck_its = 3
    for d in tqdm(decks):
        for _ in range(deck_its):
            value = analyze(player_hand, dealer_hand.copy(), d, can_split=can_split)
            for i, v in enumerate(value):
                total_value[i] += v
        d.draw()

    expected_value = [v / num_decks / deck_its for v in total_value] + [-0.5]

    best_action_idx = max(range(5), key=lambda i: expected_value[i])
    actions = ["stand", "hit", "double", "split", "surrender"]

    rec = actions[best_action_idx]

    return rec, expected_value


def analyze(player_hand, dealer_hand, deck: Deck, can_split=False):
    if dealer_hand[0] == 1:
        while deck.peek() >= 10:
            deck.shuffle()
    if dealer_hand[0] >= 10:
        while deck.peek() == 1:
            deck.shuffle()
    dealer_hand += [deck.draw()]

    deck_pos = deck.pos
    value_stand = stand(player_hand, dealer_hand, deck)

    deck.pos = deck_pos
    value_hit = hit(player_hand, dealer_hand, deck)

    deck.pos = deck_pos
    value_double = double(player_hand, dealer_hand, deck)

    deck.pos = deck_pos
    if can_split:
        value_split = split(player_hand, dealer_hand, deck, [3])
    else:
        value_split = -1000

    return (value_stand, value_hit, value_double, value_split)


def stand(player_hand, dealer_hand, deck: Deck):
    dealer_hand = dealer_hand.copy()
    player_score, _ = score(player_hand)

    dealer_score, ace = score(dealer_hand)
    while dealer_score < 17 or (dealer_score == 17 and ace):
        dealer_hand += [deck.draw()]
        dealer_score, ace = score(dealer_hand)

    if dealer_score > 21:
        return 1
    if dealer_score > player_score:
        return -1
    if dealer_score < player_score:
        return 1
    return 0


def hit(player_hand, dealer_hand, deck: Deck, preserve=True):
    if preserve:
        player_hand = player_hand.copy()
    player_hand += [deck.draw()]
    if score(player_hand)[0] > 21:
        return -1

    if hit_heuristic(player_hand, dealer_hand, deck):
        return hit(player_hand, dealer_hand, deck)

    return stand(player_hand, dealer_hand, deck)


# Basic heuristic for repeated hit calculations
def hit_heuristic(player_hand, dealer_hand, deck: Deck):
    player_score, ace = score(player_hand)
    dealer_card = dealer_hand[0]

    if player_score <= 11:
        return True
    if player_score <= 16 and dealer_card >= 7:
        return True
    if player_score <= 17 and ace:
        return True
    return False


def double(player_hand, dealer_hand, deck: Deck):
    player_hand = player_hand.copy()
    player_hand += [deck.draw()]
    if score(player_hand)[0] > 21:
        return -2
    return 2 * stand(player_hand, dealer_hand, deck)


def split(player_hand, dealer_hand, deck: Deck, split_left=None):
    if split_left is None:
        split_left = [3]
    player_hand_1 = [player_hand[0]]
    player_hand_2 = [player_hand[1]]
    player_hand_1 += [deck.draw()]
    player_hand_2 += [deck.draw()]
    split_left[0] -= 1

    ev = 0
    # No drawing or splitting on split aces
    if player_hand_1[0] == 1:
        ev += stand(player_hand_1, dealer_hand, deck)
        ev += stand(player_hand_2, dealer_hand, deck)
        return ev

    if player_hand_1[0] == player_hand_1[1] and split_left[0] > 0:
        ev += split(player_hand_1, dealer_hand, deck, split_left)
    elif hit_heuristic(player_hand_1, dealer_hand, deck):
        ev += hit(player_hand_1, dealer_hand, deck, preserve=False)
    else:
        ev += stand(player_hand_1, dealer_hand, deck)

    if player_hand_2[0] == player_hand_2[1] and split_left[0] > 0:
        ev += split(player_hand_1, dealer_hand, deck, split_left)
    elif hit_heuristic(player_hand_2, dealer_hand, deck):
        ev += hit(player_hand_2, dealer_hand, deck, preserve=False)
    else:
        ev += stand(player_hand_2, dealer_hand, deck)

    return ev
