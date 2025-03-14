import unittest
import numpy as np
from wordle_utils import get_feedback, get_feedback_from_lookup


class TestGetFeedback(unittest.TestCase):
    def test(self):
        self.assertEqual(get_feedback("apple", "apple"), [2, 2, 2, 2, 2])
        self.assertEqual(get_feedback("abcde", "vwxyz"), [0, 0, 0, 0, 0])
        self.assertEqual(get_feedback("apple", "apron"), [2, 2, 0, 0, 0])
        self.assertEqual(get_feedback("paper", "apple"), [1, 1, 2, 1, 0])
        self.assertEqual(get_feedback("allee", "lemon"), [0, 1, 0, 1, 0])
        self.assertEqual(get_feedback("crane", "candy"), [2, 0, 1, 1, 0])

    def test_from_lookup(self):
        with open("wordle_word_list.txt", "r") as f:
            words = [line.strip() for line in f]
        feedback_matrix = np.load("feedback_matrix.npy")
        word_index = {word: i for i, word in enumerate(sorted(words))}
        self.assertTrue((get_feedback_from_lookup("apple", "apple", feedback_matrix, word_index) == np.array([2, 2, 2, 2, 2])).all())
        self.assertTrue((get_feedback_from_lookup("apple", "apron", feedback_matrix, word_index) == np.array([2, 2, 0, 0, 0])).all())
        self.assertTrue((get_feedback_from_lookup("paper", "apple", feedback_matrix, word_index) == np.array([1, 1, 2, 1, 0])).all())
        self.assertTrue((get_feedback_from_lookup("allee", "lemon", feedback_matrix, word_index) == np.array([0, 1, 0, 1, 0])).all())
        self.assertTrue((get_feedback_from_lookup("crane", "candy", feedback_matrix, word_index) == np.array([2, 0, 1, 1, 0])).all())


if __name__ == "__main__":
    unittest.main()
