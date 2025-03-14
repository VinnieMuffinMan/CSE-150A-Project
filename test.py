import unittest
from wordle_utils import get_feedback


class TestGetFeedback(unittest.TestCase):
    def test(self):
        self.assertEqual(get_feedback("apple", "apple"), [2, 2, 2, 2, 2])
        self.assertEqual(get_feedback("abcde", "vwxyz"), [0, 0, 0, 0, 0])
        self.assertEqual(get_feedback("apple", "apron"), [2, 2, 0, 0, 0])
        self.assertEqual(get_feedback("paper", "apple"), [1, 1, 2, 1, 0])
        self.assertEqual(get_feedback("allee", "lemon"), [0, 1, 0, 1, 0])
        self.assertEqual(get_feedback("crane", "candy"), [2, 0, 1, 1, 0])


if __name__ == "__main__":
    unittest.main()
