# Milestone 2 Writeup

### Describe your agent in terms of PEAS and give a background of your task at hand.
The task for this milestone was to create an agent that uses probabilistic concepts to determine the best five-letter words to guess in games of Wordle. The agent's performance measure is the amount of Wordle games that the agent wins. Its environment is a five-letter input space where the agent can input five-letter words and receive feedback for each letter. The agent's "actuators" choose the five-letter word that maximizes the amount of information we need to find the answer word. The agent's "sensors" sense the feedback that the game gives for its guesses, i.e. whether a letter is in the right place, in the word, or not in the word at all.

### Give an exploration of your dataset, and highlight which variables are important. Give a brief overview of each variable and its role in your agent/model. (Draw a picture!!)
Our dataset is generated in `precompute_feedback` in `wordle_utils.py`; this function loops through all possible 5-letter words (found in `wordle_word_list.txt`), using each one as a guess against every possible 5-letter word and obtaining the feedback for the guess using `get_feedback`. The function saves all of these observations to `feedback_matrix.npy`, which is used to calculate probabilities.

The primary variables are the word we are trying to guess (**W**), the guesses that the agent makes (**G_i**), and the feedback that the game gives for each guess (**F_i**). Our **W** variable serves as the goal of our model, our **G_i** variables are the model's actions, and the **F_i** variables are the information that the model uses to make better decisions. These variables and their relationships are shown in the diagram below:
![diagram]()

### Describe in detail how your variables interact with each other, and if your model fits a particular structure, explain why you chose that structure to model your agent. If it does not, further elaborate on why you chose that model based on the variables.
At the start of each game, our target five-letter word **W** is chosen at random (unless explicitly chosen using the `const_word` parameter in our `Wordle` game) and influences our **F_i** variables by determining how accurate each guess is. Each action our agent makes is a **G_i** variable, i.e. a five-letter word; for all i from 1 to 6 (since we have 6 total guesses), **G_i** influences **F_i** because the feedback reflects how accurate the guess is in comparison to the answer word. Once our agent guesses, the game computes the **F_i** variable, a list of five integers (0 = letter is not in the word, 1 = letter is in the word but in a different place, 2 = letter is in the word and in the correct place). For all i from 1 to 5 (we exclude 6 since that is our final guess, so the game is over), **F_i** influences **G_{i+1}** because the feedback narrows down the words that could possibly be the answer, meaning **G_{i+1}** will only be a word from this subset of possible words.

### END OF NEW README, WILL ADD MORE LATER

### Describe how your agent is set up and where it fits in probabilistic modeling
**Update:** The agent is set up according to the network below: 
![diagram](CSE150A-GP.png)
The state variable is the current game state (which consists of the dealer's hand, the player's hand, and the remaining cards in the deck). The action variable is what the player chooses to do (hit, stand, double, split, surrender). The win variable is a binary node where 1 indicates the player wins the game and 0 indicates the player loses. 
The state variable influences the action variable by determining which action is most likely to result in a win: 
- The dealer's hand tells the player what the dealer's score could most likely be, indicating whether the player should play against that hand.
- The player's hand tells the player what the player's score could most likely be, indicating whether the player should stand or take further action.
- The remaining cards in the deck tells the player what possible cards the dealer or player can draw, indicating what either hand could possibly be.<br/>

The state and action variables affect the win variable by determining how the game plays out. The state can indicate what either hand could possibly be, and the action could either increase or decrease the chances of winning.
This network is modeled in the `action` function, which takes the current game state as input and generates a large number of possible decks that match the not-seen cards in the state. From this set of possible decks, it creates a dataset of observations by performing possible actions on the deck (hit, stand, etc) and recording their outcomes. The agent chooses the action A that maximizes the chance of winning a game, i.e. the action with the most observations where the player won (the first probability listed in our diagram). Note that this probability is also conditioned on the current game state and thus we only generate observations that are based on this game state, as generating observations proved to be very inefficient. **(end of update)**

### Train your first model
**Update:** Our model's functionality is found in data_bot.py, particularly in the `action` function. It generates a large number of decks using `__generate_decks`, where each deck is a shuffled version of the unseen cards in the current game state. For each shuffled deck, the model calculates the expected value for all possible action in the `analyze` function. The `analyze` function does this by running the respective function for each action other than surrender (`hit` for hitting, `stand` for standing, etc), where each function returns the expected value of performing that action on the given deck. Running `analyze` on all these shuffled decks creates our observations. The expected values are summed across these observations and divided by `num_decks` to find the final expected values for each action. The model incorporates the diagram above by choosing the action with the most observations resulting in a win, i.e. the action with the highest expected value. **(end of update)**

### Evaluate your model
**Update:** Our model can be evaluated by running data_bot_sim.py, particularly the `simulate` function. For each game, the model chooses the best action (based on the logic described above) repeatedly until either the player or dealer wins. The result of the game determines what is added to or subtracted from the player's balance. This continues for a user-specified number of games, and a plot showing the player's balance over time is created when all games have been played. **(end of update)**

### Create/Update your README.md to include your new work and updates you have all added. Make sure to upload all code and notebooks. Provide links in your README.md
The following are the main scripts that we implemented throughout the process of building our agent (in chronological order):
- [blackjack.py](https://github.com/VinnieMuffinMan/CSE-150A-Project/blob/Milestone2/blackjack.py): This contains the Blackjack class that our agent interacts with to play the game.
- [bj_utils.py](https://github.com/VinnieMuffinMan/CSE-150A-Project/blob/Milestone2/bj_utils.py): This contains utility functions for our game. So far we have a score function that determines the score of a hand.
- [state.py](https://github.com/VinnieMuffinMan/CSE-150A-Project/blob/Milestone2/state.py): This contains the State class that stores the current game state, i.e. the player hand, the dealer hand, and the cards we have not yet seen (for card counting).
- [bot.py](https://github.com/VinnieMuffinMan/CSE-150A-Project/blob/Milestone2/bot.py): This bot chooses the player's action based on ideal probabilities i.e. not on observations. We would use this to compare with our data-driven agent and determine its accuracy.
- [test.py](https://github.com/VinnieMuffinMan/CSE-150A-Project/blob/Milestone2/test.py): This test file ensures that our bot in bot.py outputs the correct expected values.
- [main.py](https://github.com/VinnieMuffinMan/CSE-150A-Project/blob/Milestone2/main.py): This file compares the accuracy of our agent to the bot in bot.py.
- [data_bot.py](https://github.com/VinnieMuffinMan/CSE-150A-Project/blob/Milestone2/data_bot.py): This contains our utility-based agent which generates the dataset of observations and chooses the action that maximizes earnings based on these observations.
- [data_bot_sim.py](https://github.com/VinnieMuffinMan/CSE-150A-Project/blob/Milestone2/data_bot_sim.py): This simulates games for our agent to show its performance measure by outputting the agent's balance after a given number of games.

### Conclusion section: What is the conclusion of your 1st model? What can be done to possibly improve it?
**Update:** Our model is evaluated by the player's balance after a number of games, a higher balance indicating better performance (a positive final balance would be ideal). Overall, the model performed decently but could definitely be improved as evidenced by the negative balance after 200 games as shown in the graph below:

![evaluation](balance_seed_0.png)

The model did well with making the right decisions: we compared the expected values for each decision that it calculated with those calculated in bot.py (which finds the true expected values) and found that they often agreed on which action had the highest expected value. The model also did well with generating observations, only considering those that match the current game state so that it rejects irrelevant data. However, the model is limited by the number of observations it generates and its lack of variable betting, causing it to perform suboptimally. Improving the model would most likely involve generating more observations to increase the precision of expected values as well as adding some kind of variable betting to allow for more advantage play. **(end of update)**