from tqdm import tqdm
from wordle import Wordle
import random
from wordle_bot import WordleBot


def simulate(const_word=None, num_games=100, hard=False, debug=False, first=None):
    wordle = Wordle(const_word=const_word, hard=hard)
    bot = WordleBot(wordle.words, wordle.sol_words)

    for i in range(num_games):
        wordle.start_game()
        bot.reset(wordle.words, wordle.sol_words)

        guess_history = []
        while wordle.attempts > 0:
            if debug:
                print(f"Attempts left: {wordle.attempts}")
            guess = bot.action(guess_history, debug=debug, first=first)
            if debug:
                print(f"Guess: {guess}")
            feedback = wordle.get_feedback(guess)
            guess_history.append((guess, feedback))

            wordle.attempts -= 1
            if debug:
                print(f"Feedback: {feedback}")
            if not feedback:
                raise ValueError
            if sum(feedback) == 10:
                if debug:
                    print(
                        f"Successfully guessed: {wordle.answer} in {6 - wordle.attempts} attempts"
                    )
                return 6 - wordle.attempts
        if debug:
            print(f"Out of attempts, correct word: {wordle.answer}")
        return 0


if __name__ == "__main__":
    # simulate(const_word="skull", num_games=1, debug=True, first="tarse")

    with open("wordle_sol_list.txt", "r") as f:
        words = [line.strip() for line in f]
    game_stats = [simulate(const_word=w, num_games=100, first="tarse") for w in tqdm(words)]
    avg = sum(game_stats) / len(game_stats)
    won = 0
    loss = 0
    for i in game_stats:
        if i == 0:
            loss += 1
        else:
            won += 1
    print(f"Won: {won}, Loss: {loss}")
    print(f"Win rate: {won / len(game_stats) * 100:.2f}%")
    print(f"Average attempts: {avg:.2f}")

    # game_stats = [simulate(const_word=w, num_games=1, first="tares") for w in tqdm(subset)]

    # avg = sum(game_stats) / len(game_stats)
    # won = 0
    # loss = 0
    # for i in game_stats:
    #     if i == 0:
    #         loss += 1
    #     else:
    #         won += 1
    # print(f"Won: {won}, Loss: {loss}")
    # print(f"Win rate: {won / len(game_stats) * 100:.2f}%")
    # print(f"Average attempts: {avg:.2f}")
