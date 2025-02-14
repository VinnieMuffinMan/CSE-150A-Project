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

def __generate_decks(not_seen, count=10000, num_workers=None):
    start_time = time.time()

    if num_workers is None:
        num_workers = multiprocessing.cpu_count()

    num = not_seen.sum()
    cards = [0] * num
    i = 0
    for c, n in enumerate(not_seen):
        for _ in range(n):
            cards[i] = c + 1
            i += 1

    chunk_size = max(1, count // num_workers)
    chunk_sizes = [chunk_size] * (count // chunk_size) + ([count % chunk_size] if count % chunk_size else [])

    with ProcessPoolExecutor(max_workers=num_workers) as executor:
        shuffled_chunks = list(executor.map(create_and_shuffle_decks, [cards] * len(chunk_sizes), chunk_sizes))

    decks = [deck for chunk in shuffled_chunks for deck in chunk]

    end_time = time.time()
    print(f"Execution time: {end_time - start_time:.2f} seconds using {num_workers} cores")

    return decks


def action(state: State):
    player_hand = state.player_hand
    dealer_hand = state.dealer_hand
    decks = __generate_decks(state.not_seen)
    num_decks = len(decks)
    total_value = [0, 0, 0, 0]
    for d in tqdm(decks):
        value = analyze(player_hand, dealer_hand.copy(), d)
        for i, v in enumerate(value):
            total_value[i] += v

    expected_value = [v / num_decks for v in total_value]
    return expected_value


def analyze(player_hand, dealer_hand, deck: Deck):
    if dealer_hand[0] == 1:
        while deck.peek() >= 10:
            deck.shuffle()
    if dealer_hand[0] >= 10:
        while deck.peek() == 1:
            deck.shuffle()
    dealer_hand += [deck.draw()]
    # if len(player_hand) == 2:
    #     if score(player_hand) == 21:
    #         if score(dealer_hand) == 21:
    #             return 0
    #         return 1.5

    #     if score(dealer_hand) == 21:
    #         return -1

    split = all((len(player_hand) == 2, player_hand[0] == player_hand[1]))

    deck_pos = deck.pos
    value_stand = stand(player_hand.copy(), dealer_hand.copy(), deck)

    deck.pos = deck_pos
    value_hit = hit(player_hand.copy(), dealer_hand.copy(), deck)

    deck.pos = deck_pos
    value_double = double(player_hand.copy(), dealer_hand.copy(), deck)

    deck.pos = deck_pos
    value_split = 0

    return (value_stand, value_hit, value_double, value_split)


def stand(player_hand, dealer_hand, deck: Deck):
    player_score, _ = score(player_hand)

    dealer_score, ace = score(dealer_hand)
    while dealer_score < 17 or (dealer_score == 17 and ace > 0):
        dealer_hand += [deck.draw()]
        dealer_score, ace = score(dealer_hand)

    if dealer_score > 21:
        return 1
    if dealer_score > player_score:
        return -1
    if dealer_score < player_score:
        return 1
    return 0


def hit(player_hand, dealer_hand, deck: Deck):
    player_hand += [deck.draw()]
    player_score, _ = score(player_hand)
    value = -1
    while player_score <= 21:
        stand_val = stand(player_hand, dealer_hand.copy(), deck)
        if stand_val == 1:
            return 1

        value = max(value, stand_val)
        player_hand += [deck.draw()]
        player_score, _ = score(player_hand)

    return value


def double(player_hand, dealer_hand, deck: Deck):
    player_hand += [deck.draw()]
    if score(player_hand)[0] > 21:
        return -2
    return 2 * stand(player_hand, dealer_hand, deck)
