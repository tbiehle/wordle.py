import pygame
from key import Key

class ResetButton(Key):
    
    def __init__(self, game):
        self.settings = game.settings

        self.text = 'RESTART'
        self.xpos = self.settings.screen_x - 3 * (self.settings.k_width) - 8
        self.ypos = 8
        
        super().__init__(game, self.text, self.xpos, self.ypos)

        self.color = (1, 46, 26)

        self.k_width = self.settings.k_width * 3