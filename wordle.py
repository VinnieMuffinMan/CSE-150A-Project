import numpy as np
import random
from wordle_utils import get_feedback_safe


class Wordle:
    def __init__(self, const_word=None, hard=False):
        with open("wordle_word_list.txt", "r") as f:
            self.words = [line.strip() for line in f]

        with open("wordle_sol_list.txt", "r") as f:
            self.sol_words = [line.strip() for line in f]
        if hard:
            self.sol_words = self.words.copy()
        self.answer = ""
        self.attempts = 6
        self.const_word = const_word

    def get_feedback(self, guess):
        return get_feedback_safe(guess, self.answer, self.words)

    def start_game(self, word=None):
        # print("New game, choosing word...")
        self.answer = (
            self.const_word if self.const_word else random.choice(list(self.sol_words))
        )
        self.attempts = 6

    def play(self, word=None):
        self.start_game(word=word)

        while self.attempts > 0:
            print(f"Attempts left: {self.attempts}")
            guess = input("Enter your guess: ").lower()
            feedback = self.get_feedback(guess)
            if not feedback:
                print("Invalid: must be a 5-letter word in the word list")
                continue

            self.attempts -= 1
            print(f"Feedback: {feedback}")
            if sum(feedback) == 10:
                print(f"Successfully guessed: {self.answer}")
                return

        print(f"Out of attempts, correct word: {self.answer}")


if __name__ == "__main__":
    game = Wordle()
    game.play(word="trees")
