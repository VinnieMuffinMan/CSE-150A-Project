import numpy as np


class Wordle:
    def __init__(self, seed=None):
        self.words = np.genfromtxt("wordle_word_list.txt", dtype="str")
        self.sol_words = np.genfromtxt("wordle_sol_list.txt", dtype="str")
        self.answer = ""
        self.attempts = 6
        if seed is not None:
            np.random.seed(seed)

    def get_feedback(self, guess):
        if len(guess) != 5 or guess not in self.words:
            return

        # For returning the correct number of yellow/green squares for each letter
        answer_counts = {
            letter: self.answer.count(letter) for letter in set(self.answer)
        }

        feedback = ["⬜"] * 5
        for i in range(len(guess)):
            if guess[i] == self.answer[i]:
                feedback[i] = "🟩"
                answer_counts[guess[i]] -= 1

        for i in range(len(guess)):
            if feedback[i] == "🟩":
                continue
            if guess[i] in answer_counts and answer_counts[guess[i]] > 0:
                feedback[i] = "🟨"
                answer_counts[guess[i]] -= 1

        feedback = "".join(feedback)
        return feedback

    def start_game(self, word=None):
        print("New game, choosing word...")
        if not word:
            self.answer = np.random.choice(self.sol_words)
        else:
            self.answer = word
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
            if feedback == "🟩🟩🟩🟩🟩":
                print(f"Successfully guessed: {self.answer}")
                return

        print(f"Out of attempts, correct word: {self.answer}")


if __name__ == "__main__":
    game = Wordle()
    game.play(word="trees")
