import pygame

class Letter:
    """A class to represent each box on the guess board."""
    def __init__(self, wordle_game, xpos, ypos):

        self.settings = wordle_game.settings
        self.screen = wordle_game.screen
        self.color = self.settings.dormant_grey

        self.letter = ''
        self.font = self.settings.l_font

        self.bounce = True
        self.start = True
        self.step = 0

        self.xpos = xpos
        self.ypos = ypos
        self.width = self.settings.l_width
        self.height = self.settings.l_height

        if self.letter:
            self.width += 5
            self.height += 5
    
        self.fill = 2


    def draw_letter(self):
        if self.letter and self.bounce:
            if self.start:
                self.xpos -= 5
                self.ypos -= 5
                self.width += 10
                self.height += 10
                self.start = False
            self._bounce()
        self.rect = pygame.Rect(self.xpos, self.ypos, self.width, self.height)
        pygame.draw.rect(self.screen, self.color, self.rect, self.fill)

        font = pygame.font.SysFont(self.font, 48)
        text = font.render(f'{self.letter.upper()}', True, self.settings.white)
        textRect = text.get_rect()
        textRect.center = (self.xpos + (self.width / 2), self.ypos + 3 + (self.height / 2))

        self.screen.blit(text, textRect)
        if not self.letter:
            self.start = True
            self.times_through = 0

    def _bounce(self):
        if self.width > self.settings.l_width and self.height > self.settings.l_height:
    
            self.width -= 2
            self.height -= 2
            if self.times_through < 5:
                self.xpos += 1
                self.ypos += 1
            self.times_through += 1


