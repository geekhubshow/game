import pygame
from game.constants import colors

class Button:
    def __init__(self, text, height, width, color, x, y):
        self.text = text
        self.height = height
        self.width = width
        self.font = pygame.font.Font(None, 24)
        self.rect = None
        self.color = color
        self.x = x
        self.y = y

    def create_rect(self):
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw_button(self, screen):
        # Создайте поверхность для кнопки
        button_surface = pygame.Surface((self.width, self.height))
        button_surface.fill(self.color)

        # Отображение текста на кнопке
        text = self.font.render(self.text, True, (0, 0, 0))
        text_rect = text.get_rect(
            center=(button_surface.get_width() / 2,
                    button_surface.get_height() / 2))

        button_surface.blit(text, text_rect)

        pygame.draw.rect(screen, (200,200,200), self.rect)
        screen.blit(button_surface, (self.x, self.y))


