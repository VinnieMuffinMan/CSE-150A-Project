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
            new_feedback = get_feedback(guess, word, self.guessable)
            if new_feedback != feedback:
                return False         
        return True

    def action(self, guess_history):
        self.guessable = [word for word in self.guessable if self.fits_info(word, guess_history)]
        self.remaining = [word for word in self.remaining if self.fits_info(word, guess_history)]
        self.guessable.sort(reverse=False)
        self.remaining.sort(reverse=False)
        print(self.guessable)
        print(self.remaining)
        guess = input("Enter your guess: ").lower()
        return guess