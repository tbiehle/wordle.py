import pygame

class PopUp:

    def __init__(self, game, color = ''):
        self.game = game
        self.settings = game.settings
        self.screen = game.screen
        self.use = 0
        self.word = ''

        if color:
            self.color = color
        else:
            self.color = self.settings.white

        font = pygame.font.SysFont(self.settings.l_font, 25)
        text = font.render(f'{self.word}', True, self.settings.black)
        textRect = text.get_rect()

        self.center = (self.game.settings.screen_x // 2) - (textRect.x / 2), (((self.game.line_rect.y + (self.game.settings.screen_y - self.game.settings.total_kheight * 3)) // 2) - (3 * self.game.settings.total_lheight) + self.game.line_rect.y) / 2

        self.increase = True

    def _draw_popup(self, word):
        self.increase = True

        font = pygame.font.SysFont(self.settings.l_font, 25)
        text = font.render(f'{word}', True, self.settings.black)
        textRect = text.get_rect()

        if word == self.settings.restart_message:
            textRect.center = (self.game.settings.screen_x // 2, self.game.settings.screen_y - 3 * (self.game.settings.total_lheight))
        else:
            textRect.center = (self.game.settings.screen_x // 2) - (textRect.x / 2), (((self.game.line_rect.y + (self.game.settings.screen_y - self.game.settings.total_kheight * 3)) // 2) - (3 * self.game.settings.total_lheight) + self.game.line_rect.y) / 2

        rect_width, rect_height = textRect.width + 30, textRect.height + 30

        self.rect = pygame.Rect(textRect.center[0] - (rect_width / 2), textRect.center[1] - (rect_height / 2), rect_width, rect_height)
        pygame.draw.rect(self.screen, self.color, self.rect, border_radius=8)

        self.screen.blit(text, textRect)

        if self.increase:
            self.use += 1
        else:
            self.increase = False
            self.use = 0
            self.name = ''