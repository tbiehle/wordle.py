import pygame
import sys
import random
from key import Key
from letter import Letter
from settings import Settings
from popup import PopUp


class Wordle:
    def __init__(self):
        pygame.init()

        self.clock = pygame.time.Clock()

        self.screen = pygame.display.set_mode((1000, 750), pygame.RESIZABLE)
        self.settings = Settings(self)

        self.settings.screen_x, self.settings.screen_y = self.screen.get_size()

        pygame.display.set_caption(self.settings.name)

        self.keys = []
        self.letters = []
        self.change_position = True

        # settings for letter animations
        self.l_passed1 = False
        self.l_passed2 = False
        self.shake = False

        self.l_index = 0
        self.index_min = 0

        self.display_popup = False
        self.display_incorrect = False
        self.display_word = False
        self.reactions = ['Genius', 'Magnificent', 'Impressive', 'Splendid', 'Great', 'Phew']
        self.reaction_position = 0
        
        self.letter_list = ['a','b', 'c', 'd', 'e', 'f', 'g', 'h', 'i' ,'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

        self.guess = []
        self.guesses = []
        self.ans_dict = {}
        self.guessed = False
        self._create_anslist()
        self._create_guesslist()
        self.answer = self._generate_answer()
        self.allow_typing = True

        self.line_rect = pygame.Rect(0, 59, 500, 2)
        self._create_keyboard()
        self._create_board()
    

    def run_game(self):

        self.popup = PopUp(self)
        self.reset_popup = PopUp(self, (8, 201, 255))

        while True:
            self.screen.fill((18, 18, 19))
            self._check_events()
            self._update_screen()

            pygame.display.flip()
            self.clock.tick(30)


    def _update_screen(self):

        self._display_title()
        self._display_letters()
        self._display_keyboard()
        self._show_popup()


    def _show_popup(self):
        if self.display_popup:
            self.popup.center = (self.settings.screen_xmiddle, self.settings.screen_y - 3 * (self.settings.total_lheight))
            self.popup._draw_popup(self.reactions[self.reaction_position])

            self.reset_popup.center = (self.settings.screen_xmiddle, self.settings.screen_y - 3 * (self.settings.total_lheight))
            self.reset_popup._draw_popup('Press control to restart.')
        
        if self.display_incorrect:
            if self.popup.use <= 100:
                self.popup._draw_popup('Not in word list')

                if self.popup.use == 100:
                    self.popup.increase = False
                    self.display_incorrect = False
                    self.popup.use = 0
            
        for letter in self.letters:
            if self.shake:
                if letter.letter in self.guess and letter.color == self.settings.active_grey:
                    self._shake_letter(letter)

        if self.display_word:
            self.popup._draw_popup(f'{self.ans_string.upper()}')


    def _shake_letter(self, letter):

        if letter.step < 2:
            letter.xpos += 6
            letter.step += 1

        elif letter.step == 2:
            self.l_passed1 = True
            letter.step += 1

        elif letter.step > 2 and letter.step < 6 and self.l_passed1:
            letter.xpos -= 6
            letter.step += 1

        elif letter.step == 6 and self.l_passed1:
            self.l_passed2 = True
            self.l_passed1 = False
            letter.step += 1

        elif letter.step > 6 and letter.step < 10 and self.l_passed2:
            letter.xpos += 6
            letter.step +=1

            # Reset letters once everything is completed, making sure the change occurs before any letters can be updated.
            if letter.step == 9:
                for letter in self.letters:
                    letter.xpos = letter.final_xpos
                    letter.step = 0
                self.l_passed1 = False
                self.l_passed2 = False
                self.shake = False
                letter.step = 0



    def _reset_game(self):
        self.settings.screen_x, self.settings.screen_y = self.screen.get_size()
        self.ans_dict = {}
        self.letters.clear()
        self.keys.clear()
        self.guess.clear()
        self._create_board()
        self._create_keyboard()
        self._generate_answer()
        self.l_index = 0
        self.index_min = 0
        self.display_popup = False
        self.display_incorrect = False
        self.display_word = False
        self.popup.increase = False
        self.popup.use = 0
        self.reaction_position = 0
        self.allow_typing = True
        self.guessed = False


    def _create_anslist(self):
        with open('a_l.txt', 'r') as answer_file:
            
            self.answers = []
            answers = [word[:-1] for word in answer_file]
            for word in answers:
                answer_l_list = [letter for letter in word]
                self.answers.append(answer_l_list)
                self.guesses.append(answer_l_list)

        self.change_attempts = True


    def _create_guesslist(self):
        with open('a_g.txt', 'r') as guess_file:
            
            guesses = [word[:-1] for word in guess_file]
            for word in guesses:
                guess_l_list = [letter for letter in word]
                self.guesses.append(guess_l_list)


    def _generate_answer(self):
        """Randomly select the answer for the wordle."""
        self.ans_string = ""

        self.answer = self.answers[random.randint(0, 2314)] #  Choose word from word list

        ans_list = [letter for letter in self.answer] #  Create list of letters in answer word

        for letter in ans_list:
            if letter in self.ans_dict:
                self.ans_dict[letter] += 1
            else:
                self.ans_dict[letter] = 1

        for letter in ans_list:
            self.ans_string += letter
        print(self.answer)

        return ans_list


    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_mouse_events(mouse_pos)


    def _check_mouse_events(self, mouse_pos):
        for key in self.keys:
            if self.allow_typing:
                if key.rect.collidepoint(mouse_pos): 
                    if key.letter == '⌫':
                        self._delete_letter()

                    elif key.letter == 'enter':
                        self._submit_guess()

                    else: 
                        self._process_letter(key.letter)


    def _check_keydown_events(self, event):

        if event.key == pygame.K_ESCAPE:
            sys.exit()

        if self.allow_typing:
            if pygame.key.name(event.key) in self.letter_list:
                self._process_letter(pygame.key.name(event.key))

            if event.key == pygame.K_BACKSPACE or event.key == pygame.K_DELETE:
                self._delete_letter()

            if event.key == pygame.K_RETURN:
                self._submit_guess()
        
        if event.key == pygame.K_LCTRL:
            self._reset_game()


    def _process_letter(self, letter, delete=False):
        if self.l_index < 30:
            if len(self.guess) < 5:
                if not delete:
                    self.guess.append(letter)

                item = self.l_index
                self.letters[item].letter = letter
                if not delete:
                    self.letters[item].color = self.settings.active_grey
                # self.letters[item].xpos = self.settings.l_posx
                self.letters[item].draw_letter()


                if self.l_index < 30 and not delete:
                    self.l_index += 1


    def _submit_guess(self):
        correct_dict = {}
        skip = False

        if self.guess == self.answer:
            self.guessed = True
            self.display_popup = True
            self.allow_typing = False
        
        if self.guess not in self.guesses:
            self.display_incorrect = True
            self.shake = True
            return
        
        for i in range(self.settings.num_letters):
            if self.guess[i] == self.answer[i]:
                if self.guess[i] not in correct_dict:
                    correct_dict[self.guess[i]] = 0
                correct_dict[self.guess[i]] += 1

        
        for i in range(self.settings.num_letters):
            
            current_letter = self.l_index - (self.settings.num_letters - i)

            self.letters[current_letter].fill = 0

            if self.guess[i] in self.ans_dict:

                if self.ans_dict[self.guess[i]] > 0 and not self.guess[i] == self.answer[i]:

                    try:
                        if correct_dict[self.guess[i]] == self.ans_dict[self.guess[i]]:
                            skip = True

                    except KeyError:
                        skip = False

                    finally:
                        if not skip:
                            self.letters[current_letter].color = self.settings.possible
                        
                            for key in self.keys:
                                if key.letter == self.letters[current_letter].letter and key.color != self.settings.correct:
                                    key.color = self.settings.possible

                if self.guess[i] == self.answer[i]:

                    self.letters[current_letter].color = self.settings.correct

                    for key in self.keys:
                        if key.letter == self.letters[current_letter].letter:
                            key.color = self.settings.correct
                else:
                    self._make_letters_wrong(current_letter)

                self.ans_dict[self.guess[i]] -= 1

                
            else:
                self._make_letters_wrong(current_letter)

        self.guess.clear()
        self.index_min += self.settings.num_letters
        self._reset_ans_dict()
        if self.reaction_position < self.settings.allowed_guesses - 1 and not self.display_popup:
            self.reaction_position += 1

        if self.l_index == self.settings.num_letters * self.settings.allowed_guesses and self.guessed == False:
            self.display_word = True
                

    def _make_letters_wrong(self, letter):
        if self.letters[letter].color != self.settings.correct and self.letters[letter].color != self.settings.possible:
            self.letters[letter].color = self.settings.wrong
        for key in self.keys:
            if key.letter == self.letters[letter].letter:
                if key.color != self.settings.correct and key.color != self.settings.possible:
                    key.color = self.settings.wrong


    def _reset_ans_dict(self):
        self.ans_dict = {}

        for letter in self.answer:
            if letter in self.ans_dict:
                self.ans_dict[letter] += 1
            else:
                self.ans_dict[letter] = 1


    def _delete_letter(self):
        self.change_position = False

        if len(self.guess) > 0:
            self.guess.pop()

        if self.l_index > self.index_min:

            self.l_index -= 1
            self.letters[self.l_index].letter = ''
            self.letters[self.l_index].color = self.settings.dormant_grey
            

            self._process_letter(self.letters[self.l_index].letter, True)
                    

    def _display_letters(self):
        for letter in self.letters:
            letter.draw_letter()


    def _display_keyboard(self):
        for key in self.keys:
            key.draw_key()


    def _create_keyboard(self):
        
        # create the letters of the keyboard
        
        ypos = self.settings.screen_y - self.settings.total_kheight * 3

        row_one = ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p']
        row_two = ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l']
        row_three = ['z', 'x', 'c', 'v', 'b', 'n', 'm']

        xpos = (self.settings.screen_x / 2) - (5 * self.settings.total_kwidth)
        for letter in row_one:
            key = Key(self, letter, xpos, ypos)
            key.draw_key()
            xpos += self.settings.total_kwidth
            self.keys.append(key)
        ypos += self.settings.total_kheight

        xpos = (self.settings.screen_x / 2) - (4.5 * self.settings.total_kwidth)
        for letter in row_two:
            key = Key(self, letter, xpos, ypos)
            key.draw_key()
            xpos += self.settings.total_kwidth
            self.keys.append(key)
        ypos += self.settings.total_kheight
        
        xpos = (self.settings.screen_x / 2) - (3.5 * self.settings.total_kwidth)
        for letter in row_three:
            key = Key(self, letter, xpos, ypos)
            key.draw_key()
            xpos += self.settings.total_kwidth
            self.keys.append(key)
        ypos += self.settings.total_kheight

        # create the delete and enter keys
        
        delete = Key(self, '⌫', xpos, self.settings.screen_y - self.settings.total_kheight)
        enter = Key(self, 'enter', (self.settings.screen_x / 2) - (3.5 * self.settings.total_kwidth) - 70, self.settings.screen_y - self.settings.total_kheight)

        buttons = [delete, enter]
        for name in buttons:
            name.k_width = 65
            name.font_size = 18
            name.color = ((120, 120, 120))
            if name == delete: # Make the delete symbol and set its appropriate font size.
                delete.font = 'Apple Symbols'
                delete.font_size = 32
            name.draw_key()
            self.keys.append(name)


    def _create_board(self):
        ypos = ((self.line_rect.y + (self.settings.screen_y - self.settings.total_kheight * 3)) // 2) - 3 * self.settings.total_lheight

        for i in range(self.settings.allowed_guesses):
            xpos = (self.settings.screen_x / 2) - (2.5 * self.settings.total_lwidth) + (.5 * self.settings.l_spacing)

            for i in range(self.settings.num_letters):
                letter = Letter(self, xpos, ypos)
                letter.draw_letter()
                xpos += self.settings.total_lwidth
                self.letters.append(letter)

            ypos += self.settings.total_lheight

    
    def _display_title(self):
        name = self.settings.name

        font = pygame.font.SysFont('Helvetica Neue Bold', 64)
        text = font.render(f"{name.upper()}", True, self.settings.white)
        textRect = text.get_rect()

        textRect.center = ((self.settings.screen_x / 2), 30)

        self.line_rect = pygame.Rect(0, 0, 500, 2)
        self.line_rect.center = ((self.settings.screen_x / 2), 60)

        self.screen.blit(text, textRect)

        pygame.draw.rect(self.screen, self.settings.dormant_grey, self.line_rect)


wordle = Wordle()
wordle.run_game()
