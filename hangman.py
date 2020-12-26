# Problem Set 2, hangman.py
# Name:
# Students group: KM-04
# Collaborators: -
# Time spent:

import random
from string import ascii_lowercase

WORDLIST_FILENAME = "words.txt"
VOWELS = frozenset('aeiou')
UNKNOWN_LETTER = "_"
HINT = "*"

warnings = 3
guesses = 6
letters = ascii_lowercase
letters_guessed = []


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
        print('-' * 20)
        print('Congratulations, you won!')
        print('Total score:', get_total_score(word, guesses))
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
            # append a "_" symbol to a word
            result.append(f'{UNKNOWN_LETTER} ')
        elif char in letters_guessed:
            # append guessed letters to a word
            result.append(char)
    return ''.join(result)


def get_available_letters(letters_guessed):
    """
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string (of letters), comprised of letters that represents which letters have not
      yet been guessed.
    """

    result = []
    for letter in letters:
        if letter not in letters_guessed:
            result.append(letter)
    return ''.join(result)


def is_ascii(user_guess):
    """
    user_guess: input the user is trying to guess;
    returns: True if input is letter, otherwise False
    """
    # checks if input in ascii code
    is_letter = user_guess != '' and user_guess.lower() in ascii_lowercase
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

    # checks if input a valid letter
    is_warning = user_guess in letters
    # if user's guess was correct
    if is_warning:
        if user_guess in my_word:
            letters_guessed.append(user_guess)
        letters_guessed.append(user_guess)
        letters = get_available_letters(letters_guessed)
    # if user's guess was incorrect
    else:
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
    # if user guessed a letter
    if is_guessed:
        print('Good guess:', get_guessed_word(my_word, letters_guessed))
    # if user didn't guess a letter
    else:
        guesses -= 2 if user_guess in VOWELS else 1
        if guesses > 0:
            print('Oops! That letter is not in my word.')
            print('Please guess a letter:', get_guessed_word(my_word, letters_guessed))
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
    # if the user has run out of guesses
    while guesses > 0:
        print('-' * 20)
        print('You have', guesses, 'guesses left.')
        print('Available letters:', letters)
        user_guess = str(input('Please guess a letter: ')).lower()

        # if the user has input "*" symbol
        if user_guess == HINT and game_mode:
            print('Possible word matches are:', show_possible_matches(get_guessed_word(secret_word, letters_guessed)))
            continue

        get_warnings(user_guess, secret_word)
        get_guesses(user_guess, secret_word)
        if is_word_guessed(secret_word, letters_guessed):
            break

    if guesses <= 0:
        return print(('-' * 20), f'\nSorry, you ran out of guesses/warnings. '
                                 f'The word was else:\n'
                                 f'"{secret_word}"')



def match_with_gaps(my_word, other_word):
    """
    my_word: string with _ characters, current guess of secret word
    other_word: string, regular English word
    returns: boolean, True if all the actual letters of my_word match the
        corresponding letters of other_word, or the letter is the special symbol
        _ , and my_word and other_word are of the same length;
        False otherwise:
    """


    if len(my_word) == len(other_word):
        for i in range(len(my_word)):
            # checks if letter in word fits letter in other word
            if my_word[i] == UNKNOWN_LETTER or my_word[i] == other_word[i]:
                continue
            else:
                return False
        return True



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
    my_word = my_word.replace(' ', '')

    for word in wordlist:
        if match_with_gaps(my_word, word):
            show.append(word)

    if len(show) != 0:
        return ' '.join(show)

    else:
        return 'No matches found'


if __name__ == "__main__":
    hangman(word, 1)
