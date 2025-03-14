import math
import numpy as np
from tqdm import tqdm
from wordle_utils import get_feedback


class WordleBot:
    def __init__(self, guessable, remaining):
        self.guessable = guessable
        self.remaining = remaining

    def reset(self, guessable, remaining):
        self.guessable = guessable
        self.remaining = remaining

    def fits_info(self, word, guess_history):
        for guess, feedback in guess_history:
            new_feedback = get_feedback(guess, word)
            if new_feedback != feedback:
                return False
        return True

    def get_information(self, word, answers):
        possible = np.zeros(3**5)
        for a in answers:
            feedback = get_feedback(word, a)
            pos = 0
            while len(feedback) > 0:
                pos *= 3
                pos += feedback[0]
                feedback.pop(0)
            possible[pos] += 1

        possible /= len(answers)
        exp = np.where(possible > 0, possible * -1 * np.log2(possible), 0)
        return exp.sum()

    def evaluate_words(self, remaining, words):
        eval_words = [self.get_information(w, remaining) for w in tqdm(words)]
        max_i = np.argmax(eval_words)
        print(words[max_i])
        return words[max_i]

    def action(self, guess_history):
        self.guessable = [
            word for word in self.guessable if self.fits_info(word, guess_history)
        ]
        self.remaining = [
            word for word in self.remaining if self.fits_info(word, guess_history)
        ]
        self.guessable.sort(reverse=False)
        self.remaining.sort(reverse=False)
        print(self.guessable)
        print(self.remaining)
        guess = self.evaluate_words(self.remaining, self.guessable)
        return guess
