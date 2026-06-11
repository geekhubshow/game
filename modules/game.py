import pygame
import random
import modules.db as db

# Константы
WIDTH = 800
HEIGHT = 400
GROUND_LEVEL = 330

class Dino:

    def __init__(self):
        self.x = 100
        self.y = GROUND_LEVEL - 30
        self.width = 30
        self.height = 30
        self.vy = 0
        self.on_ground = True

    def jump(self):
        if self.on_ground:
            self.on_ground = False
            self.vy = -12

    def update(self):
        if not self.on_ground:
            self.vy += 0.8
            self.y += self.vy

            if self.y >= GROUND_LEVEL - self.height:
                self.y = GROUND_LEVEL - self.height
                self.on_ground = True
                self.vy = 0

    def draw(self, surface):
        pygame.draw.rect(surface, (50, 50, 50), (self.x, self.y, self.width, self.height))
        pygame.draw.circle(surface, (255, 255, 255), (self.x + 25, self.y + 8), 3)
        pygame.draw.circle(surface, (0, 0, 0), (self.x + 25, self.y + 8), 1)

    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)


class DinoRunGame:
    def __init__(self, id_user, x=0, y=0, width=WIDTH, height=HEIGHT):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x, y, width, height)

        # Игровые переменные
        self.dino = Dino()
        self.cactuses = []
        self.score = 0
        self.best = self.load_best_score()
        self.game_over = False
        self.speed = 5

        # Таймер для создания кактусов
        self.spawn_timer = 0
        self.spawn_delay = random.randint(60, 120)
        self.ground_offset = 0

        # Шрифты
        self.big_font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)

        # Цвета
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.GRAY = (100, 100, 100)
        self.DARK = (50, 50, 50)

        self.id_user = id_user

    def load_best_score(self):
        try:
            with open("highscore.txt", "r") as f:
                return int(f.read())
        except:
            return 0

    def save_best_score(self, score):
        with open("highscore.txt", "w") as f:
            f.write(str(score))

    def create_cactus(self):
        if random.choice([True, False]):
            return {
                'x': self.width,
                'y': GROUND_LEVEL - 30,
                'w': 15,
                'h': 30,
                'speed': self.speed
            }
        else:
            return {
                'x': self.width,
                'y': GROUND_LEVEL - 20,
                'w': 10,
                'h': 20,
                'speed': self.speed
            }

    def update_cactus(self, cactus):
        cactus['x'] -= cactus['speed']

    def is_offscreen(self, cactus):
        return cactus['x'] + cactus['w'] < 0

    def draw_ground(self, surface):
        pygame.draw.rect(surface, self.GRAY, (0, GROUND_LEVEL, self.width, self.height - GROUND_LEVEL))
        pygame.draw.line(surface, self.DARK, (0, GROUND_LEVEL), (self.width, GROUND_LEVEL), 2)

        line_w = 20
        gap = 30
        for i in range(-int(self.ground_offset % (line_w + gap)), self.width, line_w + gap):
            pygame.draw.rect(surface, self.DARK, (i, GROUND_LEVEL - 5, line_w, 3))

        self.ground_offset += self.speed / 2

    def update(self):
        if not self.game_over:
            self.dino.update()

            # Создаем кактусы
            self.spawn_timer += 1
            if self.spawn_timer >= self.spawn_delay:
                can_spawn = True
                if self.cactuses:
                    last = self.cactuses[-1]
                    if last['x'] > self.width - 100:
                        can_spawn = False

                if can_spawn:
                    self.cactuses.append(self.create_cactus())

                self.spawn_timer = 0
                self.spawn_delay = random.randint(50, 100)

            # Двигаем кактусы
            for cactus in self.cactuses[:]:
                self.update_cactus(cactus)
                if self.is_offscreen(cactus):
                    self.cactuses.remove(cactus)
                    self.score += 10

            # Увеличиваем скорость
            if self.score > 0:
                self.speed = min(12, 5 + self.score // 100)

            # Обновляем скорость кактусов
            for cactus in self.cactuses:
                cactus['speed'] = self.speed

            # Проверка столкновений
            dino_rect = self.dino.rect()
            for cactus in self.cactuses:
                cactus_rect = pygame.Rect(cactus['x'], cactus['y'], cactus['w'], cactus['h'])
                if dino_rect.colliderect(cactus_rect):
                    self.game_over = True
                    db.res(self.score, self.id_user)

    def draw(self, surface):
        # Создаем временную поверхность для игры
        game_surface = pygame.Surface((self.width, self.height))
        game_surface.fill(self.WHITE)

        # Земля
        self.draw_ground(game_surface)

        # Динозавр
        self.dino.draw(game_surface)

        # Кактусы
        for cactus in self.cactuses:
            pygame.draw.rect(game_surface, self.DARK, (cactus['x'], cactus['y'], cactus['w'], cactus['h']))

        # Интерфейс
        score_text = self.big_font.render(f"Score: {self.score}", True, self.BLACK)
        game_surface.blit(score_text, (10, 10))

        best_text = self.small_font.render(f"Best: {self.best}", True, self.GRAY)
        game_surface.blit(best_text, (10, 50))

        speed_text = self.small_font.render(f"Speed: {self.speed}", True, self.GRAY)
        game_surface.blit(speed_text, (10, 75))

        # Экран Game Over
        if self.game_over:
            overlay = pygame.Surface((self.width, self.height))
            overlay.set_alpha(120)
            overlay.fill(self.WHITE)
            game_surface.blit(overlay, (0, 0))

            over_text = self.big_font.render("GAME OVER", True, self.BLACK)
            restart_text = self.small_font.render("Press R to restart", True, self.GRAY)

            game_surface.blit(over_text, (self.width // 2 - 80, self.height // 2 - 50))
            game_surface.blit(restart_text, (self.width // 2 - 70, self.height // 2))

        surface.blit(game_surface, (self.x, self.y))

    def handle_event(self, event, surface_rect=None):
        mouse_pos = pygame.mouse.get_pos()
        if surface_rect:
            mouse_x = mouse_pos[0] - surface_rect[0] - self.x
            mouse_y = mouse_pos[1] - surface_rect[1] - self.y
            mouse_pos = (mouse_x, mouse_y)

        # Проверяем, находится ли мышь в области игры
        if not self.rect.collidepoint(mouse_pos):
            return False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not self.game_over:
                self.dino.jump()
                return True
            if event.key == pygame.K_r and self.game_over:
                self.reset()
                return True

        return False

    def reset(self):
        self.dino = Dino()
        self.cactuses = []
        self.score = 0
        self.game_over = False
        self.speed = 5
        self.spawn_timer = 0
        self.spawn_delay = random.randint(60, 120)
        self.ground_offset = 0

    def get_score(self):
        return self.score

    def is_game_over(self):
        return self.game_over
