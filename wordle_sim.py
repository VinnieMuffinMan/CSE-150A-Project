from tqdm import tqdm
from wordle import Wordle
import random
from wordle_bot import WordleBot
import matplotlib.pyplot as plt

def simulate(const_word=None, hard=False, debug=False):
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
    bot.reset(wordle.words, wordle.sol_words)

    # Main game loop, one iteration for every guess
    guess_history = []
    while wordle.attempts > 0:
        if debug:
            print(f"Attempts left: {wordle.attempts}")
        guess = bot.action(guess_history)
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
    # Sample a number of random words as answers to Wordle games
    with open("wordle_word_list.txt", "r") as f:
        words = [line.strip() for line in f]
    num_games = 5
    subset = random.sample(words, k=num_games)
    game_stats = [simulate(const_word=w, hard=True) for w in tqdm(subset)]

    # Calculate agent statistics
    avg = sum(game_stats) / len(game_stats)
    won = 0
    loss = 0
    games = range(num_games+1)
    attempts = []
    for i in game_stats:
        if i == 0:
            loss += 1
            attempts.append(6)
        else:
            won += 1
            attempts.append(i)

    plt.plot(games, [0] + attempts)
    plt.xlabel("Games")
    plt.ylabel("Attempts")
    plt.title(f"Number of Attempts Per Game ({num_games} Games)")
    plt.savefig(f"num_attempts_games_{num_games}.png")

    print(f"Won: {won}, Loss: {loss}")
    print(f"Win rate: {won / len(game_stats) * 100:.2f}%")
    print(f"Average attempts: {avg:.2f}")
