import numpy as np

def get_feedback_safe(guess, answer, words):
    if len(guess) != 5 or guess not in words:
        return

    return get_feedback(guess, answer)


def get_feedback(guess, answer):
    # For returning the correct number of yellow/green squares for each letter
    answer_counts = {letter: answer.count(letter) for letter in set(answer)}

    feedback = [0] * 5
    for i in range(len(guess)):
        if guess[i] == answer[i]:
            feedback[i] = 2
            answer_counts[guess[i]] -= 1

    for i in range(len(guess)):
        if feedback[i] == 2:
            continue
        if guess[i] in answer_counts and answer_counts[guess[i]] > 0:
            feedback[i] = 1
            answer_counts[guess[i]] -= 1

    return feedback
