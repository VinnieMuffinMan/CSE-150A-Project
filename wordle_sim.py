from wordle import Wordle
from wordle_bot import action

def simulate(seed=None,num_games=100):
    wordle = Wordle(seed=seed)
    for i in range(num_games):
        wordle.start_game()

        curr_feedback = ["⬜"] * 5
        guess_history = []
        while wordle.attempts > 0:
            print(f"Attempts left: {wordle.attempts}")
            guess = action(guess_history, curr_feedback)
            guess_history.append(guess)
            print(f"Guess: {guess}")
            feedback = wordle.get_feedback(guess)

            wordle.attempts -= 1
            print(f"Feedback: {feedback}")
            curr_feedback = feedback
            if feedback == "🟩🟩🟩🟩🟩":
                print(f"Successfully guessed: {wordle.answer}")
                return

        print(f"Out of attempts, correct word: {wordle.answer}")

if __name__ == "__main__":
    simulate(seed=0, num_games=1)