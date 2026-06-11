import pygame
import constants.colors as colors

SCROLLBAR_WIDTH = 10
ITEM_HEIGHT = 30
PADDING = 2

class Scroll:
    def __init__(self, items):
        self.items = items
        self.scroll_y = 0
        self.max_scroll = 0
        self.font = pygame.font.Font(None, 24)
        self.block = None
        self.dragging = False
        self.drag_start_y = 0
        self.drag_start_scroll = 0
        self.scroll_handle_rect = None
        self.scrollbar_rect = None

    def draw_scroll(self, block, x, y):
        self.block = block
        self.rect = pygame.Rect(x, y, block.get_width(), block.get_height())

        content_height = len(self.items) * ITEM_HEIGHT
        view_height = self.rect.height
        self.max_scroll = max(0, content_height - view_height)

        content_surf = pygame.Surface((self.rect.width - PADDING * 2, len(self.items) * ITEM_HEIGHT))
        content_surf.fill(colors.MAIN_COLOR)

        for index, item in enumerate(self.items):
            item_rect = pygame.Rect(0, index * ITEM_HEIGHT, self.rect.width - PADDING * 2, ITEM_HEIGHT)
            pygame.draw.rect(content_surf, colors.BORDER_COLOR, item_rect, 1)
            text_surf = self.font.render(item, True, (0, 0, 0))
            content_surf.blit(text_surf, (10, index * ITEM_HEIGHT + 10))

        view_surf = pygame.Surface((self.rect.width - PADDING * 2, self.rect.height - PADDING * 2))
        view_surf.fill(colors.MAIN_COLOR)

        if len(self.items) * ITEM_HEIGHT <= self.rect.height:
            view_surf.blit(content_surf, (0, 0))
        else:
            visible_rect = pygame.Rect(0, self.scroll_y, self.rect.width - PADDING * 2, self.rect.height - PADDING * 2)
            visible_content = content_surf.subsurface(visible_rect)
            view_surf.blit(visible_content, (0, 0))

            self.scrollbar_rect = pygame.Rect(
                self.rect.width - SCROLLBAR_WIDTH - PADDING,
                0,
                SCROLLBAR_WIDTH,
                self.rect.height
            )

            scroll_handle_height = max(50, self.rect.height * (self.rect.height / (len(self.items) * ITEM_HEIGHT)))
            self.scroll_handle_rect = pygame.Rect(
                self.scrollbar_rect.x,
                PADDING,
                SCROLLBAR_WIDTH,
                min(scroll_handle_height, self.rect.height - PADDING * 2)
            )

            # Рисуем фон скроллбара
            pygame.draw.rect(view_surf, colors.SECONDARY_COLOR, self.scrollbar_rect)

            # Рассчитываем положение ползунка
            if self.max_scroll > 0:
                handle_y = (self.scroll_y / self.max_scroll) * (
                            self.rect.height - self.scroll_handle_rect.height - PADDING * 2)
                self.scroll_handle_rect.y = handle_y + PADDING

            pygame.draw.rect(view_surf, colors.BORDER_COLOR, self.scroll_handle_rect)

        # Помещаем view_surf на блок
        block.blit(view_surf, (self.rect.x + PADDING, self.rect.y + PADDING))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:  # Колесо вверх
                self.scroll_y = max(0, self.scroll_y - 20)
                return True
            elif event.button == 5:  # Колесо вниз
                self.scroll_y = min(self.max_scroll, self.scroll_y + 20)
                return True
            elif event.button == 1:  # Левая кнопка мыши
                if self.scroll_handle_rect and self.scroll_handle_rect.collidepoint(
                        event.pos[0] - self.rect.x - PADDING,
                        event.pos[1] - self.rect.y - PADDING):
                    self.dragging = True
                    self.drag_start_y = event.pos[1]
                    self.drag_start_scroll = self.scroll_y
                    return True

                if self.scrollbar_rect and self.scrollbar_rect.collidepoint(event.pos[0] - self.rect.x - PADDING,
                                                                            event.pos[1] - self.rect.y - PADDING):
                    click_ratio = (event.pos[
                                       1] - self.rect.y - PADDING - self.scrollbar_rect.y) / self.scrollbar_rect.height
                    self.scroll_y = max(0, min(self.max_scroll, int(click_ratio * self.max_scroll)))
                    return True

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and self.dragging:
                self.dragging = False
                return True

        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
                # Перемещаем ползунок
                delta_y = event.pos[1] - self.drag_start_y
                scroll_range_height = self.rect.height - self.scroll_handle_rect.height - PADDING * 2
                if scroll_range_height > 0:
                    scroll_delta = (delta_y / scroll_range_height) * self.max_scroll
                    self.scroll_y = max(0, min(self.max_scroll, self.drag_start_scroll + scroll_delta))
                return True

        return False
