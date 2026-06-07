import pygame
import modules.db as db
import constants.colors as colors
import modules.input as input
import modules.button as button
from pathlib import Path
from modules.game import DinoRunGame

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

FONT = pygame.font.Font(None, 30)
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

# Использую эти же поля в регистрации
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
    print(f"Changing page from {page} to {page_name}")  # Отладочный вывод
    page = page_name

sing_in_button = button.Button("Войти", 50, 120, on_login)
registration_button = button.Button("У меня нет аккаунта", 50, 200, callback=lambda: change_page("Registration"))

sing_in_button.create_rect(270, 120 + input.INPUT_HEIGHT * 2)
registration_button.create_rect(50, 120 + input.INPUT_HEIGHT * 2)
# Конец блока
# Блок с формой регистрации

reg_width = 480
reg_height = 300

reg_rect = pygame.Rect((WINDOW_WIDTH-reg_width)/2, (WINDOW_HEIGHT-reg_height-30)/2, reg_width, reg_height)
reg_surface = pygame.Surface((reg_rect.width, reg_rect.height))
pygame.draw.rect(reg_surface, colors.MAIN_COLOR, reg_surface.get_rect())

reg_text_surface = FONT.render("Форма регистрации", True, colors.TEXT_COLOR)
reg_surface.blit(reg_text_surface, ((reg_rect.width-reg_text_surface.get_width())/2, PADDING))

repassword_text_surface = SMALL_FONT.render("Повтор пароля", True, colors.TEXT_COLOR)

reg_surface.blit(login_text_surface, (PADDING, 85))
reg_surface.blit(password_text_surface, (PADDING, input.INPUT_HEIGHT+105))
reg_surface.blit(repassword_text_surface, (PADDING, input.INPUT_HEIGHT*2+125))

repassword_input = input.Input(True)

def on_reg_login():
    if password_input.value == repassword_input.value and len(login_input.value)>4:
        change_page("Game")

registration_in_button = button.Button("Зарегистрироваться", 50, 200, on_reg_login)
back_button = button.Button("Назад", 50, 120, callback=lambda: change_page("Auth"))

registration_in_button.create_rect(230, 140 + input.INPUT_HEIGHT * 3)
back_button.create_rect(50, 140 + input.INPUT_HEIGHT * 3)

# Конец блока

game = DinoRunGame(x=0, y=0, width=WINDOW_WIDTH-300, height=WINDOW_HEIGHT-100)
clock = pygame.time.Clock()

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

        elif page == "Registration":

            login_input.handle_event(e, (reg_rect.x, reg_rect.y))
            password_input.handle_event(e, (reg_rect.x, reg_rect.y))
            repassword_input.handle_event(e, (reg_rect.x, reg_rect.y))

            registration_in_button.handle_event(e,(reg_rect.x, reg_rect.y))
            back_button.handle_event(e,(reg_rect.x, reg_rect.y))

        elif page == "Game":
            game.handle_event(e)

    # Отрисовка блока входа
    if page == "Auth":
        screen.fill(colors.SECONDARY_COLOR)
        screen.blit(auth_surface, auth_rect.topleft)

        login_input.draw_input(auth_surface, 150,80)
        password_input.draw_input(auth_surface, 150,100+input.INPUT_HEIGHT)

        sing_in_button.draw_button(auth_surface)
        registration_button.draw_button(auth_surface)

    elif page == "Registration":
        screen.fill(colors.SECONDARY_COLOR)
        screen.blit(reg_surface, reg_rect.topleft)

        login_input.draw_input(reg_surface, 150,80)
        password_input.draw_input(reg_surface, 150,100+input.INPUT_HEIGHT)
        repassword_input.draw_input(reg_surface, 150,120+input.INPUT_HEIGHT*2)

        registration_in_button.draw_button(reg_surface)
        back_button.draw_button(reg_surface)

    elif page == "Game":
        screen.fill(colors.MAIN_COLOR)
        game.update()
        game.draw(screen)
        clock.tick(60)

    pygame.display.flip()


pygame.quit()