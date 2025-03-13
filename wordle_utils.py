def get_feedback(guess, answer, words):
    if len(guess) != 5 or guess not in words:
        return
    
    # For returning the correct number of yellow/green squares for each letter
    answer_counts = {letter: answer.count(letter) for letter in set(answer)}

    feedback = ["⬜"] * 5
    for i in range(len(guess)):
        if guess[i] == answer[i]:
            feedback[i] = "🟩"
            answer_counts[guess[i]] -= 1

    for i in range(len(guess)):
        if feedback[i] == "🟩":
            continue
        if guess[i] in answer_counts and answer_counts[guess[i]] > 0:
            feedback[i] = "🟨"
            answer_counts[guess[i]] -= 1

    feedback = "".join(feedback)
    return feedback