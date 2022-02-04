import pygame

class Settings:

    def __init__(self, game):
        #Settings for the display.
        self.bg_color = (0, 0, 0)
        self.screen_x, self.screen_y = game.screen.get_size()
        
        self.screen_size = (self.screen_x, self.screen_y)
        self.screen_xmiddle = self.screen_x // 2

        #Changeable settings for the game.
        self.num_letters = 5
        self.allowed_guesses = 6
        self.name = "wordle.py"

        # Settings for the keyboard.
        self.correct = (83, 141, 78)
        self.wrong = (58, 58, 60)
        self.possible = (181, 159, 60)
        self.k_new = (130, 131, 132)
        self.white = (255, 255, 255)
        self.black = (0, 0, 0)
        self.k_width = 40
        self.k_height = 50
        self.k_spacing = 5
        self.total_kwidth = self.k_width + self.k_spacing
        self.total_kheight = self.k_height + self.k_spacing
        self.keyboard_font = 'Helvetica Neue Bold'

        #Settings for the board.
        self.l_font = 'Helvetica Neue Bold'
        self.dormant_grey = (50, 50, 50)
        self.active_grey = pygame.Color(134, 136, 138)
        self.l_width = 65
        self.l_height = 65
        self.l_spacing = 5
        self.total_lwidth = self.l_width + self.l_spacing
        self.total_lheight = self.l_height + self.l_spacing

        #Settings for the popup.
        self.restart_message = 'Press control to restart.'