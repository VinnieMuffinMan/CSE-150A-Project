import numpy as np
from collections import Counter
from tqdm import tqdm
import time


def get_feedback_safe(guess, answer, words):
    """
    Determines whether the given guess is valid and gets the feedback for the guess.

    Args:
        guess (string): Five-letter word that the player guesses.
        answer (string): Five-letter word that the guess will be compared against.
        words (list[int]): List of all possible five-letter words.
    Returns:
        list[int]: A list of five integers (0 = letter not in word, 1 = letter in word but different place, 
                   2 = letter is correct), or None if the guess is not valid.
    """
    if len(guess) != 5 or guess not in words:
        return

    return get_feedback(guess, answer)


def get_feedback(guess, answer):
    """
    Gets the feedback for a guess on a given answer.

    Args:
        guess (string): Five-letter word that the player guesses.
        answer (string): Five-letter word that the guess will be compared against.
    Returns:
        list[int]: A list of five integers (0 = letter not in word, 1 = letter in word but different place, 2 = letter is correct).
    """
    # For returning the correct number of yellow/green squares for each letter
    answer_counts = Counter(answer)

    feedback = [0, 0, 0, 0, 0]
    # Loop through correct letters first
    for i, (g, a) in enumerate(zip(guess, answer)):
        if g == a:
            feedback[i] = 2
            answer_counts[g] -= 1

    # Then loop through incorrectly placed letters
    for i, g in enumerate(guess):
        if answer_counts.get(g, 0) > 0 and feedback[i] == 0:
            feedback[i] = 1
            answer_counts[g] -= 1

    return feedback

def get_feedback_from_lookup(guess, answer, feedback_matrix, word_index):
    """
    Gets the feedback for a guess on a given answer via the feedback_matrix.npy dataset.

    Args:
        guess (string): Five-letter word that the player guesses.
        answer (string): Five-letter word that the guess will be compared against.
        feedback_matrix (np.ndarray): Array where each entry corresponds to the feedback of a specific guess and answer.
        word_index (dict): Dictionary where each word corresponds to an index (they are indexed in alphabetical order).
    Returns:
        list[int]: A list of five integers (0 = letter not in word, 1 = letter in word but different place, 2 = letter is correct).
    """
    guess_idx = word_index[guess]
    answer_idx = word_index[answer]
    return feedback_matrix[guess_idx, answer_idx]

def get_feedback_from_index(guess_idx, answer_idx, feedback_matrix):
    """
    Gets the feedback for a guess (given by index) on an answer (given by index) via the feedback_matrix.npy dataset.

    Args:
        guess_idx (int): Index of the guess word.
        answer (int): Index of the answer word that the guess will be compared against.
        feedback_matrix (np.ndarray): Array where each entry corresponds to the feedback of a specific guess and answer.
    Returns:
        list[int]: A list of five integers (0 = letter not in word, 1 = letter in word but different place, 2 = letter is correct).
    """
    return feedback_matrix[guess_idx, answer_idx]

def precompute_feedback(word_file="wordle_word_list.txt"):
    """
    Finds the feedbacks of all possible guess-answer combinations and saves them to feedback_matrix.npy.

    Args:
        word_file (string, optional): Name of the file of words that will be used to generate all guess-answer combinations.
    """
    with open(word_file, "r") as f:
        words = [line.strip() for line in f]

    word_list = sorted(words)  # Ensure consistent indexing

    feedback_matrix = np.zeros((len(word_list), len(word_list), 5), dtype=np.uint8)
    for i, guess in enumerate(tqdm(word_list)):
        for j, answer in enumerate(word_list):
            feedback_matrix[i, j] = get_feedback(guess, answer)

    np.save("feedback_matrix.npy", feedback_matrix)

if __name__ == "__main__":
    with open("wordle_word_list.txt", "r") as f:
        words = [line.strip() for line in f]
    guess = "apple"
    answer = "apron"


    # feedback_matrix = np.load("feedback_matrix.npy")
    start_time = time.time()
    precompute_feedback()

    # for gi in tqdm(range(len(words))):
    #     for ai in range(len(words)):
    #         feedback = get_feedback_from_index(gi, ai, feedback_matrix)
    #         tuple(feedback)
    end_time = time.time()
    print(f"Time taken: {end_time - start_time}")

