import numpy as np
from tqdm import tqdm
from wordle_utils import get_feedback_from_index


class WordleBot:
    def __init__(self, guessable, remaining):
        """
        Initializes the Wordle agent.

        Args:
            guessable (list[string]): List of all valid 5-letter words to guess in Wordle.
            remaining (list[string]): List of all possible answer words in Wordle.
        """
        self.guessable = guessable.copy()
        self.guessable = sorted(self.guessable)
        self.guessable_index = np.arange(len(self.guessable))
        self.lookup = np.load("feedback_matrix.npy")
        self.word_index = {word: i for i, word in enumerate(self.guessable)}
        self.index_word = np.array(self.guessable)

        self.remaining = remaining.copy()
        self.remaining = sorted(self.remaining)
        self.remaining_index = np.array([self.word_index[word] for word in self.remaining])
        with open('wordle_sol_list.txt', 'r') as f:
            sol_words = [line.strip() for line in f]
        self.frequencies = np.array([4 if word in sol_words else 1 for word in self.guessable])

    def reset(self, guessable, remaining):
        """
        Resets the agent's lists of guessable and remaining words.

        Args:
            guessable (list[string]): List of all valid 5-letter words to guess in Wordle.
            remaining (list[string]): List of all possible answer words in Wordle.
        """
        self.guessable = guessable
        self.remaining = remaining

    def fits_info(self, i, guess_history):
        """
        Determines whether the answer word (given by index) fits all previous feedback.

        Args:
            i (int): Index of the answer word that is checked for fitting the feedback.
            guess_history (list[tuple]): List of tuples that contains the agent's previous guesses and their corresponding feedbacks.
        Returns:
            bool: True if the answer word fits the guess history, False otherwise.
        """
        for guess, feedback in guess_history:
            new_feedback = get_feedback_from_index(
                self.word_index[guess], i, self.lookup
            )
            if np.any(new_feedback != feedback):
                return False
        return True

    def get_information(self, wi, answers, possible):
        """
        Calculates the amount of information given by the word (given by index).

        Args:
            wi (int): Index of the guess word whose parameter is being calculated.
            answers (np.ndarray): Array of indices of possible answer words we are comparing the guess against.
            possible (np.ndarray): Array of all possible feedbacks (all length-5 list combinations of 0s, 1s, and 2s).
        Returns:
            float: Entropy of the feedback of the given guess word.
        """
        for ai in answers:
            feedback = get_feedback_from_index(wi, ai, self.lookup)
            possible[
                feedback[0], feedback[1], feedback[2], feedback[3], feedback[4]
            ] += self.frequencies[wi]

        possible /= sum(self.frequencies[ai] for ai in answers)
        exp = 0

        for value in possible.flatten():
            if value > 0:
                exp -= value * np.log2(value)

        return exp

    def evaluate_words(self, remaining_index, words_index, debug=False):
        """
        Returns the index of the word that gives us the most information to find the answer.

        Args:
            remaining_index (np.ndarray): Array of indices of possible answer words.
            words_index (np.ndarray): Array of indices of all 5-letter words.
            debug (bool, optional): Prints calculated parameters if True.
        Returns:
            int: Index of the word with the highest entropy value.
        """
        possible_zeros = np.zeros((len(self.guessable), 3, 3, 3, 3, 3))
        if debug:
            eval_words = [
                self.get_information(wi, remaining_index, possible_zeros[wi])
                for wi in tqdm(words_index)
            ]
        else:
            eval_words = [
                self.get_information(wi, remaining_index, possible_zeros[wi])
                for wi in words_index
            ]
        max_i = np.argmax(eval_words)
        return words_index[max_i]

    def action(self, guess_history, debug=False, first=None):
        """
        Returns the word that gives us the most information to find the answer.

        Args:
            guess_history (list[tuple]): List of tuples that contains the agent's previous guesses and their corresponding feedbacks.
            debug (bool, optional): Prints words at certain indices if True.
            first (string, optional): Automatically chooses the first guess of the game if not None.
        Returns:
            string: Word that the agent chooses as its next guess.
        """
        self.remaining_index = np.array(
            [wi for wi in self.remaining_index if self.fits_info(wi, guess_history)]
        )
        if debug:
            print(self.index_word[self.guessable_index])
            print(len(self.remaining_index))
            print(self.index_word[self.remaining_index])
        if first and len(guess_history) == 0:
            guess = self.word_index[first]
        elif len(self.remaining_index) == 1:
            guess = self.remaining_index[0]
        else:
            guess = self.evaluate_words(self.remaining_index, self.guessable_index)
        self.guessable_index
        return self.index_word[guess]
