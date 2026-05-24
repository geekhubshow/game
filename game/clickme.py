import pygame
import modules.db as db
import constants.colors as colors
import modules.input as input
import modules.button as button
from pathlib import Path

# Константы
WINDOW_HEIGHT = 540
WINDOW_WIDTH = 1000
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
SMALL_FONT = pygame.font.Font(None, 26)

# Настройки основного экрана
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Игра без названия')
screen.fill(colors.MAIN_COLOR)

run = True
page = "Auth"
# Конец настроек

# Блок с формой входа
auth_width = 480
auth_height = 240

auth_rect = pygame.Rect((WINDOW_WIDTH-auth_width)/2, (WINDOW_HEIGHT-auth_height-30)/2, auth_width, auth_height)
auth_surface = pygame.Surface((auth_rect.width, auth_rect.height))
pygame.draw.rect(auth_surface, colors.MAIN_COLOR, auth_surface.get_rect())

text_surface = FONT.render("Форма входа", True, colors.TEXT_COLOR)
auth_surface.blit(text_surface, ((auth_rect.width-text_surface.get_width())/2, PADDING))

login_text_surface = SMALL_FONT.render("Логин", True, colors.TEXT_COLOR)
password_text_surface = SMALL_FONT.render("Пароль", True, colors.TEXT_COLOR)

auth_surface.blit(login_text_surface, (PADDING*2, 85))
auth_surface.blit(password_text_surface, (PADDING*2, input.INPUT_HEIGHT+105))

login_input = input.Input()
password_input = input.Input(True)

def on_login():
    if login_input.value == test_login and password_input.value == test_password:
        change_page("Game")

def change_page(page_name):
    global page
    page = page_name

sing_in_button = button.Button("Войти", 50, 120, on_login)
sing_in_button.create_rect(270, 120+input.INPUT_HEIGHT*2)

registration_button = button.Button("У меня нет аккаунта", 50, 200, callback=lambda: change_page("Registration"))
registration_button.create_rect(50, 120+input.INPUT_HEIGHT*2)

# Конец блока

test_login = "1234"
test_password = "4321q"

# Основной цикл
while run:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            run = False

        if page == "Auth":
            login_input.handle_event(e, (auth_rect.x, auth_rect.y))
            password_input.handle_event(e, (auth_rect.x, auth_rect.y))
            sing_in_button.handle_event(e,(auth_rect.x, auth_rect.y))
            registration_button.handle_event(e,(auth_rect.x, auth_rect.y))

    # Отрисовка блока входа
    if page == "Auth":
        screen.fill(colors.SECONDARY_COLOR)
        screen.blit(auth_surface, auth_rect.topleft)

        login_input.draw_input(auth_surface, 150,80)
        password_input.draw_input(auth_surface, 150,100+input.INPUT_HEIGHT)

        sing_in_button.draw_button(auth_surface)
        registration_button.draw_button(auth_surface)

    elif page == "Game":
        screen.fill(colors.MAIN_COLOR)

    elif page == "Registration":
        screen.fill(colors.MAIN_COLOR)

    pygame.display.flip()

pygame.quit()