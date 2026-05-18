import pygame
import modules.db as db
import constants.colors as colors
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

# Настройки основного экрана
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Игра без названия')
screen.fill(colors.MAIN_COLOR)
# Конец настроек

# Блок с игрой
game_h = WINDOW_HEIGHT-2*PADDING
game_block_rect = pygame.Rect(PADDING, PADDING, game_h, game_h)
# The end блок с игрой

run = True

# Основной цикл
while run:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            run = False

    # Отрисовка блока с игрой
    pygame.draw.rect(screen, colors.SECONDARY_COLOR, game_block_rect)
    pygame.draw.rect(screen, colors.BORDER_COLOR, game_block_rect, 3)
    # Конец отрисовки

    pygame.display.flip()

pygame.quit()