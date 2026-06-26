from .Button import Button
from pygame import Surface, Rect, Event, Font
import pygame


class TextBox(Button):
    def __init__(self,
                 base: Surface,
                 highlight: Surface,
                 bottom_img: Surface,
                 rect: Rect,
                 text_img: Surface | None = None,
                 font: Font | None = None) -> None:

        super().__init__(base, highlight, bottom_img,
                         rect, text_img)

        self.font = font

        border: int = 10

        self.rect.topleft = (self.topleft[0],
                             self.topleft[1] - self.dynamic_thickness)

        self.input_text: str = ""
        self.input_surface: Surface | None = None
        self.input_rect: Rect = Rect(self.rect.left + border,
                                     self.rect.top + border,
                                     self.rect.width - border * 2,
                                     self.rect.height - border * 2)
        self.text_top_y: int = 0

        self.input_activated: bool = False
        self.cursor: int = pygame.SYSTEM_CURSOR_ARROW

    def draw(self, screen: Surface) -> None:

        screen.blit(self.bottom_img,
                    self.topleft)

        screen.blit(self.top_img,
                    (self.rect))

        # pygame.draw.rect(screen, (255, 255, 255), self.input_rect)

        if self.text_img and not self.input_text and not self.input_activated:

            text_x: int = self.rect.left + self.text_leading
            if not self.text_top_y:
                text_size_y: int = self.text_img.get_size()[1]
                self.text_top_y = self.rect.centery - text_size_y // 2

            screen.blit(self.text_img, (text_x, self.text_top_y))

        elif self.input_text:
            self.show_input_text(screen)

    def show_input_text(self, screen: Surface) -> None:

        if not self.input_surface:
            return

        txt_width = self.input_surface.get_width()
        scroll_x = max(0, txt_width - self.input_rect.width)

        screen.set_clip(self.input_rect)
        screen.blit(self.input_surface, (self.input_rect.left + 5 - scroll_x,
                                         self.text_top_y))
        screen.set_clip(None)

    def write_text(self, event: Event) -> None:

        if not self.input_activated or not self.font:
            return

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self.input_text = self.input_text[:-1]
                self.input_surface = self.font.render(self.input_text,
                                                      True, (255, 255, 255))
            else:
                self.input_text += event.unicode
                self.input_surface = self.font.render(self.input_text,
                                                      True, (255, 255, 255))

    def hover(self) -> None:
        mouse_pos: tuple[int, int] = pygame.mouse.get_pos()
        new_cursor: int = pygame.SYSTEM_CURSOR_ARROW

        if self.rect.collidepoint(mouse_pos):
            new_cursor = pygame.SYSTEM_CURSOR_IBEAM
            self.top_img = self.highlight
        else:
            new_cursor = pygame.SYSTEM_CURSOR_ARROW
            self.top_img = self.base_img

        if new_cursor != self.cursor:
            pygame.mouse.set_cursor(new_cursor)
            self.cursor = new_cursor

    def check_click(self, event: Event) -> bool:

        if event.type not in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP):
            return False

        if self.rect.collidepoint(event.pos):
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.pressed = True

            if event.type == pygame.MOUSEBUTTONUP and self.pressed:
                self.input_activated = True
                return True
        else:
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.input_activated = False
            self.pressed = False

        return False
