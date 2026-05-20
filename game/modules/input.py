import pygame

INPUT_HEIGHT = 30
INPUT_WIDTH = 300


class Input:
    def __init__(self, x, y):
        self.value = ""
        self.rect = None
        self.x = x
        self.y = y
        self.active = False

    def draw_input(self, block):
        FONT = pygame.font.Font(None, 32)
        self.rect = pygame.Rect(self.x, self.y, INPUT_WIDTH, INPUT_HEIGHT)

        pygame.draw.rect(block, (200,200,200), self.rect)

        color = (0,0,0) if self.active else (100,100,100)
        pygame.draw.rect(block, color, self.rect, 2)

        text_surface = FONT.render(self.value, True, (0, 0, 0))
        block.blit(text_surface, (self.rect.x + 5, self.rect.y + 5))
