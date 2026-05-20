import pygame
import modules.db as db
import constants.colors as colors
import modules.input as input
import modules.button as button
from pathlib import Path

# Константы
WINDOW_HEIGHT = 600
WINDOW_WIDTH = 950
PADDING = 20
BUTTON_HEIGHT = 50
ITEM_HEIGHT = 30

# Проверка существования БД
file_path = Path("src/data.db")
if not file_path.is_file():
    db.bd_create()
# Конец проверки

pygame.init()

FONT = pygame.font.Font(None, 32)

# Настройки основного экрана
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Игра без названия')
screen.fill(colors.MAIN_COLOR)
# Конец настроек

# Блок с игрой
game_h = WINDOW_HEIGHT-2*PADDING
game_block_rect = pygame.Rect(PADDING, PADDING, game_h, game_h)
# The end блок с игрой

# Блок с формой входа
auth_rect = pygame.Rect(PADDING+game_h/6, PADDING+game_h/3, game_h/1.5, game_h/3)
auth_input = input.Input(PADDING+game_h/6+35, PADDING+game_h/2.2)

auth_button = button.Button("Войти", 40, game_h/3, colors.SECONDARY_COLOR, PADDING+game_h/3, PADDING+game_h/3+game_h/4.5)
auth_button.create_rect()

text_surface = FONT.render("Введите ник", True, (0, 0, 0))
# Конец блока с формой входа

run = True
auth_selected = True

# Основной цикл
while run:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            run = False

        if e.type == pygame.MOUSEBUTTONDOWN:
            if auth_button.rect.collidepoint(e.pos):
                if len(auth_input.value) > 3:
                    auth_selected = False

            auth_input.active = True if auth_input.rect.collidepoint(e.pos) else False

        if e.type == pygame.KEYDOWN:
            if auth_input.active:
                if e.key == pygame.K_BACKSPACE:
                    auth_input.value = auth_input.value[:-1]
                else:
                    if len(auth_input.value) < 10:
                        auth_input.value += e.unicode


    mouse_pos = pygame.mouse.get_pos()

    # Отрисовка блока с игрой
    pygame.draw.rect(screen, colors.SECONDARY_COLOR, game_block_rect)
    pygame.draw.rect(screen, colors.BORDER_COLOR, game_block_rect, 3)
    # Конец отрисовки

    # Отрисовка блока входа
    if auth_selected:
        pygame.draw.rect(screen, colors.MAIN_COLOR, auth_rect)
        pygame.draw.rect(screen, colors.BORDER_COLOR, auth_rect, 3)

        auth_button.color = colors.BORDER_COLOR if auth_button.rect.collidepoint(mouse_pos) else colors.SECONDARY_COLOR
        auth_input.draw_input(screen)
        auth_button.draw_button(screen)

        screen.blit(text_surface, (PADDING+game_h/3+15, PADDING+game_h/2.5-10))
    # Конец отрисовки

    pygame.display.flip()

pygame.quit()