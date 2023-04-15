import pathlib
import random
from string import ascii_letters, ascii_uppercase

from rich.console import Console
from rich.theme import Theme

console = Console(width=40, theme=Theme({'warning': 'red on yellow'}))
wordLength = 5
numGuesses = 6
wordList = 'wordList.txt'

def main():
    #pre-process
    words_path = pathlib.Path(__file__).parent / wordList
    word = get_random_word(wordList=words_path.open().read().split('\n'))
    guesses = ['_' * wordLength] * numGuesses

    #process
    for idx in range(6):
        refresh_page(headline=f'Guess {idx + 1}')
        show_guesses(guesses, word)

        guesses[idx] = guess_word(previous_guesses=guesses[:idx])
        if guesses[idx] == word:
            break
        
    #post-process
    game_over(guesses, word, guessed_correctly=guesses[idx] == word)


def get_random_word(wordList):
    if words := [
        word.upper()
        for word in wordList
        if len(word) == wordLength and all(letter in ascii_letters for letter in word)
    ]:
        return random.choice(words)
    console.print(f"No words of length {wordLength} in the word list", style='warning')
    raise SystemExit()


def guess_word(previous_guesses):
    guess = console.input('\nGuess the Word: ').upper()
    
    if guess in previous_guesses:
        console.print(f"You've already guessed {guess}", style='warning')
        return guess_word(previous_guesses)
    elif len(guess) != wordLength:
        console.print(f'{guess} does not have a length of {wordLength}. All guess must have a length of {wordLength}', style='warning')
        return guess_word(previous_guesses)
    elif any((invalid := letter) not in ascii_letters for letter in guess):
        console.print(f'{guess} contains a non-letter. Guesses may only contain letters.')
    else:
        return guess


def show_guesses(guesses, word):
    letter_status = {letter: letter for letter in ascii_uppercase}
    for guess in guesses:
        styled_guess = []
        for letter, correct in zip(guess, word):
            if letter == correct:
                style = 'bold white on green'
            elif letter in word:
                style = 'bold white on yellow'
            elif letter in ascii_letters:
                style = 'white on #666666'
            else:
                style = 'dim'
            styled_guess.append(f'[{style}]{letter}[/]')
            if letter != '_':
                letter_status[letter] = f"[{style}]{letter}[/]"

        console.print(''.join(styled_guess), justify='center')
    console.print('\n' + ''.join(letter_status.values()), justify='center')


def refresh_page(headline):
    console.clear()
    console.rule(f'[bold blue]:leafy_green: {headline} :leafy_green:[/]\n')


def game_over(guesses, word, guessed_correctly):
    refresh_page(headline='Game Over')
    show_guesses(guesses, word)

    if guessed_correctly:
        console.print(f'\n[bold white on green]Correct! The word is {word}.[/]')
    else:
        console.print(f'\n[bold white on red]Out of guesses. The word was {word}.[/]')


if __name__ == "__main__":
    main()