#Step 5

import random
import sqlite3
from hangman_art import stages, logo

def get_category():
    conn = sqlite3.connect('data/hangman.db')
    c = conn.cursor()

    c.execute('SELECT * FROM categories')
    categories = c.fetchall()
    
    print("Choose a category:")
    for i, category in enumerate(categories, 1):
        print(f"{i}. {category[1]}")
    
    choice = int(input("Enter the number of your choice: ")) - 1
    category = categories[choice]
    conn.close()
    return category[1], category[0]

def get_word(category_id):
    conn = sqlite3.connect('data/hangman.db')
    c = conn.cursor()

    c.execute('SELECT word FROM words WHERE category_id=?', (category_id,))
    words = c.fetchall()
    chosen_word = random.choice(words)[0]

    conn.close()
    return chosen_word

def hangman():
    category_name, category_id = get_category()
    chosen_word = get_word(category_id)
    word_length = len(chosen_word)
    lives = 6
    end_game = False
    display = ["_"] * word_length

    print(f"\nPssst, the solution is {chosen_word}.\n")
    print(f"The category is: {category_name}\n")

    while not end_game:
        guess = input("Guess a letter: ").lower()

        if guess in display:
            print(f"You've already guessed {guess}")
        else:
            for position in range(word_length):
                letter = chosen_word[position]
                if letter == guess:
                    display[position] = letter

            if guess not in chosen_word:
                lives -= 1
                print(f"You guessed {guess}, that's not in the word. You lose a life.")
                if lives == 0:
                    end_game = True
                    print("You lose.")
                    print(f"The word was {chosen_word}.")

        print(f"{' '.join(display)}")

        if "_" not in display:
            end_game = True
            print("You win!")

        print(stages[lives])

if __name__ == "__main__":
    hangman()