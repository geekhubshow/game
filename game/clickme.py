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

pygame.init()

# Основной экран
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Игра без названия')
screen.fill(colors.MAIN_COLOR)

run = True

while run:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            run = False

    pygame.display.flip()

pygame.quit()