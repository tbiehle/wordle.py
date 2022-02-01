import pygame
from pygame.sprite import Sprite

class Key(Sprite):
    """A key on the keyboard of the display."""

    def __init__(self, wordle_game, letter, xpos, ypos):
        super().__init__()
        self.settings = wordle_game.settings

        self.xpos = xpos
        self.ypos = ypos
        self.font_size = 22

        self.letter = letter
        self.screen = wordle_game.screen
        self.color = self.settings.k_new
        self.letter_color = self.settings.white

        self.font = self.settings.keyboard_font
        
        self.k_width, self.k_height = self.settings.k_width, self.settings.k_height
        
        self.rect = pygame.Rect(self.xpos, self.ypos, self.k_width, self.k_height)


    def draw_key(self):
        self.rect = pygame.Rect(self.xpos, self.ypos, self.k_width, self.k_height)
        pygame.draw.rect(self.screen, self.color, self.rect, border_radius=3)
        font = pygame.font.SysFont(self.font, self.font_size)
        text = font.render(f'{self.letter.upper()}', True, self.letter_color)
        textRect = text.get_rect()
        textRect.center = (self.xpos + (self.k_width // 2), self.ypos + (self.k_height // 2))
        
        self.screen.blit(text, textRect)