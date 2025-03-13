import random
from wordle_utils import get_feedback

class Wordle:
    def __init__(self, seed=None):
        self.words = set()
        with open("wordle_word_list.txt", "r") as f:
            for line in f:
                self.words.add(line.strip())
        self.sol_words = set()
        with open("wordle_sol_list.txt", "r") as f:
            for line in f:
                self.sol_words.add(line.strip())
        self.answer = ""
        self.attempts = 6
        if seed is not None:
            random.seed(seed)

    def get_feedback(self, guess):
        return get_feedback(guess, self.answer, self.words)

    def start_game(self):
        print("New game, choosing word...")
        self.answer = random.choice(list(self.sol_words))
        self.attempts = 6

    def play(self):
        self.start_game()

        while self.attempts > 0:
            print(f"Attempts left: {self.attempts}")
            guess = input("Enter your guess: ").lower()
            feedback = self.get_feedback(guess)
            if not feedback:
                print("Invalid: must be a 5-letter word in the word list")
                continue

            self.attempts -= 1
            print(f"Feedback: {feedback}")
            if feedback == "🟩🟩🟩🟩🟩":
                print(f"Successfully guessed: {self.answer}")
                return

        print(f"Out of attempts, correct word: {self.answer}")