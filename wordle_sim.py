from wordle import Wordle
from wordle_bot import WordleBot


def simulate(const_word=None, num_games=100,hard=False):
    wordle = Wordle(const_word=const_word,hard=hard)
    bot = WordleBot(wordle.words, wordle.sol_words)

    for i in range(num_games):
        wordle.start_game()
        bot.reset(wordle.words, wordle.sol_words)

        guess_history = []
        while wordle.attempts > 0:
            print(f"Attempts left: {wordle.attempts}")
            guess = bot.action(guess_history)
            print(f"Guess: {guess}")
            feedback = wordle.get_feedback(guess)
            guess_history.append((guess, feedback))

            wordle.attempts -= 1
            print(f"Feedback: {feedback}")
            if not feedback:
                raise ValueError
            if sum(feedback) == 0:
                print(f"Successfully guessed: {wordle.answer}")
                return

        print(f"Out of attempts, correct word: {wordle.answer}")


if __name__ == "__main__":
    simulate(const_word=None, num_games=1, hard=True)
