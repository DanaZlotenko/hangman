# Problem Set 2, hangman.py
# Name: Zlotenko Bohdana
# Students group: KM-04
# Collaborators: Alexey Garmash
# Time spent: really a lot

import random
from string import ascii_lowercase

WORDLIST_FILENAME = "words.txt"
VOWELS = ('a', 'e', 'i', 'o', 'u')
UNKNOWN_LETTER = "_ "
HINT = "*"

warnings = 3
guesses = 6
letters = ascii_lowercase
letters_guessed = []
word_letters_guessed = []


def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.

    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    wordlist = inFile.readline().split()
    # wordlist: list of strings
    print("  ", len(wordlist), "words loaded.")
    return wordlist


def choose_word(wordlist):
    """
    wordlist (list): list of words (strings)

    Returns a word from wordlist at random
    """
    return random.choice(wordlist)


wordlist = load_words()
word = choose_word(wordlist)


def get_total_score(secret_word, guesses_remaining):
    """
    secret_word: string, the word the user is guessing; assumes all letters are
      lowercase
    guesses_remaining: guesses that are left
    returns: user's score;

    """

    total_score = len(set(secret_word)) * guesses_remaining
    return total_score


def is_word_guessed(secret_word, letters_guessed):
    """
    secret_word: string, the word the user is guessing; assumes all letters are
      lowercase
    letters_guessed: list (of letters), which letters have been guessed so far;
      assumes that all letters are lowercase
    returns: boolean, True if all the letters of secret_word are in letters_guessed;
      False otherwise
    """

    if set(secret_word) == set(letters_guessed):
        print('-' * 20, f'\nCongratulations, you won!\nTotal score: {get_total_score(word, guesses)}')
        return True
    else:
        return False


def get_guessed_word(secret_word, letters_guessed):
    """
    secret_word: string, the word the user is guessing
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string, comprised of letters, underscores (_), and spaces that represents
      which letters in secret_word have been guessed so far.
    """
    result = []
    for char in secret_word:
        if char not in letters_guessed:
            result.append(UNKNOWN_LETTER)  # append a "_" symbol to a word
        elif char in letters_guessed:
            result.append(char)  # append guessed letters to a word
    return ''.join(result)


def get_available_letters(letters_guessed):
    """
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string (of letters), comprised of letters that represents which letters have not
      yet been guessed.
    """

    result = []
    for i in letters:
        if i not in letters_guessed:
            result.append(i)
    return ''.join(result)


def is_ascii(user_guess):
    """
    user_guess: input the user is trying to guess;
    returns: True if input is letter, otherwise False
    """
    is_letter = user_guess != '' and user_guess.lower() in ascii_lowercase  # checks if input in ascii code
    return is_letter


def get_warnings(user_guess, my_word):
    """
    Func checks user input for invalid values and repeated letters;
    user_guess: input the user is trying to guess;
    my_word: string with _ characters, current guess of secret word;
    returns: boolean - True and append letter to list available letters,
    otherwise False, print information message about
    repeated  letter or use of a banned symbol
    and take away warnings;
    """
    global letters, letters_guessed, warnings, guesses

    is_warning = is_ascii(user_guess) and user_guess in letters  # checks if input a valid letter
    if is_warning:  # if user's guess was correct
        if user_guess in my_word:
            word_letters_guessed.append(user_guess)
        letters_guessed.append(user_guess)
        letters = get_available_letters(letters_guessed)
    else:  # if user's guess was incorrect
        warnings -= 1
        if warnings >= 0:
            print(f'Oops! That is not a valid symbol or you already entered that letter. '
                  f'You have {warnings} warnings left: ', get_guessed_word(my_word, letters_guessed))
        else:
            guesses -= 1
    return is_warning


def get_guesses(user_guess, my_word):
    """
    user_guess: input the user is trying to guess;
    my_word: string with _ characters, current guess of secret word;
    returns: boolean - True, prints information message
    and calls func get_guessed_word, if user_guess in word,
    otherwise False, information message and take away attempts (guesses);
    """
    global letters_guessed, guesses

    is_guessed = user_guess in my_word
    if is_guessed:  # if user guessed a letter
        print('Good guess:', get_guessed_word(my_word, letters_guessed))
    else:  # if user didn't guess a letter
        guesses -= 2 if user_guess in VOWELS else 1
        if guesses >= 0:
            print(f'Oops! That letter is not in my word.\n'
                  f'Please guess a letter: {get_guessed_word(my_word, letters_guessed)}')
    return is_guessed


print('Welcome to the game Hangman!')
print("I'm thinking of a word that is", len(word), "letters long.\nYou have ", warnings, "warnings and", guesses,
      "guesses left")


def hangman(secret_word, game_mode):
    """
    secret_word: string, the secret word to guess.
    game_mode: 1 - without hints, 2 - with hints
    returns:
    Starts up an interactive game of Hangman.

    """
    global warnings, guesses, letters, letters_guessed
    if 0 or guesses <= 0:  # if the user has run out of guesses
        return print('-' * 20, f'\nSorry, you ran out of guesses/warnings. The word was else:\n'
                               f'"{secret_word}"')

    print('-' * 20, f'\nYou have {guesses} guesses left.\nAvailable letters: {letters}')
    user_guess = str(input('Please guess a letter: ')).lower()

    if user_guess == HINT and game_mode:  # if the user has input "*" symbol
        random_words = show_possible_matches(get_guessed_word(secret_word, letters_guessed))
        print('Possible word matches are:', ', '.join(random_words))  # show 10 possible matches
        return hangman(secret_word, game_mode)

    elif not get_warnings(user_guess, secret_word) or not get_guesses(user_guess, secret_word) \
            or not is_word_guessed(secret_word, word_letters_guessed):
        return hangman(secret_word, game_mode)


def match_with_gaps(my_word, other_word):
    """
    my_word: string with _ characters, current guess of secret word
    other_word: string, regular English word
    returns: boolean, True if all the actual letters of my_word match the
        corresponding letters of other_word, or the letter is the special symbol
        _ , and my_word and other_word are of the same length;
        False otherwise:
    """

    counter = 0
    my_word = my_word.replace(' ', '')
    if len(my_word) == len(other_word):
        for i in range(len(my_word)):
            if my_word[i] == '_' or my_word[i] == other_word[i]:  # checks if letter in word fits letter in other word
                continue
            else:
                counter += 1
        if counter == 0:
            return True
        else:
            return False


def show_possible_matches(my_word):
    """
    my_word: string with _ characters, current guess of secret word
    returns: an string of similar words if matches are True,
             if matches are False - returns information message(string)
             Keep in mind that in hangman when a letter is guessed, all the positions
             at which that letter occurs in the secret word are revealed.
             Therefore, the hidden letter(_ ) cannot be one of the letters in the word
             that has already been revealed.

    """

    show = []

    for word in wordlist:
        if match_with_gaps(my_word, word):
            show.append(word)

    if len(show) != 0:
        return random.choices(show, k=10)  # chooses random 10 words

    else:
        return 'No matches found'


if __name__ == "__main__":
    hangman(word, 1)
