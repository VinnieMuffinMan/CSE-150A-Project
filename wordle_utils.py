import numpy as np
from collections import Counter
from tqdm import tqdm
import time


def get_feedback_safe(guess, answer, words):
    if len(guess) != 5 or guess not in words:
        return

    return get_feedback(guess, answer)


def get_feedback(guess, answer):
    # For returning the correct number of yellow/green squares for each letter
    answer_counts = Counter(answer)

    feedback = [0, 0, 0, 0, 0]
    for i, (g, a) in enumerate(zip(guess, answer)):
        if g == a:
            feedback[i] = 2
            answer_counts[g] -= 1

    for i, g in enumerate(guess):
        if answer_counts.get(g, 0) > 0 and feedback[i] == 0:
            feedback[i] = 1
            answer_counts[g] -= 1

    return feedback

def get_feedback_from_lookup(guess, answer, feedback_matrix, word_index):
    guess_idx = word_index[guess]
    answer_idx = word_index[answer]
    return feedback_matrix[guess_idx, answer_idx]

def get_feedback_from_index(guess_idx, answer_idx, feedback_matrix):
    return feedback_matrix[guess_idx, answer_idx]

def precompute_feedback(word_file="wordle_word_list.txt"):
    with open(word_file, "r") as f:
        words = [line.strip() for line in f]

    word_list = sorted(words)  # Ensure consistent indexing
    word_index = {word: i for i, word in enumerate(word_list)}

    feedback_matrix = np.zeros((len(word_list), len(word_list), 5), dtype=np.uint8)
    for i, guess in enumerate(tqdm(word_list)):
        for j, answer in enumerate(word_list):
            feedback_matrix[i, j] = get_feedback(guess, answer)

    guess_idx = word_index["crane"]
    answer_idx = word_index["stone"]
    feedback = feedback_matrix[guess_idx, answer_idx]
    print(feedback)
    np.save("feedback_matrix.npy", feedback_matrix)

if __name__ == "__main__":
    with open("wordle_word_list.txt", "r") as f:
        words = [line.strip() for line in f]
    guess = "apple"
    answer = "apron"


    feedback_matrix = np.load("feedback_matrix.npy")
    start_time = time.time()
    precompute_feedback()

    # for gi in tqdm(range(len(words))):
    #     for ai in range(len(words)):
    #         feedback = get_feedback_from_index(gi, ai, feedback_matrix)
    #         tuple(feedback)
    end_time = time.time()
    print(f"Time taken: {end_time - start_time}")

