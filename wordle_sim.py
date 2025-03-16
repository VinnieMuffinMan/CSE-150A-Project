from tqdm import tqdm
from wordle import Wordle
import random
from wordle_bot import WordleBot
import matplotlib.pyplot as plt

def simulate(const_word=None, hard=False, debug=False, first=None):
    """
    Simulates a game of Wordle using the model in wordle_bot.py to play.

    Args:
        const_word (string, optional): Chosen word for the agent to find.
        hard (bool, optional): Includes all existing five-letter words as possible answers if True.
        debug (bool, optional): Prints game-related information if True.
    Returns:
        int: Number of attempts the agent used to find the answer, returns 0 if the agent lost.
    """
    # Initialize the game and the agent
    wordle = Wordle(const_word=const_word, hard=hard)
    bot = WordleBot(wordle.words, wordle.sol_words)

    wordle.start_game()

    # Main game loop, one iteration for every guess
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
    num_games = len(words)
    game_stats = [simulate(const_word=w, first="tarse") for w in tqdm(words)]
    avg = sum(game_stats) / len(game_stats)
    won = 0
    loss = 0
    attempts = []
    for i in game_stats:
        if i == 0:
            loss += 1
            attempts.append(6)
        else:
            won += 1
            attempts.append(i)

    plt.hist(attempts, bins=[0.5, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5], edgecolor='black', align='mid')
    plt.xticks(range(1, 7))
    plt.xlabel('Attempts')
    plt.ylabel('Number of Games')
    plt.title(f'Distribution of Attempts Per Game ({num_games} Games)')
    plt.savefig(f"num_attempts_{num_games}_games.png")

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
