import pygame

INPUT_HEIGHT = 30
INPUT_WIDTH = 300

class Input:
    def __init__(self, is_password = False):
        self.value = ""
        self.rect = None
        self.active = False
        self.is_password = is_password

    def draw_input(self, block, x, y):
        FONT = pygame.font.Font(None, 32)
        self.rect = pygame.Rect(x, y, INPUT_WIDTH, INPUT_HEIGHT)

        pygame.draw.rect(block, (200,200,200), self.rect)

        color = (0,0,0) if self.active else (100,100,100)

        text_surface = FONT.render("*" * len(self.value)  if self.is_password else self.value, True, (0, 0, 0))

        block.blit(text_surface, (self.rect.x + 5, self.rect.y + 5))
        pygame.draw.rect(block, color, self.rect, 2)

    def handle_event(self, event, surface_rect=None):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if surface_rect:
                mouse_x = event.pos[0] - surface_rect[0]
                mouse_y = event.pos[1] - surface_rect[1]
                mouse_pos = (mouse_x, mouse_y)
            else:
                mouse_pos = event.pos

            if self.rect and self.rect.collidepoint(mouse_pos):
                self.active = True
                return True
            else:
                self.active = False

        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                self.value = self.value[:-1]
            elif event.key == pygame.K_RETURN:
                self.active = False
                return True
            else:
                if len(self.value) < 10:
                    self.value += event.unicode
        return False