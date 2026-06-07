import pygame
from constants import colors

class Button:
    def __init__(self, text, height, width, callback = None):
        self.text = text
        self.height = height
        self.width = width
        self.font = pygame.font.Font(None, 24)
        self.rect = None
        self.color = (0,0,0)
        self.callback = callback

    def create_rect(self, x, y):
        self.rect = pygame.Rect(x, y, self.width, self.height)

    def draw_button(self, block):
        button_surface = pygame.Surface((self.width, self.height))
        button_surface.fill(self.color)

        text = self.font.render(self.text, True, (0, 0, 0))
        text_rect = text.get_rect(
            center=(button_surface.get_width() / 2,
                    button_surface.get_height() / 2))

        button_surface.blit(text, text_rect)

        pygame.draw.rect(block, (200,200,200), self.rect)
        block.blit(button_surface, (self.rect.x, self.rect.y))

    def handle_event(self, event, surface_rect=None):
        mouse_pos = pygame.mouse.get_pos()
        if surface_rect:
            mouse_x = mouse_pos[0] - surface_rect[0]
            mouse_y = mouse_pos[1] - surface_rect[1]
            mouse_pos = (mouse_x, mouse_y)

        self.color = colors.BORDER_COLOR if self.rect.collidepoint(mouse_pos) else colors.SECONDARY_COLOR

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect and self.rect.collidepoint(mouse_pos):
                if self.callback:
                    self.callback()
                return True

