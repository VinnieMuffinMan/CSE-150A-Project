from wordle import Wordle
from wordle_bot import WordleBot

def simulate(seed=None,num_games=100):
    wordle = Wordle(seed=seed)
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
            if feedback == "🟩🟩🟩🟩🟩":
                print(f"Successfully guessed: {wordle.answer}")
                return

        print(f"Out of attempts, correct word: {wordle.answer}")

if __name__ == "__main__":
    simulate(seed=0, num_games=1)