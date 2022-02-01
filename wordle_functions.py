import random
from termcolor import colored

class Functions:
    def __init__(self):
        self.attempts = 6
        self.solved = False
        self.guess =  ''
        self.done = False
        self.valid = True

        with open('wordle_list.txt', 'r') as answer_file:
            answers = [word[:-1] for word in answer_file]
        self.answers = answers
        self.ans_cols = ['white', 'white', 'white', 'white', 'white']

        self.answer = self._generate_answer()
        self.answer_string = f"{self.answer[0] + self.answer[1] + self.answer[2] + self.answer[3] + self.answer[4]}"

        self.change_attempts = True


    def _generate_answer(self):
        """Randomly select the answer for the wordle."""

        answer = self.answers[random.randint(0,4534)] #  Choose word from word list

        ans_list = [letter for letter in answer] #  Create list of letters in answer word

        return ans_list

    def _get_guess_info(self):
        """Define variables around the guess."""

        self.guess_string = f"{self.guess[0] + self.guess[1] + self.guess[2] + self.guess[3] + self.guess[4]}"
    

    def _check_guess(self, guess, answer):
        """Compare the user's guess to the answer, and inform the player of what is right and wrong."""

        if guess == answer:
            self.solved = True
            self.done = True
            self.ans_cols = ['green', 'green', 'green', 'green', 'green']
            return

        
        if self.guess_string not in self.answers:
            print('Word not in word list.')
            self.change_attempts = False
            self.valid = False
            return
        
        correct_letters = []
        maybes = []

        for letter in guess:
            if letter == answer[guess.index(letter)]:
                # print(f"{letter} is in the correct position (position {guess.index(letter) + 1}).")

                self.ans_cols[guess.index(letter)] = "green"
                correct_letters.append(letter)

        for letter in set(guess):
            if letter in answer:
                if letter not in correct_letters:
                    # print(f"{letter} is in the word.")
                    self.ans_cols[guess.index(letter)] = "yellow"
                    correct_letters.append(letter)


    def _render_guess(self, guess):
        """Render a colored version of the guess indicating the right letters."""
        guess_render = colored(guess[0].upper(), self.ans_cols[0]) + colored(guess[1].upper(), self.ans_cols[1]) + colored(guess[2].upper(), self.ans_cols[2]) + colored(guess[3].upper(), self.ans_cols[3]) + colored(guess[4].upper(), self.ans_cols[4])
        self.ans_cols = ['white', 'white', 'white', 'white', 'white']
        return guess_render


    def play(self):
        """Play the game."""
        print(self.answer)
        while not self.done:
            while True:
                self.guess = input('Please type a five letter guess. - ')
                if len(self.guess) == 5:
                    break
            self.guess = [letter.lower() for letter in self.guess]

            self._get_guess_info()
            self._check_guess(self.guess, self.answer)
            if self.valid:
                print(self._render_guess(self.guess))
            self.valid = True
            
            if self.change_attempts:
                self.attempts -= 1
                if self.attempts == 0:
                    print(f'Sorry, you have failed. The word was: {self.answer_string}')
                    self.done = True
            
            if not self.solved:
                print(f'Guesses remaining: {self.attempts}')
            self.change_attempts = True

        
        if self.solved:
            self.answer = f"{self.answer[0] + self.answer[1] + self.answer [2] + self.answer[3] + self.answer[4]}"
            print(f'Congratulations, you win! The word was: {self.answer.upper()}')
        if not self.solved:
            print(f"Sorry, you have failed. The answer was: {self.answer_string.upper()}")

wordle = Functions()
wordle.play()