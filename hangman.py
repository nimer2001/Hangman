########################################################
# FILE : hangman.py
# WRITER : NIMER NAJAR , NIMER_123 , 323015727
# EXERCISE : ex4
# DESCRIPTION: this program creates the hangman game
########################################################
from hangman_helper import *


def update_word_pattern(word, pattern, letter):
    """
        this function update the current pattern and return it
        :param word: a word
        :param pattern: the current pattern
        :param letter: a letter
        :return: an updated pattern that has the letter in it
        """
    new_list = list(pattern)
    updated_pattern = ""
    for item in range(len(word)):
        if word[item] == letter:
            new_list[item] = letter
    for i in new_list:
        updated_pattern += str(i)
    return updated_pattern


def guess_was_letter(pattern1, wrong_guesses, score, input_guess, random_word):
    """
    this is an additional function that is used when the user guesses a letter
    :param pattern1: current pattern
    :param wrong_guesses: wrong guesses list
    :param score: current score
    :param input_guess: the input guess
    :param random_word: a word
    :return: a message,an updated pattern,wrong guesses list,an updated score
    """
    count = 0
    if len(input_guess) > 1 or not input_guess.isalpha() or not input_guess.islower():
        msg1 = "your input is not valid"
    elif input_guess in pattern1 or input_guess in wrong_guesses:
        msg1 = "you already selected this letter"
    else:
        score -= 1
        if input_guess in random_word:
            msg1 = "nice,your guess is right!"
            for i in range(len(random_word)):
                if random_word[i] == input_guess:
                    count += 1
                pattern1 = update_word_pattern(random_word, pattern1, input_guess)
            n = (count * (count + 1)) // 2
            score += n
        else:
            wrong_guesses.append(input_guess)
            msg1 = "wrong guess,try again!"
    return msg1, pattern1, wrong_guesses, score


def guess_was_word(score, input_guess, random_word, pattern1):
    """
    this function is an additional function that is used if the user guessed a word
    and a current pattern
    :param score: current score
    :param input_guess: the user guess
    :param random_word: a word
    :param pattern1: current pattern
    :return: a message, an updated pattern,an updated score
    """
    msg1 = ""
    score -= 1
    if input_guess == random_word:
        n1 = 0
        count1 = 0
        for i in range(len(pattern1)):
            if pattern1[i] == "_":
                count1 += 1
        n1 += count1 * (count1 + 1) // 2
        score += n1
        pattern1 = random_word
    else:
        msg1 = "your guess is wrong,try again!"
    return msg1, pattern1, score


def guess_was_hint(score, word_list, pattern1, wrong_guesses):
    """
    this is an additional function that is used when the user wants a hint
    :param score: current score
    :param word_list: a list of words
    :param pattern1: the current pattern
    :param wrong_guesses: wrong guesses list
    :return: a message and an updated score
    """
    score -= 1
    msg1 = "don't forget that asking for a hint does cost you a point!"
    new_list = filter_words_list(word_list, pattern1, wrong_guesses)
    n = len(new_list)
    if n > HINT_LENGTH:
        new_list1 = help3(new_list)
        show_suggestions(new_list1)
    else:
        show_suggestions(new_list)
    return msg1, score


def run_single_game(word_list, score):
    """
        this function runs one game and returns the score of the player at the end of the game
        :param word_list:list of words
        :param score:the number of points the player starts the game with
        :return:the score of the player at the end of the game
        """
    random_word = get_random_word(word_list)
    wrong_guesses = []
    pattern1 = "_" * len(random_word)
    msg1 = "Game started,Good luck!"
    while ("_" in pattern1) and score > 0:
        display_state(pattern1, wrong_guesses, score, msg1)
        input_type, input_guess = get_input()
        if input_type == LETTER:
            msg1, pattern1, wrong_guesses, score = guess_was_letter \
                (pattern1, wrong_guesses, score, input_guess, random_word)
        elif input_type == WORD:
            msg1, pattern1, score = guess_was_word(score, input_guess, random_word, pattern1)
        elif input_type == HINT:
            msg1, score = guess_was_hint(score, word_list, pattern1, wrong_guesses)
    if score > 0:
        msg1 = "congratulation you have won"
        display_state(pattern1, wrong_guesses, score, msg1)
    else:
        msg1 = f"you have lost,the word was {random_word}"
        display_state(pattern1, wrong_guesses, score, msg1)
    return score


def help3(new_list):
    """
    this function is an additional function that receives a list
    :param new_list: a list of words
    :return: returns a list in a specific places
    """
    n = len(new_list)
    new_list1 = []
    for i in range(HINT_LENGTH):
        new_list1.append(new_list[n * i // HINT_LENGTH])
    return new_list1


def help1(word, pattern):
    """
    this is an additional function that receives a word and a current pattern
    :param word: a word
    :param pattern: current pattern
    :return: true if the pattern matches the word
    """
    for i in range(len(pattern)):
        if pattern[i] != "_" and pattern[i] != word[i]:
            return False
        pattern1 = update_word_pattern(word, pattern, pattern[i])
        if pattern1 != pattern:
            return False
    return True


def help2(word, wrong_guess):
    """
    this is an additional function that receives a word and a wrong_guess list of characters
    :param word: a word
    :param wrong_guess: a list
    :return: true if all the characters in the word are not in the list
    """
    for i in word:
        if i in wrong_guess:
            return False
    return True


def filter_words_list(words, pattern, wrong_guess_lst):
    """
    it receives a list of words and a pattern and a wrong_guess_lst
    :param words: list of words
    :param pattern: current pattern
    :param wrong_guess_lst: wrong_guess_lst
    :return:  a list of words that matches the current pattern and the wrong guess_lst
    """
    new_list = []
    for i in words:
        if len(i) == len(pattern) and help2(i, wrong_guess_lst) and help1(i, pattern):
            if i not in new_list:
                new_list.append(i)

    return new_list


def main():
    """
        runs the game(could be one or more)
        """
    list_of_words = load_words(file='words.txt')
    number_of_games = 0
    score = run_single_game(list_of_words, POINTS_INITIAL)
    number_of_games += 1
    while True:

        if score > 0:
            msg = f"your number of games is {number_of_games},your current score is {score},do you want to play again?"
            user_selection = play_again(msg)
            if user_selection:
                score = run_single_game(list_of_words, score)
                number_of_games += 1
            else:
                break
        else:
            msg = f"your number of games is {number_of_games},your current score is {score}" \
                  f",do you want to start a new series of games?"
            user_selection = (play_again(msg))
            if user_selection:
                score = run_single_game(list_of_words, POINTS_INITIAL)
                number_of_games = 1
            else:
                break


if __name__ == '__main__':
    main()
